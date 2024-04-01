from eitpylab.core.electral_properties.Current import Current
from eitpylab.core.electral_properties.Voltage import Voltage
from eitpylab.core.finite_element_model.finite_element_model import FiniteElementModel
from eitpylab.core.mesh_generator.mesh_generator import MeshGenerator
from eitpylab.core.observation_model.ObservationModel import ObservationModel
from eitpylab.models.electral_properties_model import GeneralProperties
from eitpylab.models.fem_model import FemModel
from eitpylab.models.forward_problem_model import ForwardProblemModel
from eitpylab.utils.os_path_pattern.os_path_pattern import set_absolute_path
from eitpylab.utils.parameter_parser.parameter_parser_singleton import ParameterParserSingleton


class GlobalEnviroment():
    def __init__(self, general, fem_model, forward_problem) -> None:
        super().__init__()

        self.parser = ParameterParserSingleton()

        self.general = set_absolute_path(general)
        self.fem_model = set_absolute_path(fem_model)
        self.forward_problem = set_absolute_path(forward_problem)

        self.__set_enviroment()

        self.general: GeneralProperties = self.parser.get_parameter(
            global_param='GENERAL')
        self.fem_model: FemModel = self.parser.get_parameter(
            global_param='FEM_MODEL')
        self.forward_problem: ForwardProblemModel = self.parser.get_parameter(
            global_param='FORWARD_PROBLEM')

        self.__set_current_props()
        self.__set_voltage_props()
        self.__set_mesh_file_props()
        self.__set_fem_model_props()
        self.__set_observation_model()

    def __set_enviroment(self):
        self.parser.set_parameter(
            global_param='GENERAL', file_path=self.general)
        self.parser.set_parameter(
            global_param='FORWARD_PROBLEM', file_path=self.forward_problem)
        self.parser.set_parameter(
            global_param='FEM_MODEL', file_path=self.fem_model)

    def __set_current_props(self):
        self.current_object = Current(current_object=self.general.current)

    def __set_voltage_props(self):
        self.voltage_object = Voltage(voltage_object=self.general.voltage)

    def __set_mesh_file_props(self):
        self.mesh_generator_object = MeshGenerator(path=self.fem_model.path)
        self.mesh_generator_object.open()

    def __set_fem_model_props(self):
        self.fem_model_object = FiniteElementModel(eit_general_props_object=self.general,
                                                   fem_model_object=self.fem_model,
                                                   forward_problem_object=self.forward_problem,
                                                   mesh_object=self.mesh_generator_object)

    def __set_observation_model(self):
        self.observation_model_object = ObservationModel(eit_general_props_object=self.general,
                                                         fem_model_object=self.fem_model,
                                                         forward_problem_object=self.forward_problem,
                                                         mesh_object=self.mesh_generator_object)
