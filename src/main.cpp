#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>
#include <algorithm>

struct Vec2 {
    double x = 0.0;
    double y = 0.0;
};

Vec2 operator+(Vec2 a, Vec2 b) {
    return {a.x + b.x, a.y + b.y};
}

Vec2 operator-(Vec2 a, Vec2 b) {
    return {a.x - b.x, a.y - b.y};
}

Vec2 operator*(Vec2 a, double s) {
    return {a.x * s, a.y * s};
}

Vec2 operator/(Vec2 a, double s) {
    return {a.x / s, a.y / s};
}

double length(Vec2 a) {
    return std::sqrt(a.x * a.x + a.y * a.y);
}

Vec2 normalize(Vec2 a) {
    double len = length(a);
    if (len < 1e-9) {
        return {0.0, 0.0};
    }
    return a / len;
}

Vec2 clamp_length(Vec2 a, double max_len) {
    double len = length(a);
    if (len <= max_len) {
        return a;
    }
    return normalize(a) * max_len;
}

struct Drone {
    Vec2 pos;
    Vec2 vel;
    Vec2 target;
};

struct Action {
    double ax = 0.0;
    double ay = 0.0;
};

class SwarmWorld {
public:
    SwarmWorld(int num_drones, double world_size)
        : world_size_(world_size)
    {
        std::mt19937 rng(42);
        std::uniform_real_distribution<double> dist(5.0, world_size_ - 5.0);

        drones_.reserve(num_drones);

        for (int i = 0; i < num_drones; ++i) {
            Drone d;
            d.pos = {dist(rng), dist(rng)};
            d.vel = {0.0, 0.0};
            d.target = {dist(rng), dist(rng)};
            drones_.push_back(d);
        }
    }

    void step(const std::vector<Action>& actions) {
        std::vector<Vec2> accelerations(drones_.size());

        for (size_t i = 0; i < drones_.size(); ++i) {
            Drone& d = drones_[i];

            Vec2 to_target = d.target - d.pos;

            // Simple proportional-derivative controller:
            // accelerate toward the target, damp current velocity.
            // Vec2 acc = to_target * kp_ - d.vel * kd_;
            Vec2 acc{actions[i].ax, actions[i].ay};

            // Basic collision avoidance:
            // if another drone is close, push away from it.
            for (size_t j = 0; j < drones_.size(); ++j) {
                if (i == j) continue;

                Vec2 away = d.pos - drones_[j].pos;
                double dist = length(away);

                if (dist < avoid_radius_ && dist > 1e-9) {
                    double strength = (avoid_radius_ - dist) / avoid_radius_;
                    acc = acc + normalize(away) * (avoid_gain_ * strength);
                }
            }

            accelerations[i] = clamp_length(acc, max_acc_);
        }

        for (size_t i = 0; i < drones_.size(); ++i) {
            Drone& d = drones_[i];

            d.vel = d.vel + accelerations[i] * dt_;
            d.vel = clamp_length(d.vel, max_speed_);
            d.pos = d.pos + d.vel * dt_;

            handle_walls(d);

            // If target reached, keep it simple for now:
            // stop at target instead of assigning a new one.
            if (length(d.target - d.pos) < target_radius_) {
                d.vel = {0.0, 0.0};
            }
        }
    }

    void write_csv_header(std::ofstream& out) const {
        out << "step,id,x,y,vx,vy,target_x,target_y\n";
    }

    void write_csv_row(std::ofstream& out, int step_idx) const {
        for (size_t i = 0; i < drones_.size(); ++i) {
            const Drone& d = drones_[i];
            out
                << step_idx << ","
                << i << ","
                << d.pos.x << ","
                << d.pos.y << ","
                << d.vel.x << ","
                << d.vel.y << ","
                << d.target.x << ","
                << d.target.y << "\n";
        }
    }

    const std::vector<Drone>& drones() const {
        return drones_;
    }

    std::vector<double> observe() const {
        std::vector<double> obs;
        obs.reserve(drones_.size() * 6);

        for (const Drone& d : drones_) {
            obs.push_back(d.pos.x);
            obs.push_back(d.pos.y);
            obs.push_back(d.vel.x);
            obs.push_back(d.vel.y);
            obs.push_back(d.target.x - d.pos.x);
            obs.push_back(d.target.y - d.pos.y);
        }

        return obs;
    }

    double compute_reward() const {
        double reward = 0.0;

        // Reward drones for being close to their targets
        for (const Drone& d : drones_) {
            double dist_to_target = length(d.target - d.pos);
            reward -= dist_to_target * 0.01;
        }

        // Penalize drone collisions / too-close situations
        for (size_t i = 0; i < drones_.size(); ++i) {
            for (size_t j = i + 1; j < drones_.size(); ++j) {
                double dist = length(drones_[i].pos - drones_[j].pos);

                if (dist < 2.0) {
                    reward -= 10.0;
                }
            }
        }

        // Bonus if all drones reached targets
        if (is_done()) {
            reward += 100.0;
        }

        return reward;
    }

    bool is_done() const {
        for (const Drone& d : drones_) {
            double dist_to_target = length(d.target - d.pos);

            if (dist_to_target > target_radius_) {
                return false;
            }
        }

        return true;
    }
private:
    void handle_walls(Drone& d) {
        if (d.pos.x < 0.0) {
            d.pos.x = 0.0;
            d.vel.x *= -0.5;
        }

        if (d.pos.x > world_size_) {
            d.pos.x = world_size_;
            d.vel.x *= -0.5;
        }

        if (d.pos.y < 0.0) {
            d.pos.y = 0.0;
            d.vel.y *= -0.5;
        }

        if (d.pos.y > world_size_) {
            d.pos.y = world_size_;
            d.vel.y *= -0.5;
        }
    }

private:
    double world_size_ = 100.0;
    double dt_ = 0.05;

    double max_speed_ = 8.0;
    double max_acc_ = 12.0;

    double kp_ = 0.8;
    double kd_ = 1.2;

    double avoid_radius_ = 6.0;
    double avoid_gain_ = 20.0;

    double target_radius_ = 1.0;

    std::vector<Drone> drones_;

};

std::vector<Action> make_target_actions(const SwarmWorld& world) {
    const std::vector<Drone>& drones = world.drones();

    std::vector<Action> actions(drones.size());

    double kp = 0.8;
    double kd = 1.2;
    double max_acc = 12.0;

    for (size_t i = 0; i < drones.size(); ++i) {
        const Drone& d = drones[i];

        Vec2 to_target = d.target - d.pos;

        Vec2 acc = to_target * kp - d.vel * kd;
        acc = clamp_length(acc, max_acc);

        actions[i].ax = acc.x;
        actions[i].ay = acc.y;
    }

    return actions;
}

int main() {
    SwarmWorld world(10, 100.0);

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

    std::vector<Action> actions(10);

    for (int step = 0; step < num_steps; ++step) {
        world.write_csv_row(out, step);

        std::vector<Action> actions = make_target_actions(world);

        world.step(actions);
    }

    std::cout << "Simulation finished. Wrote trajectory.csv\n";

    return 0;
}
