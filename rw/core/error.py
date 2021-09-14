
class RWBaseError(Exception):
    pass

def RW_Require(instance_, attr):
    if not hasattr(instance_, attr):
        raise RWBaseError("Object {0} does not contain property {1}.".format(instance_,attr))
    else:
        if getattr(instance_,attr) is None:
            raise RWBaseError("Object {0} property {1} is None.".format(instance_,attr))

def RW_Ensure(condition_,comments_ = "Condition do not meet"):
    if condition_:
        pass
    else:
        raise RWBaseError(comments_)

def RW_TypeCheck(instance_, class_, comments_ = "The type of instance is not the required class"):
    if issubclass(type(instance_),class_):
        pass
    else:
        raise RWBaseError(comments_)
        
def RW_Fail(description_):
    raise RWBaseError(description_)

