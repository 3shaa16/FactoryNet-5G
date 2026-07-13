# 🚀 FactoryNet 5G Network Simulator

An interactive **5G network simulation framework** that models traffic scheduling in a smart factory environment. The project compares a traditional **Round Robin scheduler** with a custom **QoS-Aware Scheduler** to evaluate network performance under varying traffic loads, including severe congestion scenarios.

---

## 📖 Overview

Modern industrial applications rely on 5G networks to support diverse traffic types with different Quality of Service (QoS) requirements. FactoryNet simulates these environments by generating realistic traffic, scheduling packets, and visualizing network behavior through an interactive dashboard.

The simulator enables users to compare scheduling strategies and analyze key network performance metrics such as latency, throughput, fairness, packet loss, and deadline violations.

---

## ✨ Features

* Modular 5G network simulation framework
* Interactive dashboard built with **Dash** and **Plotly**
* Custom QoS-Aware scheduling algorithm
* Round Robin scheduler for baseline comparison
* Multiple traffic scenarios
* Real-time visualization of packet flow and congestion
* Performance analysis using industry-relevant QoS metrics

---

## 🏭 Simulated Traffic Classes

| Traffic Class | Description                                                             |
| ------------- | ----------------------------------------------------------------------- |
| **URLLC**     | Ultra-Reliable Low-Latency Communications (critical industrial control) |
| **eMBB**      | Enhanced Mobile Broadband (high-bandwidth applications)                 |
| **mMTC**      | Massive Machine-Type Communications (IoT sensor networks)               |
| **Non-GBR**   | Best-effort background traffic                                          |

---

## 📊 Performance Metrics

The simulator evaluates scheduler performance using:

* Average latency
* URLLC latency
* Throughput
* Packet drop rate
* Deadline miss rate
* Jain's Fairness Index

---

## 🔀 Scheduling Algorithms

### Round Robin

* Equal resource allocation
* Simple and fair
* Does not consider packet priority or deadlines

### QoS-Aware Scheduler

* Priority-based scheduling
* Considers packet deadlines
* Monitors queue congestion
* Dynamically adapts resource allocation
* Improves performance during network congestion

---

## 🧪 Available Scenarios

* **Balanced Load** – Normal network conditions
* **Industrial Congestion** – Temporary traffic spikes
* **Extreme Congestion** – Heavy overload for stress testing

---

## 🛠️ Technology Stack

* Python
* Dash
* Plotly
* SimPy
* NumPy
* Pandas
* Pytest

---

## 📂 Project Structure

```text
FactoryNet-5G-Simulator/
│
├── app.py                  # Application entry point
├── simulator/              # Core simulation engine
├── schedulers/             # Scheduling algorithms
├── dashboard/              # Dash user interface
├── experiments/            # Simulation experiments
├── config/                 # Scenario configurations
├── assets/                 # Images and styling
├── tests/                  # Unit tests
└── requirements.txt
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/FactoryNet-5G-Simulator.git
cd FactoryNet-5G-Simulator
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**macOS/Linux**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open your browser and navigate to:

```
http://127.0.0.1:8050
```

---

## 📈 Results

Experimental evaluation shows that the QoS-Aware Scheduler consistently outperforms the Round Robin approach during periods of high congestion by:

* Reducing packet latency
* Lowering deadline miss rates
* Prioritizing critical URLLC traffic
* Improving overall network efficiency
* Maintaining better fairness across traffic classes

---

## 🔮 Future Work

* Reinforcement Learning-based scheduling
* Multi-cell 5G network simulation
* Dynamic radio resource allocation
* More realistic industrial traffic models
* Real-time data streaming support

