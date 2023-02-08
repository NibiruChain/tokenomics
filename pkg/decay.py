from numbers import Real
from typing import Union
import numpy as np


class ExponentialDecay:
    @staticmethod
    def calc_amt_start(
        amt_final: Real, decay_factor: Real, time: Real
    ) -> Union[Real, np.ndarray]:
        decay_term = (1 - decay_factor) ** time
        return amt_final / decay_term

    @staticmethod
    def calc_amt_final(
        amt_start: Real, decay_factor: Real, time: Real
    ) -> Union[Real, np.ndarray]:
        decay_term = (1 - decay_factor) ** time
        return amt_start * decay_term
    
    @classmethod
    def decay_amts(cls, amt_start: Real, decay_factor: Real, times: np.ndarray) -> np.ndarray: 
        return cls.calc_amt_final(amt_start=amt_start, decay_factor=decay_factor, time=times)


