Project Repository - Reinforcement Learning Université Jean Monnet

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Logo_de_l%27Université_Jean_Monnet_Saint-Etienne.png/640px-Logo_de_l%27Université_Jean_Monnet_Saint-Etienne.png" alt="Université Jean Monnet" title="Université Jean Monnet">

# Project: Reinforcement Learning Applications

This project implements various *Reinforcement Learning* techniques through two distinct applications: a classic *multi-armed bandit* problem and a simplified version of the *Pac-Man* game.

## Project Structure

### 1. **Multi-Armed Bandit Problem**

The multi-armed bandit problem involves choosing from several actions to maximize rewards over time. In this project, we apply this approach to experiment with different decision-making strategies.

- **Associated File:**  
  - `Bandit.ipynb`: This notebook explores the multi-armed bandit problem and implements various experiments to maximize rewards.

---

### 2. **Simplified *Pac-Man* Game**

In this section of the project, we apply *Reinforcement Learning* to train an agent to play a simplified version of *Pac-Man*. The agent learns to interact with the environment to achieve its goals.

- **Associated Files:**  
  - `pacman_gym.py`: This file defines the *Pac-Man* game environment in which the agent operates.  
  - `qlearning.ipynb`: This notebook applies the *Q-learning* algorithm to solve the problem in the *Pac-Man* environment.  
  - `deepqlearning.ipynb`: This file uses the *Deep Q-learning* algorithm, a more advanced version of *Q-learning*, to improve the agent's performance in the game.
