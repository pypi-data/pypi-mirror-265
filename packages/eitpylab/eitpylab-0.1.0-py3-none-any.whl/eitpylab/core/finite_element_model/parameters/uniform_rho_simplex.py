from scipy import linalg as scipyLinalg
from scipy import sparse as scipySparse

import numpy as np

from eitpylab.core.finite_element_model.polygons.fem_elements import FemElements
 

class UniformRhoSimplex(FemElements):
    """
    Base class for uniform resistivity finite element modeling elements.
    
    This class serves as the base for creating finite elements with uniform resistivity.

    Attributes:
        number (int): Number of the element.
        dim (int): Dimension of the simplex (1, 2, or 3).
        type (str): Type of the element.
        nNodes (int): Number of nodes in the element.
        connectivity (numpy.ndarray): Nodes of the element in global terms.
        coords (numpy.ndarray): Coordinates of nodes in the FemModel.
        centroid (numpy.ndarray): Centroid of the element.
        propertiesDict (dict): Dictionary containing the properties of the simplex.
        rho (float): Resistivity of the element.
        Kgeom (numpy.ndarray): Geometric component of the local stiffness matrix.
        isSparse (bool): Flag indicating whether the local matrix is sparse.
        isRegion (bool): Flag indicating whether the element is part of a region.

    """

    def __init__(self, elemNbr,  # type: int
                 dimension,  # type: int
                 connectivity,  # type: Array[int]
                 coords,  # type: Array[float]
                 rho,  # type float
                 isSparse=False,  # type: bool
                 propertiesDict=None  # type: dict
                 ):
        """
        Initialize the UniformRhoSimplex instance.

        Parameters:
            elemNbr (int): Number of the element.
            dimension (int): Dimension of the simplex (1, 2, or 3).
            connectivity (numpy.ndarray): Nodes of the element in global terms.
            coords (numpy.ndarray): Coordinates of nodes in the FemModel.
            rho (float): Resistivity of the element.
            isSparse (bool, optional): Flag indicating whether the local matrix is sparse. Default: False.
            propertiesDict (dict, optional): Dictionary containing the properties of the simplex.

        Returns:
            None
        """
        
        self.number = elemNbr
        self.dim = dimension
        self.type = 'simplex'.lower()
        self.nNodes = connectivity.shape[0]
        self.connectivity = connectivity.astype(int)
        self.coords = coords[connectivity, :]
        self.centroid = np.mean(self.coords, axis=0)
        self.propertiesDict = propertiesDict
        self.rho = rho
        self.Kgeom = np.array([])  # type: Array[float]
        self.isSparse = isSparse
        self.isRegion = False

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
        Set the resistivity of the element.

        Parameters:
            rho (float): Resistivity value.

        Returns:
            None
        """
        self.rho = rho

    def calcSimplexVolume(self):
        """
        Compute the volume of the simplex.

        Returns:
            float: Volume of the simplex (1D: Length, 2D: Area, 3D: Volume).
        """
        vol = -1

        if self.dim == 1:
            vol = scipyLinalg.norm(self.coords[1, :] - self.coords[0, :])
        if self.dim == 2:
            v1 = self.coords[1, :] - self.coords[0, :]
            v2 = self.coords[2, :] - self.coords[0, :]
            vol = 0.5 * scipyLinalg.norm(np.cross(v1, v2))
        if self.dim == 3:
            v1 = self.coords[1, :] - self.coords[0, :]
            v2 = self.coords[2, :] - self.coords[0, :]
            v3 = self.coords[3, :] - self.coords[0, :]

            vol = (1.0 / 6.0) * scipyLinalg.norm(np.dot(np.cross(v1, v2), v3))

            # V2 = np.hstack((self.coords,np.ones((4,1))))  # vol = (1.0 / 6.0) * abs(scipyLinalg.det(V2))

        if vol < 1e-12:
            print("Warning: element %d with small volume: %e (GmshElmNbr %d)" % (self.number,vol,self.propertiesDict['gmshElemNbr']))
            print("Centroid: x=%f  y=%f  z=%f" % (self.centroid[0],self.centroid[1],self.centroid[2]))

        if vol < 0:
            print("Warning: element %d with negative volume: %e  (GmshElmNbr %d)" % (self.number,vol,self.propertiesDict['gmshElemNbr']))
            print("Centroid: x=%f  y=%f  z=%f" % (self.centroid[0],self.centroid[1],self.centroid[2]))

        return vol

    def getBbox(self):
        """
        Return the bounding box of the element.

        Returns:
            list: List of numpy arrays representing the minimum and maximum limits.
        """
        minimum = np.min(self.coords, axis=0)
        maximum = np.max(self.coords, axis=0)
        return [minimum, maximum]

    def getAspectRatio(self):
        """
        Return the aspect ratio of the simplex.

        Returns:
            float: Aspect ratio value between 0.0 and 1.0.
                   0.0: Zero-volume element.
                   1.0: Equilateral simplex (equilateral triangle or regular tetrahedron).
        """
        if self.dim == 1:
            L = scipyLinalg.norm(self.coords[0, :] - self.coords[1, :])
            if L == 0:
                ratio = 0.0
            else:
                ratio = 1.0

        if self.dim == 2:
            a = scipyLinalg.norm(self.coords[0, :] - self.coords[1, :])
            b = scipyLinalg.norm(self.coords[0, :] - self.coords[2, :])
            c = scipyLinalg.norm(self.coords[1, :] - self.coords[2, :])
            area = self.areaTriangle(self.coords[0, :], self.coords[1, :], self.coords[2, :])
            semiPerimeter = (a + b + c)/2.0

            if area == 0:
                ratio = 0.0
            else:
                if area < 1e-12:
                    print("Warning: element %d with small area: %e (GmshElmNbr %d)" % (self.number,area,self.propertiesDict['gmshElemNbr']))
                    print("Centroid: x=%f  y=%f  z=%f" % (self.centroid[0],self.centroid[1],self.centroid[2]))

                # https://www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-circumcircle
                Circumradius = a * b * c / (4.0 * area)
                # https://www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-incircle
                Inradius = area / semiPerimeter

                ratio = 2.0 * Inradius / Circumradius

        if self.dim == 3:

            # Inradius:   https://en.wikipedia.org/wiki/Tetrahedron#Inradius
            # area of each face
            A1 = self.areaTriangle(self.coords[1, :], self.coords[2, :], self.coords[3, :])
            A2 = self.areaTriangle(self.coords[0, :], self.coords[2, :], self.coords[3, :])
            A3 = self.areaTriangle(self.coords[0, :], self.coords[1, :], self.coords[3, :])
            A4 = self.areaTriangle(self.coords[0, :], self.coords[1, :], self.coords[2, :])
            volume = self.calcSimplexVolume()

            if volume == 0:
                ratio = 0.0
            else:
                if volume < 1e-12:
                    print("Warning: element %d with small volume: %e (GmshElmNbr %d)" % (self.number,volume,self.propertiesDict['gmshElemNbr']))
                    print("Centroid: x=%f  y=%f  z=%f" % (self.centroid[0],self.centroid[1],self.centroid[2]))

                Inradius = 3.0 * volume / (A1 + A2 + A3 + A4)

                # Circumradius    https://en.wikipedia.org/wiki/Tetrahedron#Circumradius
                # Lenghts
                a = scipyLinalg.norm(self.coords[1, :] - self.coords[0, :])
                A = scipyLinalg.norm(self.coords[2, :] - self.coords[3, :])
                b = scipyLinalg.norm(self.coords[2, :] - self.coords[0, :])
                B = scipyLinalg.norm(self.coords[1, :] - self.coords[3, :])
                c = scipyLinalg.norm(self.coords[3, :] - self.coords[0, :])
                C = scipyLinalg.norm(self.coords[1, :] - self.coords[2, :])

                Circumradius = np.sqrt((A * a + B * b + C * c) * (-A * a + B * b + C * c) * (A * a - B * b + C * c) * (A * a + B * b - C * c)) / (
                      24 * volume)

                # http://support.moldex3d.com/r15/en/modelpreparation_reference-pre_meshqualitydefinition.html
                ratio = 3.0 * Inradius / Circumradius

        return ratio
