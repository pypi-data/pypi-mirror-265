from scipy import sparse as scipySparse

import numpy as np

class UniformRhoRegion():
    """
    Uniform rho region element.

    This class represents a uniform resistivity region element with linear properties.

    Attributes:
        number (int): Number of the element.
        dim (int): Dimension of the element (2 or 3).
        type (str): Type of the region element.
        propertiesDict (dict): Dictionary containing the properties of the region.
        rho (float): Resistivity of the element.
        isSparse (bool): Flag indicating whether the local matrix is sparse.
        isRegion (bool): Flag indicating whether the element is part of a region.
        height2D (float): Associated height of the triangular element (used only if dim=2).
        connectivity (numpy.ndarray): Nodes of the elements in global terms.
        coords (numpy.ndarray): Coordinates of nodes in the FemModel.
        centroid (numpy.ndarray): Centroid of the element.
        elements (list): List of sub-elements composing the region.
        nNodes (int): Total number of nodes in the region.
        nElements (int): Total number of elements in the region.
        Kgeom (numpy.ndarray): Geometric component of the local stiffness matrix.
        KgeomSp (scipy.sparse.coo_matrix): Geometric component of the local stiffness matrix in sparse form.

    """

    def __init__(self, dimension,  # type: int
                 elemNbr,  # type: int
                 connectivities,  # type: Array[int]
                 coords,  # type: Array[float]
                 rho,  # type float
                 height2D,  # type: float
                 isSparse=False,  # type: bool
                 propertiesDict=None  # type: dict
                 ):
        """
        Initialize the UniformRhoRegion instance.

        Parameters:
            dimension (int): Dimension of the element (2 or 3).
            elemNbr (int): Number of the element.
            connectivities (numpy.ndarray): Nodes of the elements in global terms.
            coords (numpy.ndarray): Coordinates of nodes in the FemModel.
            rho (float): Resistivity of the element.
            height2D (float): Associated height of the triangular element (used only if dim=2).
            isSparse (bool): Flag indicating whether the local matrix is sparse.
            propertiesDict (dict): Dictionary containing the properties of the region.

        Returns:
            None
        """
        self.number = elemNbr
        self.dim = dimension
        self.type = 'uniform region, linear'.lower()
        self.propertiesDict = propertiesDict
        self.rho = rho
        self.isSparse = isSparse
        self.isRegion = True

        if self.dim == 2:
            self.height2D = height2D
        else:
            self.height2D = None

        # build local connectivity
        self.connectivity, connectivityLocal = np.unique(connectivities, return_inverse=True)
        self.connectivity = self.connectivity.astype(int)
        self.connectivityElementsLocal = connectivityLocal.reshape(len(connectivityLocal) // connectivities.shape[1], connectivities.shape[1])

        # total number of elements and nodes of the region
        self.nNodes = self.connectivity.shape[0]
        self.nElements = self.connectivityElementsLocal.shape[0]

        self.coords = coords[self.connectivity, :]

        self.centroid = np.mean(self.coords, axis=0)

        self.elements = None
        self.appendElements()

        if self.isSparse:
            self._calc_localKgeom_Sparse()
        else:
            self._calc_localKgeom()

    def saveKgeom(self, fileName,  # type: str
                  binary=False  # type: bool
                  ):
        """
        Save geometric component of the matrix to a text file.

        Parameters:
            fileName (str): File path.
            binary (bool, optional): Save in binary format. Used only if matrix is not sparse. Default: False.

        Returns:
            None
        """
        if self.isSparse:
            scipySparse.save_npz(fileName, self.Kgeom, compressed=True)

        else:
            if binary:
                np.save(fileName, self.Kgeom)
            else:
                np.savetxt(fileName, self.Kgeom)

    def setRho(self, rho  # type: float
               ):
        """
        Set the resistivity of the region and all sub-elements.

        Parameters:
            rho (float): Resistivity value.

        Returns:
            None
        """
        self.rho = rho
        for e in self.elements:
            e.rho = rho

    def _calc_localKgeom(self):
        """
        Compute the geometric component of the local stiffness matrix.

        Returns:
            None
        """
        self.Kgeom = np.zeros([self.nNodes, self.nNodes])
        for e in self.elements:
            self.Kgeom[np.ix_(e.connectivity, e.connectivity)] += e.Kgeom

    def _calc_localKgeom_Sparse(self):
        """
        Compute the geometric component of the local stiffness matrix in sparse form.

        Returns:
            None
        """
        count = 0
        for e in self.elements:
            temp = scipySparse.coo_matrix(e.Kgeom)
            count += temp.nnz

        data = np.zeros(count)
        rowIdx = np.zeros(count)
        colIdx = np.zeros(count)

        position = 0
        for e in self.elements:
            temp = scipySparse.coo_matrix(e.Kgeom)
            data[position:position + temp.nnz] = temp.data
            rowIdx[position:position + temp.nnz] = e.connectivity[temp.row]
            colIdx[position:position + temp.nnz] = e.connectivity[temp.col]
            position += temp.nnz

        self.KgeomSp = scipySparse.coo_matrix((data, (rowIdx, colIdx)), shape=(self.nNodes, self.nNodes))
