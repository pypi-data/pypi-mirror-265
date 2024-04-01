import multiprocessing as mp

import numpy as np

from scipy import linalg as scipyLinalg
from scipy import sparse as scipySparse

class FemElements:
    """
    Base class for finite element modeling elements.

    This class provides common methods and utilities for finite element modeling.

    Attributes:
        None

    Methods:
        localRefSystem2D(v1, v2):
            Given two non-parallel vectors in R^3, returns an orthonormal local base in R^2 of the space spanned by
            the two vectors. The base is defined so that v1_local is parallel to v1, and v2_local has a positive
            second component.

        areaTriangle(node1, node2, node3):
            Computes the area of a triangle given the coordinates in R^3 of its nodes.

    """
    def __init__(self) -> None:
        """
        Initialize the FemElements instance.

        Parameters:
            None

        Returns:
            None
        """
        pass
    
    
    @staticmethod
    def localRefSystem2D(v1,  # type: Array[float]
                     v2  # type: Array[float]
                     ):
        """
        Given two non-parallel vectors in R^3, returns an orthonormal local base in R^2 of the space spanned by
        the two vectors. The base is defined so that v1_local is parallel to v1, and v2_local has a positive
        second component.

        Parameters:
            v1 (numpy.ndarray): Vector in R^3.
            v2 (numpy.ndarray): Vector in R^3.

        Returns:
            list: List of numpy arrays representing the local vectors [v1_local, v2_local].
        """
        
        e1 = v1 / scipyLinalg.norm(v1)
        e2 = v2 - v2.dot(e1) * e1
        e2 = e2 / scipyLinalg.norm(e2)
        base = np.hstack((e1[:, None], e2[:, None]))
        v1local = base.T.dot(v1)
        v2local = base.T.dot(v2)
        return [v1local, v2local]
    
    @staticmethod
    def areaTriangle(node1, node2, node3):
        """
        Computes the area of a triangle given the coordinates in R^3 of its nodes.

        Parameters:
            node1 (numpy.ndarray): Coordinates of the first node in R^3.
            node2 (numpy.ndarray): Coordinates of the second node in R^3.
            node3 (numpy.ndarray): Coordinates of the third node in R^3.

        Returns:
            float: Area of the triangle.
        """
        v1 = node2 - node1
        v2 = node3 - node1
        return 0.5 * scipyLinalg.norm(np.cross(v1, v2))

