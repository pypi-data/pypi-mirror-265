from eitpylab.core.finite_element_model.parameters.uniform_rho_simplex import UniformRhoSimplex

import numpy as np
from scipy import linalg as scipyLinalg

class LinearTriangle(UniformRhoSimplex):
    """
    3-node Linear triangle element with uniform resistivity/conductivity.

    This class represents a 3-node linear triangle element used in finite element modeling. It inherits from
    `UniformRhoSimplex` and includes additional methods specific to the linear triangle element.

    Attributes:
        None

    Methods:
        __init__(elemNbr, connectivity, coords, rho, height2D=1.0, propertiesDict=None):
            Initializes the LinearTriangle instance.

    """

    def __init__(self, elemNbr,  # type: int
                 connectivity,  # type: Array[int]
                 coords,  # type: Array[float]
                 rho,  # type float
                 height2D=1.0,  # type: float
                 propertiesDict=None  # type: dict
                 ):
        """
        Initializes the LinearTriangle instance.

        Parameters:
            elemNbr (int): Number of the element.
            connectivity (numpy.ndarray): Nodes of the element in global terms. The local order of the nodes will be
                the same as the connectivity input.
            coords (numpy.ndarray): 2D array where each line is composed of 3 columns (X, Y, and Z) of the node.
                This matrix should contain all nodes of the FemModel, and the function will extract only the needed lines.
            rho (float): Resistivity of the element.
            height2D (float, optional): Associated height of the triangular element. Default is 1.0.
            propertiesDict (dict, optional): Dictionary containing the properties of the simplex.

        Returns:
            None
        """
        
        dimension = 2
        super().__init__(elemNbr, dimension, connectivity, coords, rho, False, propertiesDict)
        self.type = '3-node triangle, linear'.lower()
        self.height2D = height2D
        self.area = self.calcSimplexVolume()
        self._calc_localKgeom()

    def _calc_localKgeom(self):
        """
        Compute the geometric component of the local stiffness matrix.
        """
        
        # passing the vectors to a local system of coordinates such that
        # e_1 and e_2 are contained the plane of the triangle
        v2 = self.coords[1, :] - self.coords[0, :]
        v3 = self.coords[2, :] - self.coords[0, :]
        v1local = np.array([0, 0])
        [v2local, v3local] = self.localRefSystem2D(v2, v3)

        M = np.ones([3, 3])
        M[:, 1:] = np.vstack([v1local, v2local, v3local])

        F = scipyLinalg.inv(M)[1:, :]

        # does not need to divide by (2xArea)^2 bc I am inverting M directly
        self.Kgeom = self.height2D * self.area * np.dot(F.T, F)

