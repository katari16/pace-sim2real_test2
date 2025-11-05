from isaaclab.utils import configclass

# from isaaclab.envs import ManagerBasedRLEnvCfg
from isaaclab_tasks.manager_based.locomotion.velocity.velocity_env_cfg import LocomotionVelocityRoughEnvCfg


from isaaclab_assets.robots.anymal import ANYMAL_D_CFG
from isaaclab.assets import ArticulationCfg
from isaaclab.actuators import DCMotorCfg
from pace_sim2real.utils.pace_actuator_cfg import PaceDCMotorCfg


ANYDRIVE_3_SIMPLE_ACTUATOR_CFG = PaceDCMotorCfg(
    joint_names_expr=[".*HAA", ".*HFE", ".*KFE"],
    saturation_effort=140.0,
    effort_limit=89.0,
    velocity_limit=8.5,
    stiffness={".*": 85.0},
    damping={".*": 0.6},
    encoder_bias=[0.0] * 12,
    max_delay=10,
)


@configclass
class AnymalDPaceEnvCfg(LocomotionVelocityRoughEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # switch robot to anymal-d
        self.scene.robot = ANYMAL_D_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot", init_state=ArticulationCfg.InitialStateCfg(pos=(0.0, 0.0, 2.0)),
                                                actuators={"legs": ANYDRIVE_3_SIMPLE_ACTUATOR_CFG})

        # fix in air
        self.scene.robot.spawn.articulation_props.fix_root_link = True
        self.sim.dt = 0.0025  # 400Hz simulation
        self.decimation = 1  # 400Hz control
        self.episode_length_s = 9999.0  # long episodes
        self.actions.joint_pos.scale = 1.0  # makes actions = impedance control
        self.viewer.lookat = (0.0, 0.0, 2.0)
        self.viewer.eye = (2.0, 2.0, 3.0)

        # change terrain to flat
        self.scene.terrain.terrain_type = "plane"
        self.scene.terrain.terrain_generator = None
        # disable randomization for play
        self.observations.policy.enable_corruption = False
        # remove random pushing event
        self.events.base_external_force_torque = None
        self.events.push_robot = None
        # no terrain curriculum
        self.curriculum.terrain_levels = None
