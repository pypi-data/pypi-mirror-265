class Current:
    """
    Class representing the current setup for electrical impedance tomography.

    This class is responsible for handling the current setup, including methods for setting and retrieving current GlobalVariable.

    Attributes:
        current_setup (dict): A dictionary to store current setup GlobalVariable.
    """


    def __init__(self, current_object) -> None:
        """
        Initialize the Current class.

        Retrieves the general GlobalVariable related to electrical properties and initializes the current setup.

        :return: None
        """
        self.GLOBAL_CURRENT_INPUT = current_object
        
        self.frequency = self.GLOBAL_CURRENT_INPUT['frequency']
        self.method = self.GLOBAL_CURRENT_INPUT['method']
        self.direction = self.GLOBAL_CURRENT_INPUT['direction']
        self.value = self.GLOBAL_CURRENT_INPUT['value']
        self.injection_pairs = self.GLOBAL_CURRENT_INPUT['injectionPairs']
   
    def set_current_skip_method(self):
        """
        Set the current skip method based on the current setup.

        :return: None

        :raises ValueError: If the current pattern type is not recognized.
        """

        if self.method not in [
            "bipolar_skip_full",
            "bipolar_pairs",
        ]:
            print(
                "ERROR: Current pattern type not recognized: %s"
                % self.current["method"]
            )
            return

        if self.method == "bipolar_skip_full":
            self.skip = self.GLOBAL_CURRENT_INPUT["skip"]

        if self.method == "bipolar_pairs":
            # subtracts 1 because electrode numbers start from 0
            self.skip = self.GLOBAL_CURRENT_INPUT["skip"] - 1

    def set_current_value(self):
        """
        Set the current value in the current setup.

        :return: None
        """
        if self.GLOBAL_CURRENT_INPUT["unit"] == "mA":
            self.value_amperes = (
                self.current["value"] * 0.001
            )
        else:
            self.value_amperes = float(
                self.current["value"]
            )

