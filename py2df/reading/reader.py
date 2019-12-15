"""
The reader class, and related classes.
"""
import typing
import json
import base64
import gzip
import functools
import nbtlib as nbt
from collections import deque
from .. import constants
from ..schemas import ItemSchema, ItemTagSchema
from ..utils import remove_u200b_from_doc, flatten, serialize_tag, dumps_json
from ..enums import PlotSizes, IfEntityType, Color
from ..constants import DEFAULT_VAL, DEFAULT_AUTHOR, SNBT_EXPORT_VERSION
from ..classes import Codeblock, FunctionHolder, JSONData, Arguments, Material, BracketedBlock, Block


class DFReader:
    """
    Reader; runs the functions and manages all actions. **Singleton.**

    Change its attributes (configuration) by instantiating it. For example::

        if __name__ == '__main__':
            DFReader(PlotSizes.LARGE_PLOT, auto_split=True)  # changes config
            ...

    To output the Paste item NBT, use :meth:`DFReader.output_snbt` .

    Attributes
    ----------\u200b
        plot_size : :class:`~py2df.enums.parameters.PlotSizes`
            Size of the plot this code is being developed for. Default is
            :attr:`~py2df.enums.parameters.PlotSizes.BASIC_PLOT` .

        auto_split : :class:`bool`
            If True, upon reaching the plot's length limit, the reader will automatically create a Function where to
            continue code, **if possible** (will error if that is impossible, i.e., it is not possible to shorten the
            code length). If False, will error at any trespassing of plot limit. Default: ``False``.

        author : :class:`str`
            The author of this code, to be inserted in the NBT returned by :meth:`DFReader.output_snbt`. Default:
             ``"Unknown"``.

        lines : List[Deque[:class:`~py2df.classes.abc.Codeblock`]]
            List of all lines of codeblocks. (Each line is a :class:`deque` , for performance reasons.)

        functions : Tuple[FunctionHolder]
            A read-only copy of the internal function holder :class:`list` .
    """
    __slots__ = (
        "lines", "plot_size", "auto_split", "author", "_functions", "_curr_line", "_curr_loc", "_prev_curr_locs"
    )
    lines: typing.List[typing.Deque[Codeblock]]

    plot_size: PlotSizes

    auto_split: bool

    author: str

    _functions: typing.List[FunctionHolder]  #: List of FunctionHolder instances that hold the code lines.

    _curr_line: int  #: Current line being read (index in the :attr:`lines` list).

    _curr_loc: typing.Optional[BracketedBlock]  #: The current bracket level, or None to send codeblocks to main line.

    _prev_curr_locs: typing.List[typing.Optional[BracketedBlock]]  #: The previous bracket levels, for bracket closes.

    _singleton: "DFReader" = None  #: The singleton instance of :class:`DFReader`.

    def __new__(cls, *args, **kwargs):
        if cls._singleton:
            if args or kwargs:  # there was an update in settings!
                cls._singleton.set(*args, **kwargs)

            return cls._singleton

        new_obj = object.__new__(cls)
        new_obj.__init__(*args, **kwargs)

        cls._singleton = new_obj

        return new_obj

    def __init__(
        self, plot_size: PlotSizes = PlotSizes.BASIC_PLOT, auto_split: bool = False,
        author: str = DEFAULT_AUTHOR
    ):
        """
        Inits this :class:`Reader`.

        Parameters
        ----------
        plot_size : :class:`~py2df.enums.parameters.PlotSizes`, optional
            Size of the plot this code is being developed for. Default is
            :attr:`~py2df.enums.parameters.PlotSizes.BASIC_PLOT` .

        auto_split : :class:`bool`, optional
            Whether or not to automatically split long code lines into multiple Functions. Defaults to ``False`` .

        author : :class:`str`, optional
            The author of this code, to be inserted in the NBT returned by :meth:`DFReader.output_snbt`. Defaults
            to ``"Unknown"``.
        """
        if self.__class__._singleton:
            return

        self.plot_size: PlotSizes = PlotSizes(plot_size)
        self.auto_split: bool = bool(auto_split)
        self.lines: typing.List[typing.Deque[Codeblock]] = []
        self.author = str(author)
        self._functions: typing.List[FunctionHolder] = []
        self._curr_line = 0
        self._curr_loc = None
        self._prev_curr_locs = []

    def set(
        self, plot_size: PlotSizes = DEFAULT_VAL, auto_split: bool = DEFAULT_VAL,
        author: str = DEFAULT_VAL
    ) -> "DFReader":
        """
        Configures this Reader.

        Parameters
        ----------
        plot_size : :class:`~py2df.enums.parameters.PlotSizes`, optional
            Size of the plot this code is being developed for.

        auto_split : :class:`bool`, optional
            Whether or not to automatically split long code lines into multiple Functions. Default is ``False`` .

        author : :class:`str`, optional
            The author of this code, to be inserted in the NBT returned by :meth:`DFReader.output_snbt`. Defaults
            to ``"Unknown"``.

        Returns
        -------
        :class:`DFReader`
            self to allow chaining
        """
        if plot_size != DEFAULT_VAL:
            self.plot_size = PlotSizes(plot_size)

        if auto_split != DEFAULT_VAL:
            self.auto_split = bool(auto_split)

        return self

    def append_function(self, fn_holder: FunctionHolder) -> None:
        """
        Appends a function to be read in this reader.

        Parameters
        ----------
        fn_holder : :class:`~py2df.classes.abc.FunctionHolder`
            The function holder that has the function to be used.

        Returns
        -------
        ``None``
            ``None``
        """
        if not isinstance(fn_holder, FunctionHolder):
            raise TypeError("Function holder has to be an instance of FunctionHolder ABC.")

        self._functions.append(fn_holder)

    def append_codeblock(self, codeblock: Codeblock) -> None:
        """
        Appends a codeblock to the current location (If block, line etc.) being read.

        Parameters
        ----------
        codeblock : :class:`~py2df.classes.abc.Codeblock`
            The codeblock to be added (must be an instance of a class implementing the
            :class:`~py2df.classes.abc.Codeblock` ABC).

        Returns
        -------
        ``None``
            ``None``
        """
        if not isinstance(codeblock, Codeblock):
            raise TypeError("Codeblock has to be an instance of the Codeblock ABC.")

        loc = self.curr_code_loc
        if loc is not None:
            if isinstance(loc, BracketedBlock):
                loc.codeblocks.append(codeblock)
            else:
                loc.append(codeblock)

    def remove_function(self, fn_holder: FunctionHolder) -> None:
        """
        Removes a specific function holder to be read from this reader.

        Parameters
        ----------
        fn_holder : :class:`~py2df.classes.abc.FunctionHolder`
            The function holder to be removed.

        Returns
        -------
        ``None``
            ``None``
        """
        self._functions.remove(fn_holder)

    def remove_codeblock(self, codeblock: Codeblock) -> None:
        """
        Removes a codeblock from the location (If block, line etc.) being currently read.

        Parameters
        ----------
        codeblock : Codeblock
            The codeblock to remove from the current line.

        Returns
        -------
        ``None``
            ``None``
        """
        loc = self.curr_code_loc

        if loc is not None:
            if isinstance(loc, BracketedBlock):
                loc.codeblocks.remove(codeblock)
            else:
                loc.remove(codeblock)

    @property
    def curr_line(self) -> typing.Optional[typing.Deque[Codeblock]]:
        """
        The line being currently read, or ``None`` if none is.

        Returns
        -------
        Optional[Deque[:class:`~py2df.classes.abc.Codeblock`]]
        """
        lines = self.lines
        curr_ind = self._curr_line
        if len(lines) > curr_ind:
            return lines[curr_ind]
        else:
            return None

    @property
    def curr_code_loc(self) -> typing.Union[BracketedBlock, typing.Deque[Codeblock]]:
        """
        The bracket level the code is in, currently (and where codeblocks are sent to), or a
        :class:`~collections.deque` for main code line.

        Returns
        -------
        Union[:class:`~py2df.classes.abc.BracketedBlock`, Deque[:class:`~py2df.classes.abc.Codeblock`]]
            The :class:`~py2df.classes.abc.BracketedBlock` representing the current bracket level of the code, or
            a deque being the main line.
        """
        curr = self._curr_loc
        if curr is not None:
            return curr
        else:
            return self.curr_line

    @curr_code_loc.setter
    def curr_code_loc(self, new_loc: BracketedBlock) -> None:
        """
        Set the current location to a Bracketed Block.

        Parameters
        ----------
        new_loc : :class:`~py2df.classes.abc.BracketedBlock`
            The new bracket level this code is in.

        Returns
        -------
        ``None``
            ``None``

        Raises
        ------
            :exc:`TypeError`: If the given location is not an instance of :class:`~py2df.classes.abc.BracketedBlock`.
        """
        if not isinstance(new_loc, BracketedBlock):
            raise TypeError("The new code bracket level must be an instance of (implement) BracketedBlock.")

        self._prev_curr_locs.append(self._curr_loc)
        self._curr_loc = new_loc

    def close_code_loc(self) -> None:
        """
        Sets the current location to the previous one (i.e., closes the bracket).

        Returns
        -------
        ``None``
            ``None``
        """
        self._curr_loc = self._prev_curr_locs.pop()

    @property
    def functions(self) -> typing.Tuple[FunctionHolder]:
        return tuple(self._functions)

    @functions.setter
    def functions(self, new_iter: typing.Iterable[FunctionHolder]) -> None:
        new_list = list(new_iter)
        if any(not isinstance(o, FunctionHolder) for o in new_list):
            raise TypeError("All function holders must be an instance of FunctionHolder ABC.")

        self._functions = new_list  # TODO: Add listening api - listen to add_codeblock etc.

    def read(self):
        """
        Reads the code of every given function, and stores it. Note that running this will **erase any previously
        generated data**.

        Returns
        -------
        ``None``
            ``None``

        Warnings
        --------
        Every function given will be run, meaning that any function with "side effects" (i.e., changes something on the
        system and whatnot) may be dangerous if running :meth:`~DFReader.read` more than once, so it is recommended to
        **only run this method once.**
        """
        self._curr_line = -1  # first index will, then, be 0
        for fn_holder in self._functions:
            self._curr_line += 1
            line = deque()
            if len(self.lines) <= self._curr_line:  # if there is no corresponding deque for this function holder
                self.lines.append(line)
            else:
                self.lines[self._curr_line] = line  # clear

            fn_holder.function()
            if isinstance(fn_holder, Codeblock):  # event/function/process
                line.appendleft(fn_holder)

    def output_json_data(self, read: bool = True) -> typing.List[dict]:
        """
        Outputs a JSON serializable :class:`dict` representing each code line.

        Parameters
        ----------
        read : :class:`bool`, optional
            Whether or not :meth:`~DFReader.read` should be called when running this function. Defaults to ``True`` .

        Returns
        -------
        List[:class:`dict`]
            List of dicts (one for every code line given).

        Warnings
        --------
        If ``read`` is ``True``, this method runs :meth:`~DFReader.read`, so make sure to take a look at its
        documentation and warnings.

        See Also
        --------
        :meth:`DFReader.read`
        """
        if read:
            self.read()  # obtain data

        lines = self.lines

        if not lines or not any(lines):
            raise ValueError("No code lines were generated, so JSON data cannot be exported.")

        return [
            dict(blocks=[
                block.as_json_data() if isinstance(block, JSONData) else dict(
                    id=constants.BLOCK_ID,
                    block=block.block.value,
                    **(
                        dict(
                            args=block.args.as_json_data()
                        ) if block.args and isinstance(block.args, Arguments) else dict()
                    ),
                    **(
                        dict(
                            action=str(block.action.value)
                        ) if block.action and hasattr(block.action, "value") else dict()
                    ),
                    **(
                        dict(
                            sub_action=(
                                "E" if block.sub_action in (
                                    IfEntityType.NAME_EQUALS, IfEntityType.IS_NEAR, IfEntityType.STANDING_ON
                                ) else ""  # ENameEquals; EIsNear; EStandingOn => separate from IfPlayer's.
                            ) + str(block.sub_action.value)
                        ) if block.sub_action and hasattr(block.sub_action, "value") else dict()
                    ),
                    **(
                        dict(
                            data=str(block.data)
                        ) if block.data else dict()
                    ),
                    **(
                        dict(
                            target=str(block.target.value)
                        ) if block.target and hasattr(block.target, "value") else dict()
                    )
                ) for block in flatten(
                    line, allow_iterables=(BracketedBlock, deque), keep_iterables=(BracketedBlock,)
                )  # flatten in order to include If code
            ]) for line in lines
        ]

    def output_json(self, read: bool = True) -> typing.List[str]:
        """
        Outputs the JSON string representing each code line.

        Parameters
        ----------
        read : :class:`bool`, optional
            Whether or not :meth:`~DFReader.read` should be called when running this function. Defaults to ``True`` .

        Returns
        -------
        List[:class:`str`]
            List of strings (one for every code line given).

        Warnings
        --------
        If ``read`` is ``True``, this method runs :meth:`~DFReader.read`, so make sure to take a look at its
        documentation and warnings.

        See Also
        --------
        :meth:`DFReader.output_json_data`
        """
        return [dumps_json(obj) for obj in self.output_json_data(read)]

    def output_encoded(self, read: bool = True) -> typing.List[bytes]:
        """
        Outputs the base64-formatted encoded bytes representing each code line's JSON format.

        Parameters
        ----------
        read : :class:`bool`, optional
            Whether or not :meth:`~DFReader.read` should be called when running this function. Defaults to ``True`` .

        Returns
        -------
        List[:class:`bytes`]
            List of :class:`bytes` instances (one for every code line given); they're all formatted in base 64
            (encoded in UTF-8).

        Warnings
        --------
        If ``read`` is ``True``, this method runs :meth:`~DFReader.read`, so make sure to take a look at its
        documentation and warnings.

        See Also
        --------
        :meth:`DFReader.output_json`
        """
        return [
            base64.b64encode(gzip.compress((json_str + "\n").encode("utf-8"))) for json_str in self.output_json(read)
        ]

    def output_encoded_str(self, read: bool = True) -> typing.List[str]:
        """
        Outputs the **stringified** base64-formatted encoded bytes representing each code line's JSON format.

        Parameters
        ----------
        read : :class:`bool`, optional
            Whether or not :meth:`~DFReader.read` should be called when running this function. Defaults to ``True`` .

        Returns
        -------
        List[:class:`str`]
            List of strings (one for every code line given); they're all formatted in base 64
            (encoded in UTF-8).

        Warnings
        --------
        If ``read`` is ``True``, this method runs :meth:`~DFReader.read`, so make sure to take a look at its
        documentation and warnings.

        See Also
        --------
        :meth:`DFReader.output_encoded`
        """
        return [btes.decode("utf-8") for btes in self.output_encoded(read)]

    def output_snbt(self, read: bool = True) -> typing.List[str]:
        """
        Outputs the SNBT format of the Paste item of each read line. It consists of the SNBT of an Ender Chest
        appropriately named as the first block in the code line.

        Parameters
        ----------
        read : :class:`bool`, optional
            Whether or not :meth:`~DFReader.read` should be called when running this function. Defaults to ``True`` .

        Returns
        -------
        List[:class:`str`]
            List of SNBT strings (one for every code line given); they're all formatted in base 64
            (encoded in UTF-8).

        Warnings
        --------
        If ``read`` is ``True``, this method runs :meth:`~DFReader.read`, so make sure to take a look at its
        documentation and warnings.

        See Also
        --------
        :meth:`DFReader.output_encoded_str`
        """
        encoded_strs = self.output_encoded_str(read)
        lines = self.lines

        def get_line_name(line: typing.Deque[Block]) -> str:
            first_codeblock = line[0]
            if isinstance(first_codeblock, Codeblock):
                return "No name"  # TODO: Name
            else:
                return Color.GOLD + Color.BOLD + "Code line"

        line_names = list(map(get_line_name, lines))

        return [
            serialize_tag(
                ItemSchema(
                    id=str(Material.ENDER_CHEST.value),
                    Count=1,
                    tag=ItemTagSchema(
                        PublicBukkitValues=nbt.Compound({
                            "hypercube:codetemplatedata": nbt.String(dumps_json(dict(
                                author=str(self.author or DEFAULT_AUTHOR),
                                name=line_names[i],
                                version=SNBT_EXPORT_VERSION,
                                code=encoded
                            )))
                        }),
                        display=dict(
                            Name=dumps_json(line_names[i])
                        )
                    )
                )
            ) for i, encoded in enumerate(encoded_strs)
        ]


remove_u200b_from_doc(DFReader)
