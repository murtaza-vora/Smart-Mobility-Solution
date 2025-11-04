import gym
from gym import spaces
import numpy as np
import time


# ======================================================
#  ENVIRONMENT CLASS
# ======================================================
class TrafficManagementEnv(gym.Env):
    """
    Custom Traffic Management Environment.
    Simulates a 4-way intersection where each direction has a traffic queue.
    RL agent controls which lane gets green light.
    Reward encourages minimizing waiting time & congestion.
    """

    def __init__(self, num_actions=4, num_observations=6):
        super(TrafficManagementEnv, self).__init__()

        self.num_actions = num_actions
        self.num_observations = num_observations

        # Define action and observation spaces
        # Actions = which direction's light to turn green
        self.action_space = spaces.Discrete(num_actions)
        # Observations = normalized traffic densities per lane + avg vehicle speed
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(num_observations,), dtype=np.float32
        )

        # Environment variables
        self.max_steps = 100
        self.current_step = 0
        self.state = None

    def reset(self):
        """Resets the environment to an initial state."""
        self.current_step = 0
        # Random traffic density per lane + avg speed
        traffic_density = np.random.rand(self.num_observations - 1)
        avg_speed = np.random.rand(1)  # Normalized speed (0–1)
        self.state = np.concatenate((traffic_density, avg_speed))
        return self.state

    def step(self, action):
        """Applies an action and returns (next_state, reward, done, info)."""

        self.current_step += 1

        # Simulate environment dynamics
        traffic_density = self.state[:-1]
        avg_speed = self.state[-1]

        # Action represents which direction's light turns green
        # Reduce density in that lane (simulate traffic clearing)
        if 0 <= action < len(traffic_density):
            traffic_density[action] = max(0, traffic_density[action] - np.random.uniform(0.1, 0.3))

        # Add some random noise (new cars arriving)
        traffic_density += np.random.uniform(0.01, 0.05, size=traffic_density.shape)
        traffic_density = np.clip(traffic_density, 0, 1)

        # Update speed (inverse of congestion)
        avg_speed = 1 - np.mean(traffic_density)

        # Combine new state
        self.state = np.concatenate((traffic_density, [avg_speed]))

        # Reward: higher for higher avg speed and lower congestion
        reward = avg_speed - np.mean(traffic_density)

        done = self.current_step >= self.max_steps
        info = {}

        return self.state, float(reward), done, info


# ======================================================
#  Q-LEARNING AGENT
# ======================================================
class QLearningAgent:
    def __init__(
        self,
        num_states,
        num_actions,
        learning_rate=0.1,
        discount_factor=0.99,
        exploration_rate=1.0,
        exploration_decay=0.01,
        min_exploration=0.01,
    ):
        self.num_states = num_states
        self.num_actions = num_actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        self.decay = exploration_decay
        self.min_epsilon = min_exploration

        # Initialize Q-table
        # We’ll discretize states for simplicity
        self.q_table = np.zeros((10 ** num_states, num_actions))

    def _discretize_state(self, state):
        """Convert continuous observation into discrete index."""
        bins = np.digitize(state, np.linspace(0, 1, 10)) - 1
        return int("".join(map(str, bins)))

    def choose_action(self, state):
        """Epsilon-greedy strategy."""
        state_idx = self._discretize_state(state)
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(self.num_actions)
        return np.argmax(self.q_table[state_idx, :])

    def update(self, state, action, reward, next_state):
        """Update Q-table using the Bellman equation."""
        state_idx = self._discretize_state(state)
        next_state_idx = self._discretize_state(next_state)

        best_next_action = np.max(self.q_table[next_state_idx, :])
        td_target = reward + self.gamma * best_next_action
        td_error = td_target - self.q_table[state_idx, action]
        self.q_table[state_idx, action] += self.lr * td_error

    def decay_epsilon(self, episode):
        self.epsilon = self.min_epsilon + (1.0 - self.min_epsilon) * np.exp(-self.decay * episode)


# ======================================================
#  TRAINING FUNCTION
# ======================================================
def train(env, agent, num_episodes=1000, max_steps=100):
    total_rewards = []

    start_time = time.time()

    for episode in range(num_episodes):
        state = env.reset()
        total_reward = 0

        for step in range(max_steps):
            action = agent.choose_action(state)
            next_state, reward, done, _ = env.step(action)
            agent.update(state, action, reward, next_state)

            total_reward += reward
            state = next_state

            if done:
                break

        agent.decay_epsilon(episode)
        total_rewards.append(total_reward)

        if (episode + 1) % 100 == 0:
            print(f"Episode {episode+1}/{num_episodes} | Total Reward: {total_reward:.3f}")

    end_time = time.time()
    print(f"\nTraining completed in {end_time - start_time:.2f} seconds")
    return total_rewards


# ======================================================
#  EVALUATION FUNCTION
# ======================================================
def evaluate(env, agent, episodes=100, max_steps=100):
    total_rewards = 0
    for _ in range(episodes):
        state = env.reset()
        for _ in range(max_steps):
            action = np.argmax(agent.q_table[agent._discretize_state(state), :])
            next_state, reward, done, _ = env.step(action)
            total_rewards += reward
            state = next_state
            if done:
                break
    avg_reward = total_rewards / episodes
    print(f"\nAverage Evaluation Reward: {avg_reward:.3f}")
    return avg_reward


# ======================================================
#  MAIN EXECUTION
# ======================================================
def main():
    num_actions = 4
    num_observations = 6

    env = TrafficManagementEnv(num_actions=num_actions, num_observations=num_observations)
    agent = QLearningAgent(num_states=num_observations, num_actions=num_actions)

    print("🚦 Starting training...")
    train(env, agent, num_episodes=500, max_steps=100)

    print("\n🏁 Evaluating trained agent...")
    evaluate(env, agent, episodes=100, max_steps=100)


if __name__ == "__main__":
    main()
