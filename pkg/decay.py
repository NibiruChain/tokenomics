from numbers import Real
from typing import Union
import numpy as np


class ExponentialDecay:
    """Utility class for computing values in an exponential decay."""
    @staticmethod
    def calc_amt_start(
        amt_final: Real, decay_factor: Real, time: Real
    ) -> Union[Real, np.ndarray]:
        """Compute the initial target value required for the exponential decay
        to reach "amt_final" with the given "decay_factor" and "time".
        """
        decay_term = (1 - decay_factor) ** time
        return amt_final / decay_term

    @staticmethod
    def calc_amt_final(
        amt_start: Real, decay_factor: Real, time: Union[Real, np.ndarray]
    ) -> np.ndarray:
        """Compute the target value at some time or an array of target values
        given an array of times.
        """
        decay_term = (1 - decay_factor) ** time
        amt_final = amt_start * decay_term
        if not isinstance(amt_final, np.ndarray):
            return np.array(amt_final)
        return amt_final

    @classmethod
    def decay_amts(
        cls, amt_start: Real, decay_factor: Real, times: np.ndarray
    ) -> np.ndarray:
        """Compute the exponential decay as a function of time given the
        "decay_factor" and initial value ("amt_start").
        """
        return cls.calc_amt_final(
            amt_start=amt_start, decay_factor=decay_factor, time=times
        )
