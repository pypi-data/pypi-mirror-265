from enum import Enum

class VoltageEnum(Enum):
    """
    Enumeration class for representing voltage-related parameters.

    This enum class defines constants for different parameters related to the voltage setup in electrical impedance tomography.

    Attributes:
        METHOD (str): Represents the method used in the voltage setup.
        DIRECTION (str): Represents the direction of the voltage.
        SKIP (str): Represents the skip value in the voltage setup.
        REFERENCE_NODE (str): Represents the reference node in the voltage setup.
    """

    METHOD = 'METHOD'
    DIRECTION = 'DIRECTION'
    SKIP = 'SKIP'
    REFERENCE_NODE = 'REFERENCE_NODE'
