import gym
import numpy as np
import genesis as gs
from quadcopter_controller import DronePIDController
from gym import spaces

class DroneEnv(gym.Env):
    def __init__(self):
        super().__init__()

        gs.init(backend=gs.gpu)
        self.scene = gs.Scene(show_viewer=False, sim_options=gs.options.SimOptions(dt=0.01))
        self.plane = self.scene.add_entity(morph=gs.morphs.Plane())
        self.drone = self.scene.add_entity(morph=gs.morphs.Drone(file="urdf/drones/cf2x.urdf", pos=(0, 0, 0.2)))

        pid_params = [
            [2.0, 0.0, 0.0], [2.0, 0.0, 0.0], [2.0, 0.0, 0.0],
            [20.0, 0.0, 20.0], [20.0, 0.0, 20.0], [25.0, 0.0, 20.0],
            [10.0, 0.0, 1.0], [10.0, 0.0, 1.0], [2.0, 0.0, 0.2],
        ]
        self.controller = DronePIDController(self.drone, dt=0.01, base_rpm=14468.429, pid_params=pid_params)

        self.scene.build()

        # 目標点はリセット時に更新
        self.target = np.array([1.0, 1.0, 1.5])
        self.t = 0
        self.max_steps = 500

        self.observation_space = spaces.Box(low=-10, high=10, shape=(9,), dtype=np.float32)
        self.action_space = spaces.Box(low=-1, high=1, shape=(4,), dtype=np.float32)

    def reset(self):
        self.drone.set_pos((0, 0, 0.2))
        self.target = np.array([1.0, 1.0, 1.5])  # 指定旋回パターン先の点
        self.t = 0
        return self._get_obs()

    def step(self, action):
        # action: roll, pitch, yaw, thrust のデルタ
        base_rpm = 14468.429
        roll, pitch, yaw, thrust = action

        rpms = base_rpm + np.array([
            thrust - roll - pitch - yaw,
            thrust - roll + pitch + yaw,
            thrust + roll + pitch - yaw,
            thrust + roll - pitch + yaw,
        ]) * 1000.0  # scale

        self.drone.set_propellels_rpm(rpms)
        self.scene.step()

        obs = self._get_obs()
        reward = self._compute_reward()
        done = self.t >= self.max_steps

        self.t += 1
        return obs, reward, done, {}

    def _get_obs(self):
        pos = self.drone.get_pos().cpu().numpy()
        vel = self.drone.get_vel().cpu().numpy()
        att = self.drone.get_quat().cpu().numpy()  # Quaternion
        return np.concatenate([pos, vel])[:9]  # 位置+速度（簡易化）

    def _compute_reward(self):
        pos = self.drone.get_pos().cpu().numpy()
        dist = np.linalg.norm(pos - self.target)
        reward = -dist  # 距離が近いほど高報酬
        return reward
