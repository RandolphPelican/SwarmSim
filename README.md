# 🤖 **SwarmSim**
### *Multi-Agent Simulation for AI, Robotics, and Cognitive Science*


<p align="center">
  <img src="assets/swarmsim_logo.svg" alt="SwarmSim Logo" width="360"/>
</p>

---

## 🌟 Overview

**SwarmSim** is a flexible **multi-agent simulation framework** designed for researchers, developers, and enthusiasts exploring:

- **Swarm intelligence & robotics coordination**
- **Emergent behaviors in multi-agent systems**
- **Cognitive science and human/AI intention modeling**
- **Information theory applications in agent networks**

It combines **highly configurable simulations** with **interactive visualization**, **data collection**, and optional **game-like scenarios** for demonstration and teaching purposes.

---

## ⚙️ Key Features

- **Agent Strategies:** Multiple built-in behaviors (Greedy, Cautious, Explorer, Cooperative, Q-Learning)  
- **Dynamic Environments:** 2D grid worlds with configurable resources, hazards, and communication constraints  
- **Communication Modeling:** Adjustable bandwidth and information flow for emergent coordination analysis  
- **Scenario Engine:** Run experiments with custom parameters, test interventions, and collect structured data  
- **Batch Experiments:** Automated multi-run testing with statistical reporting (ANOVA, regression, effect sizes)  
- **Data Export:** Save results in CSV/JSON for analysis, research, or further modeling  
- **Visualization Tools:** Trajectories, heatmaps, message flows, agent states  
- **Reinforcement Learning:** Q-Learning agents with adjustable hyperparameters  
- **Interactive UI:** (future) sliders and scenario controls for real-time experimentation  

---

## 🧠 Plain-Language Concepts

**Bandwidth:** How much information agents can share at each timestep — think of it as lanes on a highway: wider = smoother coordination, narrower = bottlenecks.  

**Timestep:** A discrete “tick” in the simulation; each tick updates agent positions, decisions, and communications. Smaller timesteps = more detailed evolution.  

**Variables:** Configurable parameters that determine agent behavior and environment conditions (number of agents, resource density, speed, communication limits, randomness).  

**Simulation:** A digital “what-if” — a safe way to test hypotheses about coordination, communication, and collective intelligence.

---

## 🛠️ Installation & Setup

Clone the repository:

```bash
git clone https://github.com/RandolphPelican/SwarmSim.git
cd SwarmSim
```

Install dependencies (Python 3.8+):

```bash
pip install -r requirements.txt
```

Run the simulation:

```bash
python main.py
```

---

## 📂 Project Structure

```
SwarmSim/
│
├── main.py             # entry point
├── simulation/         # core simulation engine
├── agents/             # agent definitions and behaviors
├── environment/        # environment & grid rules
├── data/               # simulation outputs and logs
├── assets/             # logos, visualizations, animation placeholders
├── scenarios/          # presets & example setups
└── README.md
```

---

## 🎮 Gameplay & Visualization (Optional)

SwarmSim supports **interactive visualization** for demonstration, teaching, and scenario testing:

- Animated agent movement and trajectories  
- Scenario presets with adjustable variables  
- Graphical feedback for communication, coordination efficiency, and resource utilization  

These features are **secondary to the scientific research focus**, but make the simulations approachable for wider audiences.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 📬 Contact

Maintainer: **John Stabler**  
GitHub: [RandolphPelican](https://github.com/RandolphPelican)
