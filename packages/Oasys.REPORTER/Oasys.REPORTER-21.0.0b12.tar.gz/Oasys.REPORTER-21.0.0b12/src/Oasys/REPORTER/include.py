import Oasys.gRPC


# Metaclass for static properties and constants
class IncludeType(type):
    _consts = {'NATIVE', 'UNIX', 'WINDOWS'}

    def __getattr__(cls, name):
        if name in IncludeType._consts:
            return Oasys.REPORTER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Include class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in IncludeType._consts:
            raise AttributeError("Cannot set Include class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Include(Oasys.gRPC.OasysItem, metaclass=IncludeType):


    def __del__(self):
        if not Oasys.REPORTER._connection:
            return

        if self._handle is None:
            return

        Oasys.REPORTER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If constructor for an item fails in program, then _handle will not be set and when
# __del__ is called to return the object we will call this to get the (undefined) value
        if name == "_handle":
            return None

        raise AttributeError("Include instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value
