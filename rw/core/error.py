
class RWBaseError(Exception):
    pass


def RW_Require(self, attr):
    if not hasattr(self, attr):
        raise Exception("Object {0} does not contain property {1}.".format(self,attr))
    else:
        if getattr(self,attr) is None:
            raise Exception("Object {0} property {1} is None.".format(self,attr))