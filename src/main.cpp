#include "swarm_core.hpp"

int main() {
    int num_drones = 10;
    double world_size = 100.0;

    SwarmWorld world(num_drones, world_size);

    std::vector<double> obs = world.observe();

    std::cout << "Observation size: " << obs.size() << "\n";
    std::cout << "First values: ";

    for (size_t i = 0; i < std::min<size_t>(obs.size(), 10); ++i) {
        std::cout << obs[i] << " ";
    }

    std::cout << "\n";

    std::ofstream out("trajectory.csv");

    if (!out) {
        std::cerr << "Could not open trajectory.csv for writing.\n";
        return 1;
    }

    world.write_csv_header(out);

    const int num_steps = 1000;

    std::vector<Action> actions(num_drones);

    for (int step = 0; step < num_steps; ++step) {
        world.write_csv_row(out, step);

        std::vector<Action> actions = make_target_actions(world);

        StepResult result = world.step(actions);

        double reward = result.reward;
        bool done = result.done;

        if (step % 100 == 0) {
            std::cout << "Step " << step << ", reward: " << reward << ", observation size: " << result.observation.size() << "\n";
        }

        if (done) {
            std::cout << "All drones reached their targets at step " << step << " with reward " << reward << "\n";
            break;
        }
    }

    std::cout << "Simulation finished. Wrote trajectory.csv\n";

    return 0;
}
