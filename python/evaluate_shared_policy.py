import numpy as np
import torch
import torch.nn as nn

from swarm_gym_env import SwarmGymEnv


class DronePolicy(nn.Module):
    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(6, 64),
            nn.Tanh(),
            nn.Linear(64, 64),
            nn.Tanh(),
            nn.Linear(64, 2),
            nn.Tanh(),
        )

    def forward(self, x):
        return self.net(x)


def make_actions(model, obs, num_drones):
    actions = []

    with torch.no_grad():
        for i in range(num_drones):
            obs6 = obs[i * 6:(i + 1) * 6]
            obs_tensor = torch.tensor(obs6, dtype=torch.float32).unsqueeze(0)

            action = model(obs_tensor).squeeze(0).numpy()
            actions.extend(action.tolist())

    return np.array(actions, dtype=np.float32)


def run_eval(num_drones):
    env = SwarmGymEnv(num_drones=num_drones, world_size=100.0, max_steps=300)

    model = DronePolicy()
    model.load_state_dict(torch.load("python/shared_drone_bc.pt"))
    model.eval()

    obs, info = env.reset()

    total_reward = 0.0

    for step in range(300):
        action = make_actions(model, obs, num_drones)

        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward

        if step % 50 == 0:
            print(
                f"drones={num_drones}, step={step}, "
                f"reward={reward:.3f}, total={total_reward:.3f}"
            )

        if terminated or truncated:
            print(
                f"drones={num_drones}, ended at step={step}, "
                f"terminated={terminated}, truncated={truncated}, "
                f"total_reward={total_reward:.3f}"
            )
            break


if __name__ == "__main__":
    run_eval(num_drones=1)
    run_eval(num_drones=2)
    run_eval(num_drones=5)
