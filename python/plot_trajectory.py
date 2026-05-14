import numpy as np
import matplotlib.pyplot as plt


data = np.genfromtxt("trajectory.csv", delimiter=",", names=True)

drone_ids = np.unique(data["id"]).astype(int)

plt.figure(figsize=(8, 8))

for drone_id in drone_ids:
    rows = data[data["id"] == drone_id]

    x = rows["x"]
    y = rows["y"]

    target_x = rows["target_x"][0]
    target_y = rows["target_y"][0]

    plt.plot(x, y, label=f"Drone {drone_id}")
    plt.scatter([x[0]], [y[0]], marker="o")
    plt.scatter([target_x], [target_y], marker="x")

plt.xlim(0, 100)
plt.ylim(0, 100)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Swarm World v0: drone trajectories")
plt.grid(True)
plt.legend(loc="upper right", fontsize=8)
plt.gca().set_aspect("equal", adjustable="box")
plt.show()
