#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "swarm_core.hpp"

namespace py = pybind11;

PYBIND11_MODULE(swarm_cpp, m) {
    py::class_<StepResult>(m, "StepResult")
        .def_readonly("observation", &StepResult::observation)
        .def_readonly("reward", &StepResult::reward)
        .def_readonly("done", &StepResult::done);

    py::class_<SwarmWorld>(m, "SwarmWorld")
        .def(py::init<int, double>())
        .def("reset", &SwarmWorld::reset)
        .def("observe", &SwarmWorld::observe)
        .def("step_flat", &SwarmWorld::step_flat)
        .def("compute_reward", &SwarmWorld::compute_reward)
        .def("is_done", &SwarmWorld::is_done)
        .def("action_size", &SwarmWorld::action_size)
        .def("observation_size", &SwarmWorld::observation_size);
}