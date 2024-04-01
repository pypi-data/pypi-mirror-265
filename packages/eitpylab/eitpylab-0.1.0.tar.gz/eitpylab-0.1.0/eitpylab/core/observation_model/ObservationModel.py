
import os
import shutil
import numpy as np
import scipy
from eitpylab.core.finite_element_model.finite_element_model import FiniteElementModel
from eitpylab.models.electral_properties_model import GeneralProperties
from eitpylab.models.fem_model import FemModel
from eitpylab.models.forward_problem_model import ForwardProblemModel

from eitpylab.utils.unit_converter.unit_converter import UnitConverter


class ObservationModel(FiniteElementModel):
    """
    Class: ObservationModel

    Inherits from FemModeling class.

    This class represents the observation model used in the EIT system. It extends the functionality provided by the FemModeling class.

    Attributes:
        None

    Methods:
        __init__(): Initializes an ObservationModel object.
        bipolar_pairs(): Sets the current matrix using the bipolar pairs method.
        bipolar_skip_full(): Sets the current matrix using the bipolar skip full method.
        set_current_matrix(): Sets the current matrix based on the specified current method.
        set_nodal_voltages(): Sets the nodal voltages based on the current matrix and the global stiffness matrix.

    """

    def __init__(self, fem_model_object: FemModel, eit_general_props_object: GeneralProperties, mesh_object: object, forward_problem_object: ForwardProblemModel) -> None:
        super().__init__(fem_model_object, eit_general_props_object,
                         mesh_object, forward_problem_object)

        self.fem_model_object = fem_model_object
        self.eit_general_props_object = eit_general_props_object
        self.mesh_object = mesh_object
        self.forward_problem_object = forward_problem_object

        self.num_electrodes = self.forward_problem_object.numberElectrodes
        self.electrodes_nodes = self.electrode_nodes

        self.curr_direction = self.eit_general_props_object.current['direction']
        self.curr_method = self.eit_general_props_object.current['method']
        self.curr_value = UnitConverter.to_metre(
            self.eit_general_props_object.current['value'], 'mm')
        self.curr_skip = self.eit_general_props_object.current['skip']
        self.injection_pairs = self.eit_general_props_object.current['injectionPairs']

        self.num_currents = len(self.injection_pairs)

        # self.reference_voltage_node = self.eit_general_props_object.voltage[
        #     'referenceVoltageNode']['node_number']
        self.voltage_method = self.eit_general_props_object.voltage[
            'referenceVoltageNode']['method']
        self.measurement_pairs = np.zeros((self.num_electrodes, 2), dtype=int)

        self.single_ended_to_differential_matrix()

        self.set_measure_weight_matrix()

        self.set_current_matrix()

        self.set_nodal_voltage()

        self.set_electrode_voltages(
            append=False, singleEnded=False, fileName='./teste.txt')

    def bipolar_pairs(self):
        """
        Sets the current matrix using the bipolar pairs method.

        Sets the current matrix based on the bipolar pairs method and the specified current parameters.
        """
        self.current_matrix = np.zeros((self.num_nodes, self.num_electrodes))
        self.injection_pairs = np.zeros((self.num_electrodes, 2), dtype=int)

        for i, pair in enumerate(self.injection_pairs):
            print(pair)
            if self.curr_direction == '+-':
                currPos, currNeg = pair
            else:
                currNeg, currPos = pair

            self.current_matrix[int(
                self.electrodes_nodes[currPos]), i] = self.curr_value
            self.current_matrix[int(
                self.electrodes_nodes[currNeg]), i] = -self.curr_value

    def bipolar_skip_full(self):
        """
        Sets the current matrix using the bipolar skip full method.

        Sets the current matrix based on the bipolar skip full method and the specified current parameters.
        """
        self.current_matrix = np.zeros((self.num_nodes, self.num_electrodes))
        self.injection_pairs = np.zeros((self.num_electrodes, 2), dtype=int)

        for i in range(self.num_electrodes):
            if self.curr_direction == '+-':
                curr_pos = i
                curr_neg = (i + self.curr_skip + 1) % self.num_electrodes
            else:
                curr_pos = (i + self.curr_skip + 1) % self.num_electrodes
                curr_neg = i

            self.injection_pairs[i] = np.array([curr_pos, curr_neg])

            self.current_matrix[self.electrode_nodes[curr_pos],
                                i] = self.curr_value
            self.current_matrix[self.electrode_nodes[curr_neg],
                                i] = -self.curr_value

    def set_current_matrix(self):
        print("\n-> Calculating current matrix")
        """
        Sets the current matrix.

        Sets the current matrix based on the specified current method.
        """

        print(self.curr_method)

        if self.curr_method == 'bipolar_skip_full':
            self.bipolar_skip_full()

        if self.curr_method == 'bipolar_pairs':
            self.bipolar_pairs()

        # set the elements of the reference voltage node to zero.
        self.current_matrix[self.voltageRefNode, :] = 0

    def set_measure_weight_matrix(self):
        """
        Find active measurements. defines the number of measurements per injection pair
        """
        matrix = np.ones([self.num_currents, self.num_electrodes])

        if self.eit_general_props_object.voltage['removeInjectingPair']:
            if self.eit_general_props_object.voltage['skip'] == 'single_ended':
                for i, pair in enumerate(self.injection_pairs):
                    matrix[i, pair] = 0.0

            if self.eit_general_props_object.voltage['skip'] == 'differential_skip':
                for i, currPair in enumerate(self.injection_pairs):
                    c1, c2 = currPair

                    # find measurements that involve electrode c1
                    rows2, _ = np.where(self.measurement_pairs == c2)
                    rows1, _ = np.where(self.measurement_pairs == c1)

                    matrix[i, rows1] = 0.0
                    matrix[i, rows2] = 0.0

        self.measure_weight_matrix = matrix.flatten('C')

        self.active_measurement_positions = np.where(
            self.measure_weight_matrix > 0)[0]

    def single_ended_to_differential_matrix(self):
        """
        computes the matrix that converts single-ended to differential measurements, following the
        information provided in the .conf file.
        """
        self.se2diffMatrix = np.zeros(
            (self.num_electrodes, self.num_electrodes), dtype=float)
        self.measurementPairs = np.zeros((self.num_electrodes, 2), dtype=int)

        if self.eit_general_props_object.voltage['method'] == 'differential_skip':
            for i in range(self.num_electrodes):
                if self.eit_general_props_object.voltage['direction'] == '+-':
                    voltPos = i
                    voltNeg = (
                        i + self.eit_general_props_object.voltage['skip'] + 1) % self.num_electrodes
                else:
                    voltPos = (
                        i + self.eit_general_props_object.voltage['skip'] + 1) % self.num_electrodes
                    voltNeg = i

                # measurements
                self.measurementPairs[i] = np.array([voltPos, voltNeg])
                self.se2diffMatrix[i, voltPos] = 1
                self.se2diffMatrix[i, voltNeg] = -1

    def set_nodal_voltage(self):
        self.nodal_voltages = scipy.linalg.solve(
            self.KglobalDense, self.current_matrix, assume_a='pos', check_finite=False)

    def set_electrode_voltages(self, fileName=None, append=False, singleEnded=False):
        """
        solves the forward problem using sparse version of the FEM matrix.

        Parameters
        ----------
        fileName: str, optional
            output file name. If None (default), then no file is saved

        append: bool
            append file. If 'False' the file is overwritten

        singleEnded : bool
            If true, the results will be single ended with respect to the reference node. if False, then the result
            will follow the configuration of the .conf file.

        Returns
        -------
        measurements : 1d numpy array
            electrode voltages of all current patterns. Thsi vector contains measurements of active electrodes only

        """

        # nodalVoltages = self.KglobalPardiso.solve(self.currMatrix)

        # dense Kglobal matrix
        # nodalVoltages = scipyLinalg.solve(self.femMesh.Kglobal, self.currMatrix, assume_a='pos', check_finite=False)

        # extract measurements from electrodes virtual nodes
        electrodeVoltages = self.nodal_voltages[self.electrode_nodes, :]

        if not singleEnded and self.voltage_method == 'differential_skip':
            electrodeVoltages = np.matmul(
                self.se2diffMatrix, electrodeVoltages)

        # vectorize array columnwise
        electrodeVoltages = electrodeVoltages.flatten('F')

        # extracts only valid measurement electrode
        electrodeVoltages = electrodeVoltages[self.active_measurement_positions]

        if fileName is not None:
            if append:
                with open(fileName, 'ab') as f:
                    np.savetxt(f, electrodeVoltages.reshape(
                        1, electrodeVoltages.shape[0]))
            else:
                with open(fileName, 'w') as f:
                    f.write('# headerSize=%d\n' % 8)
                    f.write('# nElectrodes=%d\n' % self.num_electrodes)
                    f.write('# nInjections=%d\n' % self.num_currents)
                    f.write('# currentPattern=%s\n' % self.curr_method)
                    f.write('# voltagePattern=%s\n' % self.voltage_method)
                    f.write('# currentValue_A=%f\n' % self.curr_value)
                    f.write('# ignoreInjectingElectrodes=%s\n' %
                            self.eit_general_props_object.voltage['removeInjectingPair'])
                    f.write('# measurementArray=')

                with open(fileName, 'ab') as f:
                    np.savetxt(f, self.measure_weight_matrix >
                               0, fmt='%d', newline=' ')
                    f.write(bytes('\n', 'utf8'))
                    np.savetxt(f, electrodeVoltages.reshape(
                        1, electrodeVoltages.shape[0]), fmt='%s')

        self.electrode_voltages = electrodeVoltages


