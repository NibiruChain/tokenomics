from numbers import Real
from typing import Union
import numpy as np


class ExponentialDecay:
    @staticmethod
    def calc_amt_start(
        amt_final: Real, decay_rate: Real, time: Real
    ) -> Union[Real, np.ndarray]:
        decay_term = (1 - decay_rate) ** time
        return amt_final / decay_term

    @staticmethod
    def calc_amt_final(
        amt_start: Real, decay_rate: Real, times: np.ndarray
    ) -> np.ndarray:
        decay_term = (1 - decay_rate) ** times
        return amt_start * decay_term

    @staticmethod
    def decay_amts(amt_start: Real, decay_rate: Real, times: np.ndarray) -> np.ndarray:
        print(f"amt_start: {amt_start}")
        print(f"decay_factor: {decay_rate}")
        print(f"times: {times}")
        result = ExponentialDecay.calc_amt_final(
            amt_start=amt_start, decay_rate=decay_rate, times=times
        )
        print(f"result: {result}")
        return result
