from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from cfg import *
from swarm_gym_env import SwarmGymEnv


env = SwarmGymEnv(num_drones=NUM_DRONES, world_size=WORLD_SIZE, max_steps=MAX_STEPS)

check_env(env, warn=True)

model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    device="cpu",
    learning_rate=3e-4,
    n_steps=1024,
    batch_size=64,
    gamma=0.99,
)

model.learn(total_timesteps=100_000)

model.save("python/swarm_ppo_model")

print("Saved model to python/swarm_ppo_model.zip")
