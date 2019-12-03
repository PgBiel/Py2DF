import typing
from ..utils import remove_u200b_from_doc
from ..enums import PlotSizes
from ..classes import Codeblock, FunctionHolder


class DFReader:
    """
    Reader; runs the functions and manages all actions.

    Attributes
    ----------\u200b
        lines : List[List[:class:`~py2df.classes.abcs.Codeblock`]]
            List of all lines of codeblocks.

        plot_size : :class:`~py2df.enums.parameters.PlotSizes`
            Size of the plot this code is being developed for.

        auto_split : :class:`bool`
            If True, upon reaching the plot's length limit, the reader will automatically create a Function where to
            continue code, **if possible** (will error if that is impossible, i.e., it is not possible to shorten the
            code length). If False, will error at any trespassing of plot limit. Default: False.

        functions : :class:`tuple`
            A read-only copy of the internal function holder :class:`list` .
    """
    __slots__ = ("lines", "plot_size", "auto_split", "_functions", "_curr_line")
    lines: typing.List[typing.List[Codeblock]]

    plot_size: PlotSizes

    auto_split: bool

    _functions: typing.List[FunctionHolder]  #: List of FunctionHolder instances that hold the code lines.

    _curr_line: int  #: Current line being read (index in the :attr:`lines` list).

    _singleton: "DFReader" = None  #: The singleton instance of :class:`DFReader`.

    def __new__(cls, *args, **kwargs):
        if cls._singleton:
            return cls._singleton

        new_obj = object.__new__(cls)
        new_obj.__init__(*args, **kwargs)

        return new_obj

    def __init__(self, plot_size: PlotSizes, auto_split: bool = False):
        """
        Inits this :class:`Reader`.

        Parameters
        ----------
        plot_size : :class:`~py2df.enums.parameters.PlotSizes`
            Size of the plot this code is being developed for.

        auto_split : :class:`bool`
            Whether or not to automatically split long code lines into multiple Functions. Defaults to ``False`` .
        """
        self.plot_size: PlotSizes = PlotSizes(plot_size)
        self.auto_split: bool = auto_split
        self.lines: typing.List[typing.List[Codeblock]] = []
        self._functions: typing.List[FunctionHolder] = []
        self._curr_line = 0

    def append_function(self, fn_holder: FunctionHolder) -> None:
        """
        Appends a function to be read in this reader.

        Parameters
        ----------
        fn_holder : :class:`~py2df.classes.abcs.FunctionHolder`
            The function holder that has the function to be used.

        Returns
        -------
        ``None``
            ``None``
        """
        if not isinstance(fn_holder, FunctionHolder):
            raise TypeError("Function holder has to be an instance of FunctionHolder ABC.")

        self._functions.append(fn_holder)

    def remove_function(self, fn_holder: FunctionHolder) -> None:
        """
        Removes a specific function holder to be read from this reader.

        Parameters
        ----------
        fn_holder : :class:`~py2df.classes.abcs.FunctionHolder`
            The function holder to be removed.

        Returns
        -------
        ``None``
            ``None``
        """
        self._functions.remove(fn_holder)

    @property
    def functions(self) -> typing.Tuple[FunctionHolder]:
        return tuple(self._functions)

    @functions.setter
    def functions(self, new_iter: typing.Iterable[FunctionHolder]) -> None:
        new_list = list(new_iter)
        if any(not isinstance(o, FunctionHolder) for o in new_list):
            raise TypeError("All function holders must be an instance of FunctionHolder ABC.")

        self._functions = new_list


remove_u200b_from_doc(DFReader)
