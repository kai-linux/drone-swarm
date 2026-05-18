import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

import swarm_cpp


MAX_ACC = 12.0
KP = 0.8
KD = 1.2


def clamp_length(v, max_len):
    norm = np.linalg.norm(v)
    if norm <= max_len:
        return v
    return v / (norm + 1e-8) * max_len


def expert_action(obs6):
    # obs6 = [x, y, vx, vy, target_dx, target_dy]
    vx = obs6[2]
    vy = obs6[3]
    target_dx = obs6[4]
    target_dy = obs6[5]

    acc = np.array([
        KP * target_dx - KD * vx,
        KP * target_dy - KD * vy,
    ], dtype=np.float32)

    acc = clamp_length(acc, MAX_ACC)

    # normalize to [-1, 1]
    return acc / MAX_ACC


def collect_dataset(num_episodes=200, max_steps=300):
    xs = []
    ys = []

    world = swarm_cpp.SwarmWorld(1, 100.0)

    for _ in range(num_episodes):
        world.reset()

        for _ in range(max_steps):
            obs = np.array(world.observe(), dtype=np.float32)
            action_norm = expert_action(obs)

            xs.append(obs)
            ys.append(action_norm)

            real_action = action_norm * MAX_ACC
            result = world.step_flat(real_action.tolist())

            if result.done:
                break

    x = torch.tensor(np.array(xs), dtype=torch.float32)
    y = torch.tensor(np.array(ys), dtype=torch.float32)

    return x, y


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


def main():
    x, y = collect_dataset()

    print("Dataset x:", x.shape)
    print("Dataset y:", y.shape)

    model = DronePolicy()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()

    for epoch in range(200):
        pred = model(x)
        loss = loss_fn(pred, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 20 == 0:
            print(f"epoch={epoch}, loss={loss.item():.6f}")

    torch.save(model.state_dict(), "python/shared_drone_bc.pt")
    print("Saved python/shared_drone_bc.pt")


if __name__ == "__main__":
    main()
