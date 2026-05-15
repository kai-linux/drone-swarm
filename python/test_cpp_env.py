import swarm_cpp

world = swarm_cpp.SwarmWorld(10, 100.0)

obs = world.observe()

print("Observation size:", len(obs))
print("Action size:", world.action_size())
print("First obs values:", obs[:10])

actions = [0.0] * world.action_size()

result = world.step_flat(actions)

print("Reward:", result.reward)
print("Done:", result.done)
print("New observation size:", len(result.observation))
print("First new obs values:", result.observation[:10])
