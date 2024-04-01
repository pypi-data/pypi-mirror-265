from scipy import linalg as scipyLinalg

import numpy as np

from eitpylab.core.finite_element_model.parameters.uniform_rho_region import UniformRhoRegion


class CoreElectrodeHua:
    """
    Core component of Hua's complete electrode model.

    This class represents the core component of Hua's electrode model, handling 2D and 3D geometries.

    Attributes:
        number (int): Number of the element.
        dim (int): Dimension of the model (2 or 3).
        type (str): Type of the core electrode model.
        connectivity (numpy.ndarray): Nodes of the element in global terms.
        coords (numpy.ndarray): Coordinates of nodes in the FemModel.
        centroid (numpy.ndarray): Centroid of the core electrode.
        isSparse (bool): Flag indicating whether the local matrix is sparse.
        isRegion (bool): Flag indicating whether the core electrode is part of a region.
        nNodes (int): Number of nodes in the core electrode.
        height2D (float): Associated height of the triangular element (used only if dim=2).
        propertiesDict (dict): Dictionary containing the properties of the core electrode.
        rhoT (float): Electrode parameter [rho*t] from Hua's model.
        Kgeom (numpy.ndarray): Geometric component of the local stiffness matrix.

    """

    def __init__(
        self,
        dimension,  
        elemNbr,  
        connectivity,  
        coords,  
        rhoT, 
        height2D=1.0,  
        propertiesDict=None,  
    ):
        """
        Initialize the CoreElectrodeHua instance.

        Parameters:
            dimension (int): Dimension of the model (2 or 3).
            elemNbr (int): Number of the element.
            connectivity (numpy.ndarray): Nodes of the element in global terms.
            coords (numpy.ndarray): Coordinates of nodes in the FemModel.
            rhoT (float): Electrode parameter [rho*t] from Hua's model.
            height2D (float): Associated height of the triangular element (used only if dim=2).
            propertiesDict (dict): Dictionary containing the properties of the core electrode.

        Returns:
            None
        """
        
        self.number = elemNbr
        self.dim = dimension
        self.type = "completeElectrode core Hua".lower()
        self.connectivity = connectivity.astype(int)
        self.coords = coords[connectivity[:-1], :]
        self.centroid = np.mean(self.coords, axis=0)
        self.isSparse = False
        self.isRegion = False

        if self.dim == 2:
            self.nNodes = 3
            self.height2D = height2D
        else:
            self.nNodes = 4
            self.height2D = None
        self.propertiesDict = propertiesDict
        self.rhoT = rhoT

        self.Kgeom = None
        self._calc_localKgeom()

    def _calc_localKgeom(self):
        """
        Compute the geometric component of the local stiffness matrix.

        Returns:
            None
        """
        if self.dim == 2:
            length = scipyLinalg.norm(self.coords[1, :] - self.coords[0, :])
            self.Kgeom = (length * self.height2D / 6.0) * np.array(
                [[2.0, 1.0, -3.0], [1.0, 2.0, -3.0], [-3.0, -3.0, 6.0]]
            )
        else:
            v1 = self.coords[1, :] - self.coords[0, :]
            v2 = self.coords[2, :] - self.coords[0, :]
            area = 0.5 * scipyLinalg.norm(np.cross(v1, v2))
            self.Kgeom = (area / 3.0) * np.array(
                [
                    [1.0, 0.0, 0.0, -1.0],
                    [0.0, 1.0, 0.0, -1.0],
                    [0.0, 0.0, 1.0, -1.0],
                    [-1.0, -1.0, -1.0, 3.0],
                ]
            )


class CompleteElectrodeHua(UniformRhoRegion):
    """
    Hua's complete electrode model.

    This class represents Hua's complete electrode model, extending the UniformRhoRegion.

    Attributes:
        number (int): Number of the element.
        dim (int): Dimension of the electrode model (2 or 3).
        type (str): Type of the complete electrode model.
        propertiesDict (dict): Dictionary containing the properties of the electrode.
        rhoT (float): Electrode parameter [rho*t] from Hua's model.
        isSparse (bool): Flag indicating whether the local matrix is sparse.
        isRegion (bool): Flag indicating whether the electrode is part of a region.
        height2D (float): Associated height of the triangular element (used only if dim=2).
        virtualNodeNbr (int): Virtual node of the electrode in global terms.
        connectivity (numpy.ndarray): Nodes of the elements in global terms.
        coords (numpy.ndarray): Coordinates of nodes in the FemModel.
        centroid (numpy.ndarray): Centroid of the electrode.
        elements (list): List of CoreElectrodeHua elements composing the region.
        nNodes (int): Total number of nodes in the region.
        nElements (int): Total number of elements in the region.

    """

    def __init__(
        self,
        dimension,  # type: int
        elemNbr,  # type: int
        connectivities,  # type: Array[int]
        coords,  # type: Array[float]
        rhoT,  # type float
        height2D,  # type: float
        virtualNodeNbr,  # type: int
        isSparse=False,  # type: bool
        propertiesDict=None,  # type: dict
    ):
        """
        Initialize the CompleteElectrodeHua instance.

        Parameters:
            dimension (int): Dimension of the electrode model (2 or 3).
            elemNbr (int): Number of the element.
            connectivities (numpy.ndarray): Nodes of the elements in global terms.
            coords (numpy.ndarray): Coordinates of nodes in the FemModel.
            rhoT (float): Electrode parameter [rho*t] from Hua's model.
            height2D (float): Associated height of the triangular element (used only if dim=2).
            virtualNodeNbr (int): Virtual node of the electrode in global terms.
            isSparse (bool): Flag indicating whether the local matrix is sparse.
            propertiesDict (dict): Dictionary containing the properties of the electrode.

        Returns:
            None
        """

        self.number = elemNbr
        self.dim = dimension
        self.type = "completeElectrode Hua".lower()
        self.propertiesDict = propertiesDict
        self.rhoT = rhoT
        self.isSparse = isSparse
        self.isRegion = True

        if self.dim == 2:
            self.height2D = height2D
        else:
            self.height2D = None

        # register the virtual node
        self.virtualNodeNbr = virtualNodeNbr
        connectivities = np.hstack(
            (
                connectivities,
                self.virtualNodeNbr * np.ones([connectivities.shape[0], 1]),
            )
        )

        # build local connectivity
        self.connectivity, connectivityLocal = np.unique(
            connectivities, return_inverse=True
        )
        self.connectivity = self.connectivity.astype(int)
        self.connectivityElementsLocal = connectivityLocal.reshape(
            len(connectivityLocal) // connectivities.shape[1], connectivities.shape[1]
        )

        # total number of elements and nodes of the region
        self.nNodes = self.connectivity.shape[0]
        self.nElements = self.connectivityElementsLocal.shape[0]

        # does not contain the coords of the virtual node!
        self.coords = coords[self.connectivity[:-1], :]

        self.centroid = np.mean(self.coords, axis=0)

        self.elements = None
        self.appendElements()

        if self.isSparse:
            self._calc_localKgeom_Sparse()
        else:
            self._calc_localKgeom()

    def appendElements(self):
        """
        Create elements composing the region.

        This functions does not use multiprocessing but is faster.

        Returns:
            None
        """
        
        self.elements = []

        for i, c in enumerate(self.connectivityElementsLocal):
            proPDict = self.propertiesDict.copy()
            proPDict["gmshElemNbr"] = proPDict["gmshElemNbr"][i]
            self.elements.append(
                CoreElectrodeHua(
                    self.dim, i, c, self.coords, self.rhoT, self.height2D, proPDict
                )
            )

        self.nElements = len(self.elements)
