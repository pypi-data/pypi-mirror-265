class Voltage:
    """
    Class representing the voltage setup for electrical impedance tomography.

    This class is responsible for handling the voltage setup, including methods for setting and retrieving voltage GlobalVariable.

    Attributes:
        voltage_setup (dict): A dictionary to store voltage setup GlobalVariable.
    """

    voltage_setup = {}

    def __init__(self, voltage_object) -> None:
        """
        Initialize the Voltage class.

        Retrieves the general GlobalVariable related to electrical properties and initializes the voltage setup.

        :return: None
        """
        self.GLOBAL_VOLTAGE_INPUT = voltage_object
        
        self.method = self.GLOBAL_VOLTAGE_INPUT['method']
        
        self.set_voltage_pattern()
        

    def set_voltage_pattern(self):
        """
        Set the voltage pattern based on the voltage setup.

        :return: None

        :raises ValueError: If the voltage pattern type is not recognized.
        """
        if self.method not in ["single_ended", "differential_skip"]:
            print("ERROR: Voltage pattern type not recognized: %s" % self.method)
            return

        if self.method == "differential_skip":
            self.direction = self.GLOBAL_VOLTAGE_INPUT['direction']
            self.skip = self.GLOBAL_VOLTAGE_INPUT['skip']

