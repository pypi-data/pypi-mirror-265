"""Provides basic tools to track calculations """
import json
import os
#
from contextlib import contextmanager
from pathlib import Path
from string import Template


class CalculationIncompleteError(SystemExit):
    """Indicates that a calculation is incomplete and still files are missing"""


class Calculation:
    """Hold basic information of a calculation

    Attributes
    ----------

    folder : pathlib.Path
        The path to the folder, where the calculation should be performed

    required_output_files : dict(str)
        Dictionary with the names of the required outputfiles, that should be there after
        the calculation is performed

    inputfile : pathlib.Path
        path to the inputfile

    filename : str
        Name of the inputfile

    base : str
        basename of the file

    software : str or None
        Name of the software, the calculation should be performed


    Methods
    -------

    from_dct(dct, *, keeper=None)
        Initializes a calculation object from a dictionary


    as_dict()
        Return current object as dictionary

    within()
        Contextmanager that changes the current folder to the folder of the calculation class

    input_exists()
        Check if the inputfile is already present

    missing_as_string()
        Returns missing outputfiles as a summary string

    check()
        Checks if all required files are present

    as_pycode(clsname='Calculation', keeper=None)
        Gives the class as python code string, to be used e.g. in additional scripts
    """

    def __init__(self, inputfile, required_output_files, *,
                 folder=None, software=None, keeper=None):
        self.folder = Path(folder) if folder is not None else Path("")
        self.required_output_files = required_output_files
        self.inputfile = self.folder / Path(inputfile)
        self.base = self.inputfile.name[:-len(self.inputfile.suffix)]
        self.software = software
        # register itself
        self._register_itself(keeper)

    @classmethod
    def from_dct(cls, dct, *, keeper=None):
        """Initializes a calculation object from a dictionary

        Parameters
        ----------

        dct: dict
            Dictionary representing the Calculation object

        keeper: str, optional
            if given, name of the CalculationKeeper object in the created python code
            if None, no keeper will be specified

        Returns
        -------

        self:
            Calculation instance
        """
        return cls(dct['inputfile'], dct['required_output_files'],
                   folder=dct['folder'], software=dct.get('software', None),
                   keeper=keeper)

    @property
    def filename(self):
        """Returns the inputfilename of the calculation"""
        return self.inputfile.name

    def as_dict(self):
        """Return current object as dictionary

        Parameters
        ----------

        Returns
        -------

        dict:
            Dictionary representing the current object
            fields: inputfile, required_output_files, folder
            optional fields: software
        """
        dct = {'inputfile': self.inputfile.name,
               'required_output_files': self.required_output_files,
               'folder': str(self.folder),
               }
        if self.software is not None:
            dct['software'] = self.software
        return dct

    def as_pycode(self, *, clsname='Calculation', keeper=None):
        """Return current object as python code

        Parameters
        ----------

        clsname: str, optional
            Name of the Calculation class used

        keeper: str, optional
            if given, name of the CalculationKeeper object in the created python code
            if None, no keeper will be specified

        Returns
        -------
        str:
            class as basic python code string

        """
        if keeper is None:
            keeper = ''
        else:
            keeper = f'keeper={str(keeper)}, '
        #
        return (f'{clsname}("{self.inputfile.name}", ' +
                f'{json.dumps(self.required_output_files)}, ' +
                f'folder="{str(self.folder)}", ' +
                keeper +
                f'software="{str(self.software)}")')

    @contextmanager
    def within(self):
        """Contextmanager to perform a set of option within the folder of the system"""
        current = os.getcwd()
        try:
            os.chdir(self.folder)
            yield
        finally:
            os.chdir(current)

    def input_exists(self):
        """check if the inputfile is already present

        Returns
        -------
        bool
            True if file exists else False
        """
        return self.inputfile.exists()

    def missing_as_string(self, outfiles=None):
        """ Returns missing required files as string

        Parameters
        ----------

        outfiles : dictionary, optional
            dict of possible outfiles

        Returns
        -------
        str
            The missing files as string
        """
        if outfiles is None:
            outfiles = self._get_files_dct()
        return "\n".join(f'    - {req}: {self.required_output_files[req]}'
                         for req, ext in outfiles.items()
                         if ext is None)

    def get_missing(self):
        """return missing file names"""
        return self._get_files_dct()

    def get_required_output_files(self):
        """return required outpuf file"""
        outfiles = {}
        for name, options in self.required_output_files.items():
            outfiles[name] = [self.folder / self._render(option)
                              for option in options]
        return outfiles

    def check(self):
        """Checks if all required files are present, if not raises CalculationIncompleteError

        Raises
        ------

        CalculationIncompleteError
            In case some outputfiles are missing

        """

        outfiles = self._get_files_dct()

        error = self.missing_as_string(outfiles)

        if error != '':
            raise CalculationIncompleteError((f"For folder: '{str(self.folder)}' following "
                                              f" files missing:\n{error}\n\n"))
        return outfiles

    def _get_files_dct(self):
        """gets a basic dictionary with all setted and missing files"""
        outfiles = {}

        for name, options in self.required_output_files.items():
            outfiles[name] = None
            for option in options:
                option = self._render(option)
                filename = self.folder / option
                if filename.exists():
                    outfiles[name] = filename
                    break
        return outfiles

    def _register_itself(self, keeper):
        """register itself to a given keeper

        Parameters
        ----------

        keeper : CalculationKeeper
            CalculationKeeper self will be added to

        """
        if keeper is not None:
            keeper.add(self)

    def _render(self, option):
        """Render filepath for required_output_files

        Parameters
        ----------

        options : str
            possible filename

        """
        return Template(option).substitute(base=self.base)


def get_pycode(calculations, *, with_keeper=False, header=True,
               clsname='Calculation', keeper='keeper', calculationsname='calculations'):
    """get basic python code for a set of calculations

    Parameters
    ----------

    calculations : list(Calculation)
        list of calculation to be written

    with_keeper : bool, optional
        add a CalculationKeeper to the code, default: False

    header : bool, optional
        add header to script, default: True

    clsname : str, optional
        name of the Calculation class in the current python code, default 'Calculation'

    calculationsname : str, optional
        name of the list of Calculations generated

    keeper : str, optional
        name of the CalculationKeeper instance used for the calculations

    Returns
    -------

    str:
        python script

    """

    if header is True:
        header = f"from calkeeper import {clsname}"
        if with_keeper is True:
            header += "\nfrom calkeeper import CalculationKeeper"
    else:
        header = ''

    if with_keeper is True:
        body = f"{keeper} = CalculationKeeper()\n\n\n"
    else:
        keeper = None
        body = ""
    calculations = ',\n'.join(calc.as_pycode(clsname=clsname, keeper=keeper)
                              for calc in calculations)
    body += "\n# currently missing calculations"
    body += f"\n{calculationsname.strip()} = [{calculations}]\n\n\n"

    return f"{header}\n{body}\n"


def check(calculations):
    """Check multiple calculations, if one or more fail Raises CalculationIncompleteError

    Parameters
    ----------

    calculations : list(Calculation)
        List of calculation objects that should be checked


    Returns
    -------

    list(dict)
        List of dictionaries of the created output files


    Raises
    ------

    CalculationIncompleteError:
        If one or more calculation is not complete

    """
    files = []
    error = ""
    for calc in calculations:
        try:
            files.append(calc.check())
        except CalculationIncompleteError as err:
            error += err.code + "\n\n"
    if error != "":
        raise CalculationIncompleteError(error)
    return files


class CalculationFailed(SystemExit):
    """Error passed if the direct calculation failed"""


def perform_calculations(calculations, methods, ncores):
    """Perform the calculations  using a set of methods

    Parameters
    ----------

    calculations : list(Calculation)
        List of calculation objects that should be checked

    methods : dict(str: func)
        Dictionary of software names, and corresponding functions
        the function has to accept an Calculation object as input
        and should Raise an CalculationFailed Error incase of an issue

    ncores : int
        Number of cores

    Returns
    -------

    None

    Raises
    ------

    ValueError
        If no method is given for a software

    CalculationFailed
        If a calculation did not succeed
    """

    for calculation in calculations:
        method = methods.get(calculation.software)
        if method is None:
            raise ValueError(f"Software '{calculation.software}' not suppored")
        try:
            method(calculation, ncores)
        except CalculationFailed:
            raise CalculationFailed(f"Calculation failed in {calculation.folder}") from None

        try:
            calculation.check()
        except CalculationIncompleteError:
            raise CalculationFailed("Not all necessary files could be generated for calculation"
                                    f" '{calculation.inputfile}' in {calculation.folder}"
                                    ) from None


class CalculationKeeper:
    """Keeps track over all calculations that need to be submitted

    Methods
    -------

    calculation(*args, **kwargs)
        create a Calculation using self as the keeper

    get_calcls()
        Returns function to create Calculation class instances for this specific keeper

    add(calculation):
        Add a new Calculation to the keeper

    clear(self, clear_all=False)
        Remove all done calculations from the keeper

    check()
        Check if calculations need to be performed

    do_calculations(methods, do_all=False)
        Perform the calculations using a given methods

    get_pycode(only_incomplete=True, with_keeper=False, header=True,
               clsname='Calculation', keeper='keeper', calculationsname='calculations')
        get basic python code for a set of calculations

    get_incomplete()
        Return a list of all incompleted calculations
    """

    def __init__(self, calculations=None):
        if calculations is None:
            calculations = []
        self._calculations = calculations

    @classmethod
    def from_json(cls, jsonstr):
        """Returns the CalculationKeeper from a jsonstring"""
        self = cls()
        calculations = json.loads(jsonstr)
        for cal in calculations:
            self.calculation_from_dct(cal)
        return self

    def calculation_from_dct(self, dct):
        """Returns Calculation class instance with this specific keeper from a dictionary"""
        return Calculation.from_dct(dct, keeper=self)

    def calculation(self, *args, **kwargs):
        """Returns Calculation class instance with this specific keeper"""
        kwargs['keeper'] = self
        return Calculation(*args, **kwargs)

    def get_calcls(self):
        """Returns function to create Calculation class instances for this specific keeper"""

        def _get_calculation(*args, **kwargs):
            """Setup Calculation, with fixed keeper"""
            kwargs['keeper'] = self
            return Calculation(*args, **kwargs)

        # set doc to Calculation doc
        _get_calculation.__doc__ = Calculation.__doc__

        return _get_calculation

    def add(self, calculation):
        """Add a new Calculation to the keeper

        Parameters
        ----------

        calculation : Calculation
            The calculation to be added

        Returns
        -------

        None

        """
        assert isinstance(calculation, Calculation)
        self._calculations.append(calculation)

    def clear(self, clear_all=False):
        """Remove all done calculations from the keeper

        Parameters
        ----------

        clear_all : bool, optional
            default: False
            True: remove all calculations
            False: remove all incomplete calculations

        Returns
        -------

        None

        """
        if clear_all is False:
            self._calculations = self.get_incomplete()
        else:
            self._calculations = []

    def check(self):
        """Check if calculations need to be performed

        Parameters
        ----------

        Returns
        -------

        list(dict):
            List of dictionaries of the created output files

        Raises
        ------

        CalculationIncompleteError:
            In case some calculations are still missing
        """
        return check(self._calculations)

    def do_calculations(self, methods, ncores, *, do_all=False):
        """Perform the calculations  using a set of methods

        Parameters
        ----------

        methods : dict(str: func)
            Dictionary of software names, and corresponding functions
            the function has to accept an Calculation object as input
            and should Raise an CalculationFailed Error incase of an issue

        do_all : bool, optional
            do all calculations if True else only the missing ones default: False

        Returns
        -------

        None

        Raises
        ------

        ValueError
            If no method is given for a software

        CalculationFailed
            If a calculation did not succeed
        """
        if do_all is True:
            calculations = self._calculations
        else:
            calculations = self.get_incomplete()
        #
        perform_calculations(calculations, methods, ncores)

    def as_json(self, *, only_incomplete=True):
        """Returns a json representation of the current CalculationKeeper

        Parameters
        ----------

        only_incomplete : bool, optional
            use only incomplete calculations, default: True
        Returns
        -------

        str:
            json representation of the CalculationKeeper
        """

        if only_incomplete is False:
            calculations = self._calculations
        else:
            calculations = self.get_incomplete()

        result = [cal.as_dict() for cal in calculations]
        return json.dumps(result, indent=4)

    def get_pycode(self, *, only_incomplete=True, with_keeper=False, header=True,
                   clsname='Calculation', keeper='keeper', calculationsname='calculations'):
        """get basic python code for a set of calculations

        Parameters
        ----------

        only_incomplete : bool, optional
            use only incomplete calculations, default: True

        with_keeper : bool, optional
            add a CalculationKeeper to the code, default: False

        header : bool, optional
            add header to script, default: True

        clsname : str, optional
            name of the Calculation class in the current python code, default 'Calculation'

        calculationsname : str, optional
            name of the list of Calculations generated

        keeper : str, optional
            name of the CalculationKeeper instance used for the calculations

        Returns
        -------

        str:
            python script

        """
        if only_incomplete is False:
            calculations = self._calculations
        else:
            calculations = self.get_incomplete()
        return get_pycode(calculations, with_keeper=with_keeper, header=header, clsname=clsname,
                          keeper=keeper, calculationsname=calculationsname)

    def get_incomplete(self):
        """Return a list of all incompleted calculations"""
        calculations = []
        for calc in self._calculations:
            try:
                calc.check()
            except CalculationIncompleteError:
                calculations.append(calc)
        return calculations
