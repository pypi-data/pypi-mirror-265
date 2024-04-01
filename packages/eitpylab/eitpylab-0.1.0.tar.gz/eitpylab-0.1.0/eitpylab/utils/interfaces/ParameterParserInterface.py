from abc import ABC, abstractmethod

class ParameterParserInterface(ABC):
    """
    Abstract base class for parameter parsers.

    This class defines the interface for creating parameters.

    Methods:
        create_parameters() -> None:
            Abstract method to be implemented by subclasses. It is responsible for creating and handling parameters.
    """
    
    @abstractmethod
    def create_parameters(self):
        """
        Abstract method to be implemented by subclasses.

        This method is responsible for creating and handling parameters.

        Returns:
            None
        """
        pass