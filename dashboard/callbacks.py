from dash import Input, Output, State, no_update, html

from dashboard.components import format_integer, format_latency, format_percentage
from dashboard.plots import (
    build_kpi_data,
    make_deadline_miss_chart,
    make_latency_comparison_chart,
    make_queue_length_timeseries,
    make_resource_allocation_heatmap,
    make_throughput_chart,
    make_urllc_deadline_miss_chart,
    make_urllc_latency_chart,
)
from schedulers.qos_aware import QoSAwareScheduler
from schedulers.round_robin import RoundRobinScheduler
from simulator.engine import SimulationEngine


def register_callbacks(app) -> None:
    @app.callback(
        Output("comparison-results-store", "data"),
        Input("run-button", "n_clicks"),
        State("scenario-dropdown", "value"),
        prevent_initial_call=True,
    )
    def run_simulation_comparison(n_clicks: int, scenario_name: str):
        if not n_clicks:
            return no_update

        rr_results = SimulationEngine(
            scheduler=RoundRobinScheduler(),
            scenario_name=scenario_name,
        ).run()

        qos_results = SimulationEngine(
            scheduler=QoSAwareScheduler(),
            scenario_name=scenario_name,
        ).run()

        return {
            "rr_results": rr_results,
            "qos_results": qos_results,
        }

    @app.callback(
        Output("rr-latency-card", "children"),
        Output("qos-latency-card", "children"),
        Output("rr-urllc-latency-card", "children"),
        Output("qos-urllc-latency-card", "children"),
        Output("rr-miss-card", "children"),
        Output("qos-miss-card", "children"),
        Output("rr-drop-card", "children"),
        Output("qos-drop-card", "children"),
        Output("latency-comparison-chart", "figure"),
        Output("urllc-latency-chart", "figure"),
        Output("deadline-miss-chart", "figure"),
        Output("urllc-deadline-miss-chart", "figure"),
        Output("throughput-chart", "figure"),
        Output("rr-queue-chart", "figure"),
        Output("qos-queue-chart", "figure"),
        Output("rr-heatmap-chart", "figure"),
        Output("qos-heatmap-chart", "figure"),
        Input("comparison-results-store", "data"),
        prevent_initial_call=False,
    )
    def update_dashboard(comparison_data):
        if not comparison_data:
            return (
                "—",
                "—",
                "—",
                "—",
                "—",
                "—",
                "—",
                "—",
                {},
                {},
                {},
                {},
                {},
                {},
                {},
                {},
                {},
            )

        rr_results = comparison_data["rr_results"]
        qos_results = comparison_data["qos_results"]

        kpi = build_kpi_data(rr_results, qos_results)

        rr_latency = format_latency(kpi["rr_latency"])
        qos_latency = format_latency(kpi["qos_latency"])

        rr_urllc_latency = format_latency(
            rr_results["avg_latency_by_class"].get("URLLC", 0.0)
        )
        qos_urllc_latency = format_latency(
            qos_results["avg_latency_by_class"].get("URLLC", 0.0)
        )

        rr_miss = format_percentage(kpi["rr_deadline_miss"])
        qos_miss = format_percentage(kpi["qos_deadline_miss"])

        rr_drop = format_integer(kpi["rr_dropped"])
        qos_drop = format_integer(kpi["qos_dropped"])

        latency_fig = make_latency_comparison_chart(rr_results, qos_results)
        urllc_latency_fig = make_urllc_latency_chart(rr_results, qos_results)
        miss_fig = make_deadline_miss_chart(rr_results, qos_results)
        urllc_miss_fig = make_urllc_deadline_miss_chart(rr_results, qos_results)
        throughput_fig = make_throughput_chart(rr_results, qos_results)

        rr_queue_fig = make_queue_length_timeseries(
            rr_results,
            "Round Robin Queue Length Over Time",
        )
        qos_queue_fig = make_queue_length_timeseries(
            qos_results,
            "QoS-Aware Queue Length Over Time",
        )

        rr_heatmap_fig = make_resource_allocation_heatmap(
            rr_results,
            "Round Robin Resource Allocation Heatmap",
        )
        qos_heatmap_fig = make_resource_allocation_heatmap(
            qos_results,
            "QoS-Aware Resource Allocation Heatmap",
        )

        return (
            rr_latency,
            qos_latency,
            rr_urllc_latency,
            qos_urllc_latency,
            rr_miss,
            qos_miss,
            rr_drop,
            qos_drop,
            latency_fig,
            urllc_latency_fig,
            miss_fig,
            urllc_miss_fig,
            throughput_fig,
            rr_queue_fig,
            qos_queue_fig,
            rr_heatmap_fig,
            qos_heatmap_fig,
        )
    @app.callback(
        Output("factory-view", "children"),
        Output("factory-frame-index", "data"),
        Input("factory-timer", "n_intervals"),
        State("comparison-results-store", "data"),
        State("factory-frame-index", "data"),
    )
    def update_factory_view(n, data, frame_index):
        if not data:
            return html.Div(
                "Run simulation to start the smart factory animation.",
                className="factory-empty",
            ), 0

        frame_index = frame_index or 0

        rr_results = data["rr_results"]
        qos_results = data["qos_results"]

        def build_factory_panel(title, results, panel_type):
            queue_history = results["queue_length_history"]
            congestion_history = results["congestion_history"]
            resource_history = results["resource_usage_history"]
            dropped_packets = results.get("dropped_packets", [])

            if not queue_history:
                return html.Div("No simulation data.", className="factory-empty")

            idx = frame_index % len(queue_history)

            snapshot = queue_history[idx]
            congestion = congestion_history[idx]["is_congested"]
            prev_congestion = False
            if idx > 0:
                prev_congestion = congestion_history[idx - 1]["is_congested"]
            congestion_started = congestion and not prev_congestion
            total_queue = congestion_history[idx]["total_queue_length"]
            allocation = resource_history[idx]["allocation_by_class"]

            drops_so_far = sum(
                1 for packet in dropped_packets
                if packet.get("arrival_time", 0) <= snapshot["time"]
            )

            traffic_info = {
                "URLLC": {
                    "label": "URLLC Critical Control",
                    "color": "#ef4444",
                    "emoji": "🚨",
                },
                "eMBB": {
                    "label": "eMBB Camera / Video",
                    "color": "#3b82f6",
                    "emoji": "📹",
                },
                "mMTC": {
                    "label": "mMTC Sensors",
                    "color": "#22c55e",
                    "emoji": "📡",
                },
                "NON_GBR": {
                    "label": "Non-GBR Background",
                    "color": "#9ca3af",
                    "emoji": "📦",
                },
            }

            def packet_stream(traffic_class, count):
                visible_packets = min(max(count, 1), 12)

                return html.Div(
                    className="packet-stream",
                    children=[
                        html.Div(
                            className=f"moving-packet packet-{traffic_class.lower().replace('_', '-')}",
                            style={
                                "animationDelay": f"{i * 0.15}s",
                            },
                            children=traffic_info[traffic_class]["emoji"]
                        )
                        for i in range(visible_packets)
                    ],
                )

            def build_lane(traffic_class):
                count = snapshot.get(traffic_class, 0)
                used = allocation.get(traffic_class, 0)
                active = used > 0

                pressure_class = "lane-danger" if count >= 80 else "lane-warning" if count >= 40 else "lane-normal"

                return html.Div(
                    className=f"factory-lane {pressure_class} {'lane-active' if active else ''}",
                    children=[
                        html.Div(
                            className="lane-source",
                            children=[
                                html.Div(traffic_info[traffic_class]["emoji"], className="source-icon"),
                                html.Div(traffic_class, className="source-name"),
                            ],
                        ),
                        html.Div(
                            className="conveyor-zone",
                            children=[
                                packet_stream(traffic_class, count),
                                html.Div(className="conveyor-belt"),
                            ],
                        ),
                        html.Div(
                            className="queue-box",
                            children=[
                                html.Div("QUEUE", className="queue-title"),
                                html.Div(str(count), className="queue-count"),
                            ],
                        ),
                        html.Div(
                            className="allocation-box",
                            children=[
                                html.Div("served", className="allocation-label"),
                                html.Div(str(used), className="allocation-value"),
                            ],
                        ),
                    ],
                )

            return html.Div(
                className=f"factory-panel {panel_type}",
                children=[
                    html.Div(
                        className="factory-panel-header",
                        children=[
                            html.Div(title, className="factory-panel-title"),
                            html.Div(
                                "🚨 CONGESTION STARTED"
                                if congestion_started
                                else "⚠️ CONGESTED"
                                if congestion
                                else "✅ NORMAL",
                                className=(
                                    "factory-status status-started"
                                    if congestion_started
                                    else f"factory-status {'status-danger' if congestion else 'status-normal'}"
                                ),
                                
                            ),
                        ],
                    ),

                    html.Div(
                        className="factory-stats-row",
                        children=[
                            html.Div(
                                children=[
                                    html.Span("Time"),
                                    html.Strong(str(snapshot["time"])),
                                ],
                                className="factory-stat",
                            ),
                            html.Div(
                                children=[
                                    html.Span("Total Queue"),
                                    html.Strong(str(total_queue)),
                                ],
                                className="factory-stat",
                            ),
                            html.Div(
                                children=[
                                    html.Span("Drops"),
                                    html.Strong(str(drops_so_far)),
                                ],
                                className="factory-stat",
                            ),
                        ],
                    ),

                    html.Div(
                        className="factory-flow",
                        children=[
                            html.Div(
                                className="factory-lanes",
                                children=[
                                    build_lane("URLLC"),
                                    build_lane("eMBB"),
                                    build_lane("mMTC"),
                                    build_lane("NON_GBR"),
                                ],
                            ),

                            html.Div(
                                className="scheduler-station",
                                children=[
                                    html.Div("🤖", className="robot-arm"),
                                    html.Div("Scheduler", className="robot-label"),
                                    html.Div(
                                        "QoS priority + urgency"
                                        if panel_type == "qos-panel"
                                        else "Fixed rotation",
                                        className="robot-mode",
                                    ),
                                ],
                            ),

                            html.Div(
                                className="machine-station",
                                children=[
                                    html.Div("⚙️", className="machine-icon"),
                                    html.Div("5G Resource Block", className="machine-title"),
                                    html.Div("Processing packets", className="machine-subtitle"),
                                ],
                            ),

                            html.Div(
                                className="output-zone",
                                children=[
                                    html.Div("✅ Output", className="output-good"),
                                    html.Div("🗑️ Drops", className="output-drop"),
                                ],
                            ),
                        ],
                    ),
                ],
            )

        view = html.Div(
            className="factory-comparison",
            children=[
                html.Div(
                    className="factory-explainer",
                    children=[
                        html.H3("Smart Factory Packet Flow"),
                        html.P(
                            "Packets move like factory items on conveyor belts. "
                            "The scheduler robot decides which traffic gets processed first. "
                            "Round Robin follows a fixed order, while QoS-Aware reacts to urgency, queue pressure, and congestion."
                        ),
                    ],
                ),
                html.Div(
                    className="factory-panels-grid",
                    children=[
                        build_factory_panel("Round Robin Factory", rr_results, "rr-panel"),
                        build_factory_panel("QoS-Aware Factory", qos_results, "qos-panel"),
                    ],
                ),
            ],
        )

        return view, frame_index + 1