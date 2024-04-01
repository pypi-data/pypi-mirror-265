from dataclasses import dataclass, field
from typing import List, TypeVar

@dataclass
class CurrentProperties(object):
    """
    Data class for representing current properties in an electrical system.

    Attributes:
        frequency (float): Frequency of the current.
        value (float): Magnitude of the current.
        unit (str): Unit of the current value.
        direction (str): Direction of the current.
        method (str): Method used for injecting current.
        skip (int): Number of steps to skip.
        injectionPairs (List[int]): List of injection pairs.

    """
    frequency: float
    value: float
    unit: str
    direction: str
    method: str
    skip: int
    injectionPairs: List[int]

@dataclass
class ReferenceVoltageNode(object):
    """
    Data class representing a reference voltage node in an electrical system.

    Attributes:
        method (str): Method used for obtaining the reference voltage node.
        node (List[float]): Coordinates of the reference voltage node.
        fixed_electrode_number (int): Number of the fixed electrode.
        node_number (int): Number of the reference voltage node.
        unit (str): Unit of the coordinates.

    """
    method: str
    coords: list[float]
    fixed_electrode_number: int
    node_number: int
    unit: str  
@dataclass
class VoltageProperties(object):
    """
    Data class representing voltage properties in an electrical system.

    Attributes:
        method (str): Method used for obtaining voltage properties.
        removeInjectingPair (bool): Whether to remove injecting pairs.
        direction (str): Direction of the voltage.
        skip (int): Number of steps to skip.
        referenceVoltageNode (ReferenceVoltageNode): Reference voltage node properties.

    """
    method: str
    removeInjectingPair: bool
    direction: str
    skip: int
    referenceVoltageNode: ReferenceVoltageNode
    
@dataclass
class GeneralProperties(object):
    """
    Data class representing overall electrical properties.

    Attributes:
        version (str): Version of the electrical properties.
        current (CurrentProperties): Current properties.
        voltage (VoltageProperties): Voltage properties.

    """
    version: str 
    current: CurrentProperties
    voltage: VoltageProperties
            