from stable_baselines3 import PPO

from swarm_gym_env import SwarmGymEnv


env = SwarmGymEnv(num_drones=10, world_size=100.0, max_steps=300)
model = PPO.load("python/swarm_ppo_model")

obs, info = env.reset()

total_reward = 0.0

for step in range(300):
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
