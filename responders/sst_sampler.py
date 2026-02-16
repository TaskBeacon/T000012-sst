from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from psyflow.sim.contracts import Action, Observation, SessionInfo


@dataclass
class SSTSamplerResponder:
    key_left: str = "f"
    key_right: str = "j"
    p_hit_go: float = 0.9
    p_fail_stop: float = 0.5
    rt_go_mean_s: float = 0.32
    rt_go_sd_s: float = 0.05
    rt_min_s: float = 0.12

    def __post_init__(self) -> None:
        self._rng: Any = None
        self.p_hit_go = max(0.0, min(1.0, float(self.p_hit_go)))
        self.p_fail_stop = max(0.0, min(1.0, float(self.p_fail_stop)))
        self.rt_go_mean_s = float(self.rt_go_mean_s)
        self.rt_go_sd_s = max(1e-6, float(self.rt_go_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Any) -> None:
        return None

    def end_session(self) -> None:
        return None

    def _sample_rt(self) -> float:
        return max(self.rt_min_s, float(self._rng.normal(self.rt_go_mean_s, self.rt_go_sd_s)))

    def act(self, obs: Observation) -> Action:
        valid_keys = list(obs.valid_keys or [])
        if not valid_keys or self._rng is None:
            return Action(key=None, rt_s=None, meta={"source": "sst_sampler", "reason": "unavailable"})

        condition = str(obs.condition_id or "").lower()
        if condition.startswith("go_"):
            if float(self._rng.random()) > self.p_hit_go:
                return Action(key=None, rt_s=None, meta={"source": "sst_sampler", "outcome": "go_miss"})
            key = self.key_left if condition.endswith("left") else self.key_right
            if key not in valid_keys:
                key = valid_keys[0]
            return Action(key=key, rt_s=self._sample_rt(), meta={"source": "sst_sampler", "outcome": "go_hit"})

        if condition.startswith("stop_"):
            if float(self._rng.random()) < self.p_fail_stop:
                key = self.key_left if condition.endswith("left") else self.key_right
                if key not in valid_keys:
                    key = valid_keys[0]
                return Action(key=key, rt_s=self._sample_rt(), meta={"source": "sst_sampler", "outcome": "stop_fail"})
            return Action(key=None, rt_s=None, meta={"source": "sst_sampler", "outcome": "stop_success"})

        return Action(key=None, rt_s=None, meta={"source": "sst_sampler", "outcome": "unknown_condition"})
