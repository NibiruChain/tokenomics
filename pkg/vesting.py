import numpy as np
from dataclasses import dataclass as struct
from .const import TOKEN_SUPPLY_YEARS, SUPPLY_AT_MATURITY


@struct
class VestingInfo:
    cliff_pct: float
    vest_start_month: int
    vest_end_month: int

    def months_vesting(self) -> int:
        return self.vest_end_month - self.vest_start_month

    def months_before_vest(self) -> int:
        return self.vest_start_month

    def months_after_vest(self) -> int:
        return (TOKEN_SUPPLY_YEARS * 12) - self.vest_end_month

    def distrib_vec(
        self,
        group_pct: float,
        num_time_points: int = int(1e5),
    ) -> np.ndarray:
        token_supply_months = (TOKEN_SUPPLY_YEARS * 12)
        supply_start = SUPPLY_AT_MATURITY * group_pct * self.cliff_pct
        supply_end = SUPPLY_AT_MATURITY * group_pct
        head = np.linspace(
            start=supply_start,
            stop=supply_end,
            num=num_time_points * self.months_vesting() // token_supply_months,
        )
        years_before_vest = self.months_before_vest()
        if years_before_vest > 0:
            zeros_before_head = np.zeros(
                num_time_points * self.months_before_vest() // token_supply_months, dtype=float,
            )
            head = np.concatenate([zeros_before_head, head])

        ones_tail = np.ones(
            num_time_points * self.months_after_vest() // token_supply_months, dtype=float)

        return np.concatenate(
            [head, ones_tail * head[-1]]
        )
