from enum import Enum
from typing import Union

class CurrentEnum(Enum):
    """
    Enumeration class for representing current-related parameters.

    This enum class defines constants for different parameters related to the current setup in electrical impedance tomography.

    Attributes:
        METHOD (str): Represents the method used in the current setup.
        VALUE_AMPERS (str): Represents the value of the current in amperes.
        SKIP (str): Represents the skip value in the current setup.
    """

    METHOD = 'METHOD'
    VALUE_AMPERS = 'VALUE_AMPERS'
    SKIP = 'SKIP'
