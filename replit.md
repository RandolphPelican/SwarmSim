# Multi-Agent Coordination Simulator

## Overview

This project is a multi-agent coordination simulation framework designed to investigate constraint-driven emergence in communication networks. The system simulates autonomous agents navigating a 2D grid world where they must collect food and avoid dangers while communicating through bandwidth-constrained message channels.

The core research question explores how communication bandwidth constraints affect emergent coordination behaviors, testing for inverted U-curve relationships between bandwidth and coordination efficiency. Agents employ different decision-making strategies (greedy, balanced, cautious, explorer, cooperative, Q-learning) and share information about visible food and dangers through a prioritized message-passing system.

The application provides comprehensive visualization, statistical analysis, batch experimentation, and reinforcement learning capabilities through a Streamlit web interface with 8 interactive tabs.

**Recent Enhancements (November 2025):**
- Added advanced behavior analysis visualizations (position heatmaps, trajectories, decision analysis)
- Implemented rigorous statistical testing (ANOVA, regression, causal analysis) for hypothesis validation
- Created batch experimentation system with automated report generation
- Developed custom agent architecture framework with 5 distinct strategy types
- Integrated Q-learning reinforcement learning for adaptive agent strategies

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology**: Streamlit web framework  
**Rationale**: Provides rapid prototyping for scientific visualization and interactive parameter tuning without requiring separate frontend/backend infrastructure. The choice prioritizes research iteration speed over production-grade UI/UX.

**Key Components**:
- Tab 1: Interactive simulation with real-time visualization and parameter controls
- Tab 2: Bandwidth analysis with ANOVA and regression testing
- Tab 3: Comprehensive causal testing with effect size calculations
- Tab 4: Analytics dashboard with performance metrics and coordination tracking
- Tab 5: Behavior analysis with heatmaps, trajectories, and decision visualizations
- Tab 6: Batch experiments with template-based configuration and automated reporting
- Tab 7: Q-learning reinforcement learning with training visualization
- Tab 8: Data export in CSV and JSON formats

**Design Pattern**: Multi-tab Streamlit application with session state management for maintaining simulation history, experimental results, and RL training progress across user interactions.

### Backend Architecture

**Core Simulation Engine** (`simulation_core.py`):
- **Problem**: Need deterministic, reproducible multi-agent simulations with complex state tracking
- **Solution**: Event-driven simulation loop with centralized state management and seeded random number generation
- **Key Classes**:
  - `SimulationEnvironment`: Orchestrates agent interactions, message routing, and world state updates
  - `CoordinationAgent`: Individual agent with pluggable strategy architecture

**Agent Strategy System** (`agent_architectures.py`, `rl_agent.py`):
- **Problem**: Need to compare different decision-making approaches under identical conditions
- **Solution**: Strategy pattern with abstract base class `AgentStrategy` enabling runtime strategy selection
- **Strategies Implemented**:
  - `GreedyStrategy`: Aggressively chases food, only avoids immediate dangers
  - `CautiousStrategy`: Prioritizes safety, only seeks food when safe
  - `BalancedStrategy`: Balances food seeking with danger avoidance using weighted vectors
  - `ExplorerStrategy`: Focuses on exploring new areas while opportunistically collecting food
  - `CooperativeStrategy`: Heavily relies on team communication and shared information
  - `QLearningStrategy`: Reinforcement learning approach with discretized state space and epsilon-greedy exploration
- **Tradeoff**: Simplicity of implementation vs. sophisticated learning (current Q-learning uses simplified state discretization for tractability)
- **Integration**: All strategies selectable via UI dropdown in Interactive Simulation tab

**Logging and Observability** (`simulation_logger.py`):
- **Problem**: Need comprehensive data collection for post-hoc statistical analysis without impacting simulation performance
- **Solution**: Centralized logger with structured event recording (messages, movements, coordination events)
- **Data Captured**: Message delivery success/failure, agent trajectories, decision basis, coordination outcomes
- **Design Choice**: In-memory storage for current implementation; acknowledged limitation for large-scale batch experiments

**Message Routing with Bandwidth Constraints**:
- **Problem**: Simulate realistic communication limits in distributed systems
- **Solution**: Priority queue with bit-budget allocation per simulation step
- **Algorithm**: Messages sorted by importance score, delivered until bandwidth exhausted
- **Self-Censorship Mechanism**: Agents reduce message generation when historical delivery rates are low, creating emergent adaptive behavior

### Analysis and Experimentation Layer

**Statistical Analysis** (`statistical_analysis.py`):
- **Techniques**: ANOVA for group comparisons, polynomial regression for curve fitting, effect size calculations
- **Purpose**: Detect inverted U-curve relationships between bandwidth and coordination efficiency
- **Libraries**: SciPy, statsmodels for rigorous statistical testing

**Batch Experimentation** (`batch_experiments.py`):
- **Problem**: Need systematic parameter sweeps across bandwidth ranges with multiple replications
- **Solution**: `BatchExperimentRunner` class managing experiment queues and progress tracking
- **Output**: Structured results suitable for automated report generation

**Advanced Visualizations** (`advanced_visualizations.py`):
- Position heatmaps: Spatial density analysis showing where agents spend time
- Trajectory plots: Agent movement paths with color-coded trails
- Decision heatmaps: Visualization of decision-making patterns across the grid
- Network graphs: Message flow and communication patterns between agents
- Coordination timelines: Temporal tracking of coordination events
- Exploration coverage maps: Visualization of explored vs. unexplored areas
- Agent efficiency comparisons: Bar charts comparing individual agent performance

### Data Storage

**Current Approach**: In-memory data structures (pandas DataFrames, NumPy arrays, Python dictionaries)  
**Rationale**: Simulation runs are time-bounded and dataset sizes remain manageable for typical research parameters. Prioritizes simplicity and eliminates external dependencies.

**Acknowledged Limitation**: No persistent storage for experiment results. Users must export data manually through the UI.

**Future Consideration**: Could add SQLite for experiment history or JSON file export for reproducibility, but not currently required for core research goals.

### Configuration Management

**Approach**: Parameters passed directly through function calls and Streamlit UI controls  
**Defaults**: Hardcoded sensible defaults (world_size=15, vision_radius=3, etc.)  
**Rationale**: Keeps implementation simple for research code; no need for complex configuration systems

## External Dependencies

### Core Scientific Computing Stack
- **NumPy**: Numerical operations, distance calculations, array manipulations
- **Pandas**: Structured data analysis, experiment result aggregation
- **SciPy**: Statistical testing, curve fitting algorithms

### Visualization
- **Plotly**: Interactive charts and graphs (heatmaps, line plots, network diagrams)
- **Plotly Express**: Simplified plotting API for common visualizations

### Statistical Analysis
- **statsmodels**: ANOVA, regression analysis, post-hoc tests (Tukey HSD)

### Web Framework
- **Streamlit**: Complete web application framework providing UI components, state management, and serving

### Reinforcement Learning
- **Custom Implementation**: Q-learning agent implemented from scratch using NumPy (no external RL frameworks like TensorFlow/PyTorch)
- **Features**: 
  - Discretized state space for tractable tabular Q-learning
  - Epsilon-greedy exploration with decay
  - Configurable learning rate (α), discount factor (γ), and exploration rate (ε)
  - Real-time training visualization with Q-value evolution tracking
  - Multi-episode training with progress monitoring
- **Rationale**: Educational transparency and avoiding heavyweight dependencies for simple tabular RL

### Standard Library Dependencies
- **random, collections**: Built-in Python utilities for randomization and data structures
- **datetime, json**: Logging timestamps and data serialization

### No Database Dependencies
- The application does not currently use any database system (SQL or NoSQL)
- All data storage is in-memory for the session duration
- Future integration with PostgreSQL or similar would require adding database driver and schema design

### No External APIs or Third-Party Services
- Fully self-contained simulation environment
- No cloud services, authentication providers, or external data sources
- Can run entirely offline once dependencies are installed