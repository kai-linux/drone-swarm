import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from cfg import *
from swarm_gym_env import SwarmGymEnv

env = SwarmGymEnv(num_drones=NUM_DRONES, world_size=WORLD_SIZE, max_steps=MAX_STEPS)
model = PPO.load("python/swarm_ppo_model")

obs, info = env.reset()

positions = []
targets = []
rewards = []

for step in range(MAX_STEPS):
    # obs format per drone:
    # x, y, vx, vy, target_dx, target_dy
    x = obs[0]
    y = obs[1]
    target_x = obs[0] + obs[4]
    target_y = obs[1] + obs[5]

    positions.append((x, y))
    targets.append((target_x, target_y))

    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)

    rewards.append(reward)

    if terminated or truncated:
        print(
            f"Episode ended at step={step}, "
            f"terminated={terminated}, truncated={truncated}, "
            f"total_reward={sum(rewards):.3f}"
        )
        break

positions = np.array(positions)
targets = np.array(targets)

plt.figure(figsize=(7, 7))

plt.plot(positions[:, 0], positions[:, 1], label="Drone path")
plt.scatter(positions[0, 0], positions[0, 1], marker="o", label="Start")
plt.scatter(targets[0, 0], targets[0, 1], marker="x", label="Target")

plt.xlim(0, 100)
plt.ylim(0, 100)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Learned PPO policy: 1 drone target reaching")
plt.grid(True)
plt.legend()
plt.gca().set_aspect("equal", adjustable="box")
plt.show()

plt.figure(figsize=(8, 4))
plt.plot(rewards)
plt.xlabel("Step")
plt.ylabel("Reward")
plt.title("Reward during evaluation episode")
plt.grid(True)
plt.show()
