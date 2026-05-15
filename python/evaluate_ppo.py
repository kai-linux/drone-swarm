from stable_baselines3 import PPO
from cfg import *
from swarm_gym_env import SwarmGymEnv


env = SwarmGymEnv(num_drones=NUM_DRONES, world_size=WORLD_SIZE, max_steps=MAX_STEPS)
model = PPO.load("python/swarm_ppo_model")

obs, info = env.reset()

total_reward = 0.0

for step in range(MAX_STEPS):
    action, _ = model.predict(obs, deterministic=True)

    obs, reward, terminated, truncated, info = env.step(action)
    total_reward += reward

    if step % 50 == 0:
        print(f"step={step}, reward={reward:.3f}, total={total_reward:.3f}")

    if terminated or truncated:
        print(
            f"Episode ended at step={step}, "
            f"terminated={terminated}, truncated={truncated}, "
            f"total_reward={total_reward:.3f}"
        )
        break
