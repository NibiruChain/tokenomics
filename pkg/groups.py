import dataclasses
import enum
import abc
import numpy as np


class Group(enum.Enum):
    PRIVATE = "Private"
    TEAM = "Team"
    COMMUNITY = "Community"


@dataclasses.dataclass
class Subgroup(abc.ABC):
    group: Group
    supply_pct: float

    @property
    def group_pct(self) -> float:
        ...

    @abc.abstractmethod
    def schedule(self) -> np.ndarray:

        [0, 0, 0, 0, 1, 1, 23, 2, ...]


MONTH = 1
YEAR = 12 * MONTH

TOTAL_TIME_MONTHS = 8 * YEAR


# ALL of private has the same schedule? OR only seed? 1 yr cliff, 3 year vest
# Team -> 1 yr cliff, 3 year vest
