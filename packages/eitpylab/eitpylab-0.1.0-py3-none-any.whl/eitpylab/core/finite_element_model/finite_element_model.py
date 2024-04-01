import copy

from scipy import sparse as scipySparse
import numpy as np
import multiprocessing as mp

from eitpylab.core.finite_element_model.electrode_models.electrode_hua import CompleteElectrodeHua
from eitpylab.core.finite_element_model.parameters.uniform_rho_region import UniformRhoRegion
from eitpylab.core.finite_element_model.polygons.linear_tetrahedron import LinearTetrahedron
from eitpylab.core.finite_element_model.polygons.linear_triangle import LinearTriangle
from eitpylab.models.electral_properties_model import GeneralProperties
from eitpylab.models.fem_model import FemModel
from eitpylab.models.forward_problem_model import ForwardProblemModel
from eitpylab.utils.multiprocessing_cores import set_cores
from eitpylab.utils.rotation_matrix import rotMatrix
from eitpylab.utils.unit_converter.unit_converter import UnitConverter


unit_converter = UnitConverter()


def extract_COO(elem):
    tempKlocal_coo = scipySparse.coo_matrix(elem.Kgeom)
    nComponents = tempKlocal_coo.nnz

    # multiply by 1/rho
    if elem.propertiesDict['isElectrode']:
        tempKlocal_coo *= (1.0 / elem.rhoT)
    else:
        tempKlocal_coo *= (1.0 / elem.rho)

    # re-write row and col in terms of global node numbers
    row = elem.connectivity[tempKlocal_coo.row]
    col = elem.connectivity[tempKlocal_coo.col]
    val = tempKlocal_coo.data

    return [row, col, val]


class FiniteElementModel:
    def __init__(self, fem_model_object: FemModel,
                 eit_general_props_object: GeneralProperties,
                 mesh_object: object,
                 forward_problem_object: ForwardProblemModel) -> None:

        self.fem_model_object = fem_model_object
        self.eit_general_props_object = eit_general_props_object
        self.mesh_object = mesh_object
        self.forward_problem_object = forward_problem_object

        self.set_element_hight()
        self.set_node_coords()
        self.set_domain_regions()

        self.compute_k_global()

        self.setReferenceVoltageNode()

    # Setters and getters
    def set_element_hight(self):
        if self.fem_model_object.dimentions == 2:
            self.height_2d = unit_converter.to_metre(
                inputval=self.fem_model_object.heigthElement, inputUnit=self.fem_model_object.unit
            )
        else:
            self.height_2d = None

    def set_node_coords(self):
        self.node_coords = unit_converter.to_metre(
            inputUnit=self.fem_model_object.unit, inputVal=self.mesh_object.getNodes())
        self.has_rotation = False

        for option in self.fem_model_object.rotation:
            if option['active']:
                self.set_rotation_matrix()
                self.node_coords = self.set_mesh_rotation(coords=self.node_coords.T, is_inverse=False)

                self.has_rotation = True

    def set_domain_regions(self):
        self.domain_elements = []

        for region in self.fem_model_object.regions:
            label = region['label']
            tags = region['meshTag']
            is_grouped = region['isGrouped']
            dim = region['dimentions']
            rho = region['rho_0']
            
            print(f"Building region {label} with rho value: {rho}")

            for tag in tags:
                print(f"dim: {dim}, tag: {tag}")
                [elements, connectivities] = self.mesh_object.getElem(dim, tag)

                if is_grouped:
                    group_element = UniformRhoRegion(dimension=dim, connectivities=connectivities,
                                                    coords=self.node_coords, rho=rho,
                                                    height2D=self.height_2d, isSparse=False,
                                                    propertiesDict={'isElectrode': False, 'regionTag': tag, 'gmshElemNbr': elements})
                    self.domain_elements.append(group_element)
                else:
                    if dim == 2:
                        args = [(i + len(self.domain_elements), c, self.node_coords, rho, self.height_2d,
                                {'isElectrode': False, 'regionTag': tag, 'gmshElemNbr': elements[i]}) for i, c in enumerate(connectivities)]
                        with mp.Pool(processes=set_cores(limiter=1)) as p:
                            self.domain_elements += p.starmap(
                                LinearTriangle, args)

                    if dim == 3:
                        args = [(
                            i + len(self.domain_elements), c, self.node_coords, rho, {'isElectrode': False, 'regionTag': tag, 'gmshElemNbr': elements[i]})
                            for i, c in enumerate(connectivities)]
                        with mp.Pool(processes=set_cores(limiter=1)) as p:
                            self.domain_elements += p.starmap(
                                LinearTetrahedron, args)

        self.num_elements = len(self.domain_elements)
        print(f"Number of elements> {self.num_elements}")

        # also includes the virtual nodes of the electrodes
        self.num_nodes = self.node_coords.shape[0] + \
            self.fem_model_object.eletrodes['numberElectrodes']

        # electrodes
        tags = self.fem_model_object.eletrodes['meshTag']
        rho_t = self.fem_model_object.eletrodes['rho_t']

        self.electrodes_domain = []
        self.electrodes_nodes = []

        for tag in tags:
            if self.fem_model_object.dimentions == 2:
                # if dim=2D, electrodes are line elements, with 2 nodes
                [elements, connectivities] = self.mesh_object.getElem(1, tag)
            if self.fem_model_object.dimentions == 3:
                # if dim=3D, electrodes are triangle elements, with 3 nodes
                [elements, connectivities] = self.mesh_object.getElem(2, tag)

            self.electrodes_nodes.append(
                self.node_coords.shape[0] + len(self.electrodes_domain))

            electrode_elem = CompleteElectrodeHua(dimension=self.fem_model_object.dimentions,
                                                  elemNbr=len(
                                                      self.domain_elements),
                                                  connectivities=connectivities,
                                                  coords=self.node_coords,
                                                  rhoT=rho_t,
                                                  height2D=self.height_2d,
                                                  virtualNodeNbr=self.electrodes_nodes[-1],
                                                  isSparse=False,
                                                  propertiesDict={'isElectrode': True, 'regionTag': tag, 'gmshElemNbr': elements})

            self.electrodes_domain.append(electrode_elem)
            self.domain_elements.append(electrode_elem)

        # converts to numpy array
        self.electrode_nodes = np.array(self.electrodes_nodes)

    def set_rotation_matrix(self):
        self.rotation_matrix = []
        for rotation in self.fem_model_object.rotation:
            axis: str = rotation['axis'].lower()
            angle: int = rotation['angle_deg']*np.pi/180.0
            self.rotation_matrix.append(rotMatrix(axis=axis, angle_rad=angle))

    def set_mesh_rotation(self, coords, is_inverse):
        """
    apply stored rotations to a matrix of coordinates
        the first rotation is the first element of the list self.RotMat, and so on.
    Parameters
    ----------
    coords: numpy array
        coordinate matrix. This matrix must be 3xN .
    isInverse: bool
        if true, apply the inverse of the rotations .In this case, the transpose (=inverse) of the last element of self.RotMat is applied first.
    """
        self.set_rotation_matrix()
        temp = copy.copy(coords)
        if is_inverse:
            for mat in reversed(self.rotation_matrix):
                temp = np.matmul(mat.T, temp)
        else:
            for mat in self.rotation_matrix:
                temp = np.matmul(mat, temp)
        return temp

    def get_domain_elements(self):
        return [elem for elem in self.domain_elements if not elem.propertiesDict['isElectrode']]

    def get_mesh_limits(self):
        """
        Retuns the limits of the mesh.

        Returns
        -------
        listLimits: list of np arrays
            list of limits in the form   [ [minX, minY, min Z] , [maxX, maxY, maxZ] ]

        """
        minimum = np.min(self.node_coords, axis=0)
        maximum = np.max(self.node_coords, axis=0)
        return [minimum, maximum]

    def set_resistivities(self, elemNumbers, rhoVector):
        """
        set the resistivities of the elements

        Note: Remember that if a regionTag is configured to be grouped, then there is a single element that
        represent the entire region.

        Parameters
        ----------

        elemNumbers: iterable of ints
            elements to set the resitivity

        rhoVector: 1D numpy.array
            vector with resistivities, or electrode parameter (rho.t) in case of electrode elements
        """
        for (e, rho) in zip(elemNumbers, rhoVector):
            if self.domain_elementselements[e].propertiesDict['isElectrode']:
                self.domain_elementselements[e].setRhoT(rho)
            else:
                self.domain_elementselements[e].setRho(rho)

    def get_elements_by_mesh_tag(self, meshTagList):
        """
        return a list of elements with the given meshTag

        Parameters
        ----------
        meshTagList: list of int
            meshTags of the regions

        Returns
        -------
        listElem: list
            list of elements

        """
        listElem = []
        for elem in self.domain_elements:
            if elem.propertiesDict['regionTag'] in meshTagList:
                listElem.append(elem)
        return listElem

    def get_elements_by_element_number(self, elementNbrList):
        """
        return a list of elements with the given meshTag

        Parameters
        ----------
        elementNbrList: list of int
            number of the elements

        Returns
        -------
        listElem: list
            list of elements

        """
        return [self.domain_elements[e] for e in elementNbrList]

    # K global builder

    def compute_k_global(self):
        try:
            del self.KglobalSp
        except AttributeError:
            pass

        print('-> Building FEM global matrix...')

        # extract COO information in parallel
        args = [(e,) for e in self.domain_elements]
        with mp.Pool(processes=set_cores(limiter=1)) as p:
            dataList = p.starmap(extract_COO, args)

        # find the total number of non zero elements in all local matrices
        size = 0
        for data in dataList:
            size += len(data[0])

        rows = np.empty(size, dtype=int)
        cols = np.empty(size, dtype=int)
        vals = np.empty(size)

        pos = 0
        for data in dataList:
            nComponents = len(data[0])

            # re-write row and col in terms of global node numbers
            rows[pos:pos + nComponents] = data[0]
            cols[pos:pos + nComponents] = data[1]
            vals[pos:pos + nComponents] = data[2]
            pos += nComponents

        # Saves sparse kglobal
        self.KglobalSp = scipySparse.coo_matrix(
            (vals, (rows, cols)), shape=(self.num_nodes, self.num_nodes)).tocsr()
        
         # Saves dense kglobal
        self.KglobalDense = scipySparse.coo_matrix(
            (vals, (rows, cols)), shape=(self.num_nodes, self.num_nodes)).todense()

    def setReferenceVoltageNode(self):
        """
        set the reference node for the measurements
        """
        ref_votage_params = self.eit_general_props_object.voltage['referenceVoltageNode']

        method = ref_votage_params['method']
        

        if method == 'fixed_electrode':
            electrdeNbr = ref_votage_params['fixed_electrode_number']
            # subtracts 1 because electrode numbers start with 0 in the code.
            self.voltageRefNode = self.electrode_nodes[electrdeNbr - 1]

        if method == 'origin':
            nodeDists = np.sum(self.node_coords * self.node_coords, axis=1)
            self.voltageRefNode = np.argmin(nodeDists)

        if method == 'nodeNbr':
            customNode = ref_votage_params['node_number']
            # subtracts 1 because node numbers start with 0 in the code.
            self.voltageRefNode = customNode - 1

        if method == 'coords':
            print(f"Choosed method: {method}")
            coords = np.array(ref_votage_params['coords'])
            coordsUnit = ref_votage_params['unit']
            coords = unit_converter.to_metre(inputUnit=coordsUnit, inputVal=coords)

            coords = self.set_mesh_rotation(is_inverse=False, coords=coords)

            nodeDists = np.sum((self.node_coords - coords) ** 2, axis=1)
            
            self.voltageRefNode = np.argmin(nodeDists)

        
        self.KglobalSp[self.voltageRefNode, :] = 0
        self.KglobalSp[:, self.voltageRefNode] = 0
        self.KglobalSp[self.voltageRefNode, self.voltageRefNode] = 1.0
        
        self.KglobalDense[self.voltageRefNode, :] = 0
        self.KglobalDense[:, self.voltageRefNode] = 0
        self.KglobalDense[self.voltageRefNode, self.voltageRefNode] = 1.0

    def get_k_global(self):
        return self.KglobalDense