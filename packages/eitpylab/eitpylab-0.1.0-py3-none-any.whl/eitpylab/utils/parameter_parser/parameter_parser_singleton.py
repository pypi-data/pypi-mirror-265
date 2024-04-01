import os
from ruamel.yaml import YAML
from eitpylab.models.electral_properties_model import GeneralProperties
from eitpylab.models.fem_model import FemModel
from eitpylab.models.forward_problem_model import ForwardProblemModel


class ParameterMapper:
    """
    Class responsible for mapping parameter files to corresponding model objects.

    This class provides a static method to map parameter dictionaries to specific model instances based on the provided fileEnum.

    Attributes:
        None
    """

    @staticmethod
    def map_to_object(global_param, paramDict):
        """
        Map a parameter dictionary to a specific model object.

        :param fileEnum: (Parameters) An enumeration representing the type of parameter file.
        :param paramDict: (dict) A dictionary containing parameters for model initialization.

        :return: GeneralProperties or FemModel or ForwardProblemModel: An instance of the corresponding model.

        :raises ValueError: If the provided fileEnum is not implemented.
        """

        if global_param == 'FORWARD_PROBLEM':
            return ForwardProblemModel(**paramDict)
        if global_param == 'FEM_MODEL':
            return FemModel(**paramDict)
        if global_param == 'GENERAL':
            return GeneralProperties(**paramDict)
        raise ValueError("ERROR - File not implemented.")


class ParameterParserSingleton(YAML):
    """
    Singleton class for parsing and managing parameter files.

    This class follows the Singleton design pattern and is responsible for reading and managing parameter files.

    Attributes:
        parameters (dict): A dictionary to store mapped parameter objects.
    """

    parameters = {
        "GENERAL": None,
        "FEM_MODEL": None,
        "FORWARD_PROBLEM": None,
        "INVERSE_PROBLEM": None
    }

    def set_parameter(self, global_param, file_path):
        """
        Set the parameter for a given fileEnum.

        :param fileEnum: (Parameters) An enumeration representing the type of parameter file.
        :param file_path: (str) The path to the parameter file.

        :raises ValueError: If the file is not found or if there is an error while loading the parameters.
        """
        with open(file_path, "r") as params:
            try:
                self.parameters[global_param] = ParameterMapper.map_to_object(
                    global_param=global_param, paramDict=self.load(params)
                )
            except Exception as exc:
                raise exc

    def get_parameter(self, global_param):
        """
        Get the parameter object for a given global_param.

        :param global_param: (Parameters) An enumeration representing the type of parameter file.

        :return: GeneralProperties or FemModel or ForwardProblemModel: An instance of the corresponding model.

        :raises ValueError: If the specified parameter file is missing.
        """
        try:
            return self.parameters[global_param]
        except KeyError:
            raise ValueError("ERROR - Missing %s file." % global_param)
