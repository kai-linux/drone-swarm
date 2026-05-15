import numpy as np
import gymnasium as gym
from gymnasium import spaces
from cfg import *
import swarm_cpp


class SwarmGymEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, num_drones=NUM_DRONES, world_size=WORLD_SIZE, max_steps=MAX_STEPS):
        super().__init__()

        self.world = swarm_cpp.SwarmWorld(num_drones, world_size)
        self.num_drones = num_drones
        self.world_size = world_size
        self.max_steps = max_steps
        self.current_step = 0

        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(self.world.observation_size(),),
            dtype=np.float32,
        )

        self.max_acc = 12.0

        self.action_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(self.world.action_size(),),
            dtype=np.float32,
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.world.reset()
        self.current_step = 0

        obs = np.array(self.world.observe(), dtype=np.float32)
        info = {}

        return obs, info

    def step(self, action):
        self.current_step += 1

        action = np.asarray(action, dtype=np.float32)
        action = np.clip(action, -1.0, 1.0)

        scaled_action = action * self.max_acc

        result = self.world.step_flat(scaled_action.tolist())

        obs = np.array(result.observation, dtype=np.float32)
        reward = float(result.reward)

        terminated = bool(result.done)
        truncated = self.current_step >= self.max_steps

        info = {}

        return obs, reward, terminated, truncated, info
