"""Test integrated joint angles for screw based motion generators."""
from __future__ import annotations

import numpy as np
from dqrobotics.robots import FrankaEmikaPandaRobot

from screwmpcpy.dqutil import dq_pose_error
from screwmpcpy.pandamg import (
    PandaScrewMotionGenerator,
    PandaScrewMpMotionGenerator,
)
from screwmpcpy.screwintegrator import simulate_joint_waypoints
from screwmpcpy.screwmpc import BOUND


def test_simulate_joint_waypoints() -> None:
    """Test simulated waypoints from panda screw motion generator"""
    Np = 50  # prediction horizon, can be tuned;
    Nc = 10  # control horizon, can be tuned
    R = 10e-3  # weight matirix
    Q = 10e9  # weight matrix

    q_initial = np.array(
        [0.173898, 0.667434, 0.782032, -1.86421, 1.44847, 1.57491, 0.889156]
    )

    ub_jerk = np.array([8500.0, 8500.0, 8500.0, 4500.0, 4500.0, 4500.0])
    lb_jerk = -ub_jerk.copy()

    ub_acc = np.array([17.0, 17.0, 17.0, 9.0, 9.0, 9.0])
    lb_acc = -ub_acc.copy()

    ub_v = np.array([2.5, 2.5, 2.5, 3.0, 3.0, 3.0])
    lb_v = -ub_v.copy()

    jerk_bound = BOUND(lb_jerk, ub_jerk)
    acc_bound = BOUND(lb_acc, ub_acc)
    vel_bound = BOUND(lb_v, ub_v)

    franka_kin = FrankaEmikaPandaRobot.kinematics()

    goal = franka_kin.fkm(
        [0.173898, 0.667434, 0.782032, -1.86421, 1.44847, 1.57491, 0.889156]
    )

    mg = PandaScrewMotionGenerator(
        Np, Nc, Q, R, vel_bound, acc_bound, jerk_bound, sclerp=0.5
    )

    waypoints, ok = simulate_joint_waypoints(mg, q_initial, goal, dt=1e-3)

    assert ok
    assert len(waypoints) > 0
    assert len(waypoints) <= 1000
    np.testing.assert_array_equal(q_initial, waypoints[0])
    _goal = franka_kin.fkm(waypoints[-1])
    error = dq_pose_error(_goal, goal)
    assert np.linalg.norm(error.vec8()) < 0.005

    mg = PandaScrewMpMotionGenerator(
        Np, Nc, Q, R, vel_bound, acc_bound, jerk_bound, sclerp=0.5
    )

    waypoints, ok = simulate_joint_waypoints(mg, q_initial, goal, dt=1e-3)

    assert ok
    assert len(waypoints) > 0
    assert len(waypoints) <= 1000
    np.testing.assert_array_equal(q_initial, waypoints[0])
    _goal = franka_kin.fkm(waypoints[-1])
    error = dq_pose_error(_goal, goal)
    assert np.linalg.norm(error.vec8()) < 0.005
