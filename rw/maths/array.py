# a wrapper function for numpy 
import sys 
sys.path.append(".")
import numpy as np 
import math
from multipledispatch import dispatch

from core.error import RW_Ensure, RW_Fail

class Array:
    @dispatch()
    def __init__(self):
        self._n = 0
        self._data = None

    @dispatch((int,float))
    def __init__(self, size_):
        self._n = size_
        self._data = np.zeros(int(size_))
        
    @dispatch(int,(int,float))
    def __init__(self, size_, value_):
        self._n = size_
        self._data = np.ones(int(size_)) * value_
        
    @dispatch(int,(int,float),(int,float))
    def __init__(self, size_, value_, increment_):
        self._n = size_
        array_ = [value_ + increment_* i for i in range(int(size_))]
        self._data = np.array(array_)

    @dispatch((list,object))
    def __init__(self, array_):
        if isinstance(array_, list):
            self._data = np.array(array_)
            self._n = len(array_)
        elif isinstance(array_, np.ndarray):
            self._data = array_
            self._n = len(array_)
        elif isinstance(array_,Array):
            self._data = array_._data
            self._n = array_._n
        else:
            raise Exception("Initiation Error: not implemented type")

    def __str__(self):
        return "Array({0})".format(self._data)
    
    #Assign Operation is not an Option in python

    def __len__(self):
        return self._n

    def __getitem__(self,s):
        if isinstance(s, int):
            if s < 0 or s >= self._n:
                raise IndexError
            else:
                return self._data[s]

    def at(self, s):
        self.__getitem__(s)

    def front(self):
        return self.__getitem__(0)

    def back(self):
        return self.__getitem__(self._n - 1)

    def size(self):
        return self._n

    def resize(self):
        raise NotImplementedError

    @staticmethod
    def DotProduct(v1,v2):
        
        if isinstance(v1, list):
            v1 = np.array(list)
        elif isinstance(v1, Array):
            v1 = v1._data
        elif isinstance(v1,np.ndarray):
            v1 = v1
        else:
            RW_Fail("DotProduct first variable is not implemented") 
        
        if isinstance(v2, list):
            v2 = np.array(list)
        elif isinstance(v2, Array):
            v2 = v2._data
        elif isinstance(v2,np.ndarray):
            v2 = v2
        else:
            RW_Fail("DotProduct second variable is not implemented")       

        RW_Ensure(len(v1) == len(v2), "Two variables do not have the same size.")
        return np.dot(v1,v2)

    @staticmethod
    def Norm2(v):
        return math.sqrt(Array.DotProduct(v,v))

    @staticmethod
    def Abs(v):
        if isinstance(v, list):
            v1 = np.array(list)
        elif isinstance(v, Array):
            v1 = v._data
        elif isinstance(v,np.ndarray):
            v1 = v
        else:
            RW_Fail("Abs is not implemented for the variable class") 
        
        return Array(abs(v1))

    @staticmethod
    def Sqrt(v):
        if isinstance(v, list):
            v1 = np.array(list)
        elif isinstance(v, Array):
            v1 = v._data
        elif isinstance(v,np.ndarray):
            v1 = v
        else:
            RW_Fail("Sqrt is not implemented for the variable class") 
        
        return Array(np.sqrt(v1))

    @staticmethod
    def Log(v):
        if isinstance(v, list):
            v1 = np.array(list)
        elif isinstance(v, Array):
            v1 = v._data
        elif isinstance(v,np.ndarray):
            v1 = v
        else:
            RW_Fail("Log is not implemented for the variable class") 
        
        return Array(np.log(v1))

    @staticmethod
    def Exp(v):
        if isinstance(v, list):
            v1 = np.array(list)
        elif isinstance(v, Array):
            v1 = v._data
        elif isinstance(v,np.ndarray):
            v1 = v
        else:
            RW_Fail("Exp is not implemented for the variable class") 
        
        return Array(np.exp(v1))

    @staticmethod
    def Pow(v, n):
        if isinstance(v, list):
            v1 = np.array(list)
        elif isinstance(v, Array):
            v1 = v._data
        elif isinstance(v,np.ndarray):
            v1 = v
        else:
            RW_Fail("Abs is not implemented for the variable class") 
        
        return Array(np.power(v1, n))

    def __eq__(self, o: object) -> bool:
        if isinstance(o, list):
            return np.array_equal(np.array(o), self._data)
        elif isinstance(o, np.ndarray):
            return np.array_equal(o, self._data)
        elif isinstance(o,Array):
            return np.array_equal(self._data, o._data)
        else:
            return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    @dispatch((int,float))
    def __add__(self,value_):
        data_ = self._data + value_
        return Array(data_)

    @dispatch(object)
    def __add__(self,array_):
        if isinstance(array_, list):
            np_array = np.array(array_)
        elif isinstance(array_, np.ndarray):
            np_array = array_
        elif isinstance(array_,Array):
            np_array = array_._data
        else:
            RW_Fail("Add Method Error: not implemented type")
        
        if (len(np_array) == len(self._data)):
            data_ = self._data + np_array
        else:
            RW_Fail("arrays with different sizes cannot be added")
        
        return Array(data_)

    @dispatch((int,float))
    def __radd__(self,value_):
        return self.__add__(value_)

    @dispatch(object)
    def __radd__(self,array_):
        return self.__add__(array_)

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
        elif isinstance(array_,Array):
            np_array = array_._data
        else:
            RW_Fail("Initiation Error: not implemented type")
        
        if (len(np_array) == len(self._data)):
            self._data = self._data + np_array
        else:
            RW_Fail("arrays with different sizes cannot be added")
        
        return self

    @dispatch((int,float))
    def __sub__(self,value_):
        data_ = self._data - value_
        return Array(data_)

    @dispatch(object)
    def __sub__(self,array_):
        if isinstance(array_, list):
            np_array = np.array(array_)
        elif isinstance(array_, np.ndarray):
            np_array = array_
        elif isinstance(array_,Array):
            np_array = array_._data
        else:
            RW_Fail("Initiation Error: not implemented type")
        
        if (len(np_array) == len(self._data)):
            data_ = self._data - np_array
        else:
            RW_Fail("arrays with different sizes cannot be subtracted")

        return Array(data_)

    @dispatch((int,float))
    def __rsub__(self,value_):
        array_ =  self.__sub__(value_)
        array_._data = - array_._data
        return array_

    @dispatch(object)
    def __rsub__(self,array_):
        array_ =  self.__sub__(array_)
        array_._data = - array_._data
        return array_

    @dispatch((int,float))
    def __isub__(self,value_):
        self._data = self._data - value_
        return self

    @dispatch(object)
    def __isub__(self,array_):
        if isinstance(array_, list):
            np_array = np.array(array_)
        elif isinstance(array_, np.ndarray):
            np_array = array_
        elif isinstance(array_,Array):
            np_array = array_._data
        else:
            RW_Fail("Initiation Error: not implemented type")
        
        if (len(np_array) == len(self._data)):
            self._data = self._data - np_array
        else:
            RW_Fail("arrays with different sizes cannot be subtracted")
        
        return self

    @dispatch((int,float))
    def __mul__(self,value_):
        data_ = self._data * value_
        return Array(data_)

    @dispatch(object)
    def __mul__(self,array_):
        if isinstance(array_, list):
            np_array = np.array(array_)
        elif isinstance(array_, np.ndarray):
            np_array = array_
        elif isinstance(array_,Array):
            np_array = array_._data
        else:
            RW_Fail("Initiation Error: not implemented type")
        
        if (len(np_array) == len(self._data)):
            data_ = self._data * np_array
        else:
            RW_Fail("arrays with different sizes cannot be multiplied")

        return Array(data_)

    @dispatch((int,float))
    def __rmul__(self,value_):
        return self.__mul__(value_)

    @dispatch(object)
    def __rmul__(self,array_):
        return self.__mul__(array_)

    @dispatch((int,float))
    def __imul__(self,value_):
        self._data = self._data * value_
        return self

    @dispatch(object)
    def __imul__(self,array_):
        if isinstance(array_, list):
            np_array = np.array(array_)
        elif isinstance(array_, np.ndarray):
            np_array = array_
        elif isinstance(array_,Array):
            np_array = array_._data
        else:
            RW_Fail("Initiation Error: not implemented type")
        
        if (len(np_array) == len(self._data)):
            self._data = self._data * np_array
        else:
            RW_Fail("arrays with different sizes cannot be multiplied")
        
        return self

    @dispatch((int,float))
    def __truediv__(self,value_):
        data_ = self._data / value_
        return Array(data_)

    @dispatch(object)
    def __truediv__(self,array_):
        if isinstance(array_, list):
            np_array = np.array(array_)
        elif isinstance(array_, np.ndarray):
            np_array = array_
        elif isinstance(array_,Array):
            np_array = array_._data
        else:
            RW_Fail("Initiation Error: not implemented type")
        
        if (len(np_array) == len(self._data)):
            data_ = self._data / np_array
        else:
            RW_Fail("arrays with different sizes cannot be subtracted")

        return Array(data_)

    @dispatch((int,float))
    def __rtruediv__(self,value_):
        array_ =  self.__truediv__(value_)
        array_._data = 1 / array_._data
        return array_

    @dispatch(object)
    def __rtruediv__(self,array_):
        array_ =  self.__truediv__(array_)
        array_._data = 1 / array_._data
        return array_

    @dispatch((int,float))
    def __idiv__(self,value_):
        self._data = self._data / value_
        return self

    @dispatch(object)
    def __idiv__(self,array_):
        if isinstance(array_, list):
            np_array = np.array(array_)
        elif isinstance(array_, np.ndarray):
            np_array = array_
        elif isinstance(array_,Array):
            np_array = array_._data
        else:
            RW_Fail("Initiation Error: not implemented type")
        
        if (len(np_array) == len(self._data)):
            self._data = self._data / np_array
        else:
            RW_Fail("arrays with different sizes cannot be subtracted")
        
        return self

if __name__ == "__main__":
    t0 = Array(1,1)
    print(t0)
    t1 = Array(1)
    t2 = Array(1,2)
    t3 = Array([2])
    t4 = Array(np.array([2, 4]))

    print(Array.Pow(t4,3))
