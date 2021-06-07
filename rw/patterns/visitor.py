from abc import ABC,abstractmethod

def _qualname(obj):
    """Get the fully-qualified name of an object (including module)."""
    return obj.__module__ + '.' + obj.__qualname__


def _declaring_class(obj):
    """Get the name of the class that declared an object."""
    name = _qualname(obj)
    return name[:name.rfind('.')]


# Stores the actual visitor methods
_methods = {}


# Delegating visitor implementation
def _visitor_impl(self, arg):
    """Actual visitor method implementation."""
    method = _methods[(_qualname(type(self)), type(arg))]
    return method(self, arg)


# The actual @visitor decorator
def visitor(arg_type):
    """Decorator that creates a visitor method."""

    def decorator(fn):
        declaring_class = _declaring_class(fn)
        _methods[(declaring_class, arg_type)] = fn

        # Replace all decorated methods with _visitor_impl
        return _visitor_impl

    return decorator



class Visitor(ABC):

    """
    The Visitor Interface declares a set of visiting methods that correspond to
    component classes. The signature of a visiting method allows the visitor to
    identify the exact class of the component that it's dealing with.
    """
    
    @abstractmethod
    def visit(self):
        pass


class Component(ABC):
    """
    The Component interface declares an `accept` method that should take the
    base visitor interface as an argument.
    """

    @abstractmethod
    def accept(self, visitor) -> None:
        pass



if __name__ == "__main__":

    
    class ConcreteComponentA(Component):
        """
        Same here: visitConcreteComponentB => ConcreteComponentB
        """

        def accept(self, visitor):
            visitor.visit(self)

        def exclusive_method_of_concrete_component_a(self) -> str:
            return "A"

    class ConcreteVisitor1(Visitor):

        @visitor(ConcreteComponentA)
        def visit(self, element) -> None:
            print(f"{element.exclusive_method_of_concrete_component_a()} + ConcreteVisitor1")


    visitor1 = ConcreteVisitor1()
    componentA = ConcreteComponentA()
    componentA.accept(visitor1)