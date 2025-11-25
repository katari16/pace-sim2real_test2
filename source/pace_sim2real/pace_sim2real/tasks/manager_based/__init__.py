import gymnasium as gym  # noqa: F401

gym.register(
    id="Isaac-Pace-Anymal-D-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.pace_sim2real.anymal_pace_env_cfg:AnymalDPaceEnvCfg"
    },
)
