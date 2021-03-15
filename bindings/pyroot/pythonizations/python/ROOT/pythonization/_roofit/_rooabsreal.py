import cppyy

from ROOT import pythonization

def __getter(k, v):
    # helper function to get CmdArg attribute from `RooFit` 
    # Parameters:
    # k: key of the kwarg
    # v: value of the kwarg
    if isinstance(v, (tuple, list)):
        attr = getattr(cppyy.gbl.RooFit, k)(*v)
    elif isinstance(v, (dict, )):
        attr = getattr(cppyy.gbl.RooFit, k)(**v)
    else:
        attr = getattr(cppyy.gbl.RooFit, k)(v)
    return attr


def _plotOn(self, *args, **kwargs):
    """
    Docstring
    """
    # Redefinition of `RooAbsReal.plotOn` for keyword arguments.
    # the keywords must correspond to the CmdArg of the `plotOn` function.
    # Parameters:
    # self: instance of `RooAbsReal` class
    # *args: arguments passed to `plotOn`
    # **kwargs: keyword arguments passed to `plotOn`
    if not kwargs:
        return self._OriginalPlotOn(*args)
    else:
        nargs = args + tuple((__getter(k, v) for k, v in kwargs.items()))
        return self._OriginalPlotOn(*nargs)

@pythonization()
def pythonize_rooabsreal(klass, name):
    # Parameters:
    # klass: class to be pythonized
    # name: string containing the name of the class

    if name == 'RooAbsReal':
        klass._OriginalPlotOn = klass.plotOn
        klass.plotOn = _plotOn

    return True