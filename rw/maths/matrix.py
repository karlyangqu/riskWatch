
import sys 
sys.path.append(".")
import numpy as np 
import math
from multipledispatch import dispatch

from maths.array import Array
from core.error import RW_Ensure, RW_Fail

class Matrix:
    @dispatch()
    def __init__(self):
        self._rows = 0
        self._columns = 0
        self._data = None

    @dispatch((int,float), (int,float))
    def __init__(self, rows_, columns_):
        self._rows = int(rows_)
        self._columns = int(columns_)
        self._data = np.zeros((int(rows_),int(columns_)))
        
    @dispatch((int,float), (int,float),(int,float))
    def __init__(self, rows_, columns_, value_):
        self._rows = int(rows_)
        self._columns = int(columns_)
        self._data = np.ones((int(rows_),int(columns_))) * value_
    
    @dispatch(object)
    def __init__(self, matrix_):
        if isinstance(matrix_, list):
            data_ = np.array(matrix_)

            try:
                t = np.shape(data_)[1]
            except:
                raise Exception("Initiation Error: need 2D array")

            row_,col_ =  np.shape(data_)
            self._rows = int(row_)
            self._columns = int(col_)
            self._data = data_

        elif isinstance(matrix_, np.ndarray):
            data_ = matrix_
            try:
                t = np.shape(data_)[1]
            except:
                raise Exception("Initiation Error: need 2D array")

            row_,col_ =  np.shape(data_)
            self._rows = int(row_)
            self._columns = int(col_)
            self._data = data_

        elif isinstance(matrix_,Matrix):
            self._data = matrix_._data
            self._rows = matrix_._rows
            self._columns = matrix_._columns
        else:
            raise Exception("Initiation Error: not implemented type")

    def __str__(self):
        return "Matrix({0})".format(self._data)
    
    #Assign Operation is not an Option in python

    def __len__(self):
        return (self._rows, self._columns)

    def __getitem__(self,s):
        if isinstance(s, int):
            return self._data[s]

    def diagonal(self):
        n_ = min(self._rows, self._columns)
        return Array([self._data[i][i] for i in range(n_)])

    @staticmethod
    def inverse(matrix_):
        data_ = np.linalg.inv(matrix_._data)
        return Matrix(data_)
    
    @staticmethod
    def determinant(matrix_):
        return np.linalg.det(matrix_)

    @staticmethod
    def transpose(matrix_):
        return Matrix(matrix_.transpose())

    @staticmethod
    def outerProduct(v1,v2):

        if isinstance(v1, list):
            v1 = np.array(v1)
        elif isinstance(v1, np.ndarray):
            v1 = v1
        elif isinstance(v1,Array):
            v1 = v1._data
        else:
            RW_Fail("V1 Error: not implemented type")
        
        if isinstance(v2, list):
            v2 = np.array(v2)
        elif isinstance(v2, np.ndarray):
            v2 = v2
        elif isinstance(v2,Array):
            v2 = v2._data
        else:
            RW_Fail("V2 Error: not implemented type")        
        
        return Matrix(np.outer(v1,v2))

    def rows(self):
        return self._rows

    def columns(self):        
        return self._columns

    def size1(self):
        return self._rows
    
    def size2(self):
        return self._columns

    def empty(self):
        return self._data is None

    @dispatch((int,float))
    def __add__(self,value_):
        data_ = self._data + value_
        return Matrix(data_)

    @dispatch(object)
    def __add__(self,matrix_):
        if isinstance(matrix_, list):
            np_array = np.array(matrix_)
        elif isinstance(matrix_, np.ndarray):
            np_array = matrix_
        elif isinstance(matrix_,Matrix):
            np_array = matrix_._data
        else:
            RW_Fail("Add Method Error: not implemented type")
        
        if (np.shape(np_array)[0] == self._rows) and (np.shape(np_array)[1] == self._columns):
            data_ = self._data + np_array
        else:
            RW_Fail("Matrix with different sizes cannot be added")
        
        return Matrix(data_)

    @dispatch((int,float))
    def __radd__(self,value_):
        return self.__add__(value_)

    @dispatch(object)
    def __radd__(self,matrix_):
        return self.__add__(matrix_)

    @dispatch((int,float))
    def __iadd__(self,value_):
        self._data = self._data + value_
        return self

    @dispatch(object)
    def __iadd__(self,array_):
        if isinstance(array_, list):
            np_array = np.array(array_)
        elif isinstance(array_, np.ndarray):
            np_array = array_
        elif isinstance(array_,Matrix):
            np_array = array_._data
        else:
            RW_Fail("IAdd Method Error: not implemented type")

        if (np.shape(np_array)[0] == self._rows) and (np.shape(np_array)[1] == self._columns):
            data_ = self._data + np_array
        else:
            RW_Fail("Matrix with different sizes cannot be added")

        return self

    @dispatch((int,float))
    def __sub__(self,value_):
        data_ = self._data - value_
        return Matrix(data_)

    @dispatch(object)
    def __sub__(self,matrix_):
        if isinstance(matrix_, list):
            np_array = np.array(matrix_)
        elif isinstance(matrix_, np.ndarray):
            np_array = matrix_
        elif isinstance(matrix_,Matrix):
            np_array = matrix_._data
        else:
            RW_Fail("Add Method Error: not implemented type")
        
        if (np.shape(np_array)[0] == self._rows) and (np.shape(np_array)[1] == self._columns):
            data_ = self._data - np_array
        else:
            RW_Fail("Matrix with different sizes cannot be substracted")
        
        return Matrix(data_)

    def __rsub__(self,value_):
        array_ =  self.__sub__(value_)
        array_._data = - array_._data
        return array_
        
    @dispatch((int,float))
    def __isub__(self,value_):
        self._data = self._data - value_
        return self

    @dispatch(object)
    def __isub__(self,matrix_):
        if isinstance(matrix_, list):
            np_array = np.array(matrix_)
        elif isinstance(matrix_, np.ndarray):
            np_array = matrix_
        elif isinstance(matrix_,Matrix):
            np_array = matrix_._data
        else:
            RW_Fail("Isub Method Error: not implemented type")

        if (np.shape(np_array)[0] == self._rows) and (np.shape(np_array)[1] == self._columns):
            data_ = self._data - np_array
        else:
            RW_Fail("Matrix with different sizes cannot be subbed")

        return self

    @dispatch((int,float))
    def __mul__(self,value_):
        data_ = self._data * value_
        return Matrix(data_)
    
    @dispatch(object)
    def __mul__(self,matrix_):
        if isinstance(matrix_, list):
            np_array = np.array(matrix_)
        elif isinstance(matrix_, np.ndarray):
            np_array = matrix_
        elif isinstance(matrix_,Matrix):
            np_array = matrix_._data
        elif isinstance(matrix_,Array):
            np_array = np.expand_dims(matrix_._data, axis=1)
        else:
            RW_Fail("Multiply Error: not implemented type")
        
        if ( self._columns == np.shape(np_array)[0]):
            data_ = np.matmul(self._data, np_array)
        else:
            RW_Fail("Matrices cannot be multiplied")

        return Matrix(data_)

    def __rmul__(self,matrix_):
        if isinstance(matrix_, list):
            np_array = np.array(matrix_)
        elif isinstance(matrix_, np.ndarray):
            np_array = matrix_
        elif isinstance(matrix_,Matrix):
            np_array = matrix_._data
        elif isinstance(matrix_,Array):
            np_array = np.expand_dims(matrix_._data, axis=0)
        else:
            RW_Fail("Multiply Error: not implemented type")
        
        if (np.shape(np_array)[1] == self._rows):
            data_ = np.matmul(np_array, self._data)
        else:
            RW_Fail("Matrices cannot be multiplied")

        return Matrix(data_)

    @dispatch((int,float))
    def __imul__(self,value_):
        self._data = self._data * value_
        return self

    @dispatch(object)
    def __imul__(self,matrix_):
        if isinstance(matrix_, list):
            np_array = np.array(matrix_)
        elif isinstance(matrix_, np.ndarray):
            np_array = matrix_
        elif isinstance(matrix_,Matrix):
            np_array = matrix_._data
        elif isinstance(matrix_,Array):
            np_array = np.expand_dims(matrix_._data, axis=1)
        else:
            RW_Fail("Imul Error: not implemented type")
        
        if ( self._columns == np.shape(np_array)[0]):
            data_ = np.matmul(self._data, np_array)            
            row_,col_ =  np.shape(data_)

            self._rows = int(row_)
            self._columns = int(col_)
            self._data = data_

        else:
            RW_Fail("Matrices cannot be multiplied")
        
        return self

    @dispatch((int,float))
    def __truediv__(self,value_):
        data_ = self._data / value_
        return Matrix(data_)

    @dispatch((int,float))
    def __rtruediv__(self,value_):
        array_ =  self.__truediv__(value_)
        array_._data = 1 / array_._data
        return array_

if __name__ == "__main__":

    print(Matrix(1,1,2))
    t3 = Matrix([[2],[2]])
    t4 = Matrix(np.array([[2, 4],[2,4]]))
    print(t4 * t3)
    print(t3[1][0])
    print(np.outer(np.ones((5,)), np.linspace(-2, 2, 5)))
    print(Matrix.outerProduct(np.ones((5,)), np.linspace(-2, 2, 5)))
    print(Matrix.outerProduct(Array(np.ones((5,))), Array(np.linspace(-2, 2, 5))))

    a = np.array([[1, 0],
              [0, 1]])
    
    b = np.array([[4, 1],
              [2, 2]])

    print(Matrix(b) * Matrix(a))
    print(1 + Matrix(b))

    print(b.transpose())

