class DFDefault:
    def __repr__(self):
        return "DEFAULT_VAL"

    def __str__(self):
        return self.__repr__()


DEFAULT_VAL = DFDefault()  # used for detecting when no parameter was passed without using 'None' or alternatives.
