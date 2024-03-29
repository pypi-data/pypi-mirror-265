from copy import deepcopy

import attr
import numpy as np
from scipy.spatial.transform import Rotation

from .data.atomic_data import atomic_mass


@attr.s(frozen=True)
class Atom:
    """
    Representation of an individual atomas (<element> <X> <Y> <Z>)

    .. rubric:: Examples

    >>> Atom(element='H', x=0, y=0, z=0)
    {'element': 'H', 'x': 0, 'y': 0, 'z': 0}

    >>> Atom('F', 0, 0, 1.97)
    {'element': 'F', 'x': 0, 'y': 0, 'z': 1.97}

    .. rubric:: Returns

    atom : object
        object like dict {'element': str, 'x': float, 'y': float, 'z': float}

    .. rubric:: Raises

    ValueError
        format MUST be (str, float, float, float) with NOT empty filed
    """

    element: str = attr.ib()
    x: int = attr.ib()
    y: int = attr.ib()
    z: int = attr.ib()

    # ===============================================================
    # VALIDATORS
    # ===============================================================
    @element.validator
    def _check_valid_element(self, element, value):
        """Element: Must be valid NOT empty alphanumeric character"""
        if not value.isalnum():
            raise ValueError(
                "\n\nMust be valid NOT empty alphanumeric character"
                f"\nyou get --> '{value}'\n"
            )

    @x.validator
    @y.validator
    @z.validator
    def _check_valid_point(self, coordinate, value):
        """Coordinate: Must be valid float"""
        if not isinstance(value, (int, float)):
            raise ValueError(
                "\n\nMust be valid NOT empty float"
                f"\nyou get --> '{value}' with type: '{type(value).__name__}'"
            )

    # ===============================================================
    # PROPERTIES
    # ===============================================================
    @property
    def atomic_mass(self) -> list:
        """Atomic mass of the atom"""
        return atomic_mass(self.element)

    @property
    def symbol(self) -> list:
        """Atomic symbol of the atom"""
        return self.element

    # ===============================================================
    # MAGIC METHODS
    # ===============================================================
    def __str__(self):
        """Magic method '__str__' to print the object as a dictionary"""
        return str(attr.asdict(self))


# -------------------------------------------------------------
@attr.s(frozen=False)
class Molecule:
    """
    Create a Molecule that is at least ONE atom.
    The format of the INPUT coordinates must be:

    {"atoms": [(<element> <X> <Y> <Z>), (<element> <X> <Y> <Z>), ...]}

    .. rubric:: Parameters

    atoms : list[tuple(str, float, float, float)]
        Cartesian coordinates of each atom, by default empty list

    charge : int
        total molecular/atomic charge, by default zero (0)

    multiplicity : int
        larger than zero, by defaul one (1)
    """

    _atoms = attr.ib()
    _charge: int = attr.ib(default=0)
    _multiplicity: int = attr.ib(default=1)

    # ===============================================================
    # VALIDATORS
    # ===============================================================
    @_atoms.validator
    def _cehck_valid_atoms(self, attribute, atoms):
        """check if the atoms are valid"""
        for line, atom in enumerate(atoms):
            try:
                Atom(*atom)
            except (ValueError, TypeError) as err:
                raise TypeError(
                    f"\n\n{err}\ncoordinates format must be a list of tuple: "
                    "[(str, float, float, float), ...]"
                    f"\ncheck atom number {line + 1} --> {atom}\n"
                    f"from --> {atoms}\n"
                )

    @_charge.validator
    def _check_valid_charge(self, attribute, charge):
        """check if the charge is valid"""
        if not isinstance(charge, int):
            raise ValueError(
                "\n\ncharge must be an integer "  # noqa
                f"\nyou get --> 'charge = {charge}'\n"
            )

    @_multiplicity.validator
    def _check_valid_multiplicity(self, attribute, multiplicity):
        """check if the multiplicity is valid"""
        if not isinstance(multiplicity, int) or multiplicity < 1:
            raise ValueError(
                "\n\nmultiplicity must be an integer larger than zero (0)"
                f"\nyou get --> 'multiplicity = {multiplicity}'\n"
            )

    # ===============================================================
    # CONSTRUCTORS
    # ===============================================================
    @classmethod
    def from_dict(cls, atoms_dict):
        "Dictionary type: {'atoms': [(<element> <X> <Y> <Z>), ...]}"
        if "atoms" not in atoms_dict:
            # FIXME: KeyError does not support \n
            raise TypeError(
                "\n\nThe key 'atoms' is casesensitive"
                "\n{'atoms': [(<element> <X> <Y> <Z>), ...]}"
                f"\nyou get {atoms_dict}\n"
            )
        atoms = atoms_dict.get("atoms")
        charge = atoms_dict.get("charge", 0)
        multiplicity = atoms_dict.get("multiplicity", 1)
        return cls(atoms, charge, multiplicity)

    # ===============================================================
    # MAGIC METHODS
    # ===============================================================
    def __add__(self, other) -> object:
        """Magic method '__add__' to add two molecules, return a new one"""
        return self.add_molecule(other)

    def __mul__(self, value: int):
        """Magic method '__mul__' to multiply a molecule by a number"""
        return value * self

    def __rmul__(self, value: int):
        """
        Replicate a molecule.
        summing or multiplying Molecule classes produce a Cluster class

        Parameters
        ----------
        value : int
            quantity to replicate Molecue

        Return
        ------
        Cluster : object
        """
        if not isinstance(value, int) or value < 1:
            raise ValueError(
                "\nMultiplier must be and integer larger than zero"
                f"\ncheck --> '{value}'"
            )

        new_cluster = deepcopy(self)
        for _ in range(value - 1):
            new_cluster = new_cluster.add_molecule(deepcopy(self))

        return new_cluster

    def __str__(self):
        """Magic method '__str__' to print the Molecule in XYZ format"""
        return self.xyz

    # ===============================================================
    # PROPERTIES
    # ===============================================================
    @property
    def atoms(self) -> list:
        """Return the list of atoms"""
        return self._atoms

    @atoms.setter
    def atoms(self, *args, **kwargs) -> None:
        """Set the list of atoms"""
        raise AttributeError(
            "\n\nyou cannot reset 'atoms'. Consider create a new instance \n"
        )

    @property
    def write_atoms(self) -> str:
        """Printing Molecule coordinates using XYZ format"""
        write_coordinates = ""
        for atom in self.atoms:
            write_coordinates += f"""{atom[0]:<6}"""
            write_coordinates += f"""\t{atom[1]:> 15.8f}"""
            write_coordinates += f"""\t{atom[2]:> 15.8f}"""
            write_coordinates += f"""\t{atom[3]:> 15.8f}\n"""

        return write_coordinates

    @property
    def atomic_masses(self) -> list:
        """Atomic mass of the molecule"""
        return [Atom(*atom).atomic_mass for atom in self.atoms]

    @property
    def charge(self) -> int:
        """Total molecular/atomic charge"""
        return self._charge

    @charge.setter
    def charge(self, new_charge) -> int:
        """Set the total molecular/atomic charge"""
        if not isinstance(new_charge, int):
            raise ValueError(
                "\n\ncharge must be an integer "
                f"\nyou get --> 'charge = {new_charge}'\n"
            )
        self._charge = new_charge

    @property
    def coordinates(self) -> list:
        """Return the list of coordinates"""
        return [c[1:] for c in self.atoms]

    @property
    def elements(self) -> list:
        """Show a list of unique symbols

        .. rubric:: Returns

        list
            list of unique symbols
        """
        return list(set(self.symbols))

    @property
    def multiplicity(self) -> int:
        """Return the multiplicity"""
        return self._multiplicity

    @multiplicity.setter
    def multiplicity(self, new_multiplicity) -> int:
        """Set the multiplicity"""
        if not isinstance(new_multiplicity, int) or new_multiplicity < 1:
            raise ValueError(
                "\n\nmultiplicity must be an integer larger than zero (0)"
                f"\nyou get --> 'multiplicity = {new_multiplicity}'\n"
            )
        self._multiplicity = new_multiplicity

    @property
    def numbering_atoms(self) -> str:
        """show atom number line by line

        .. rubric:: Returns

        str
            atom number line by line
        """
        numbered_atoms = list()
        for i in range(self.total_atoms):
            line = list(self.atoms[i])
            line[0] = f"\r  atom #{i} --> {line[0]:<6}"
            line[1] = f"{line[1]:> 15.8f}"
            line[2] = f"{line[2]:> 15.8f}"
            line[3] = f"{line[3]:> 15.8f}"
            numbered_atoms.append("".join(line))

        return "\n".join(numbered_atoms)

    @property
    def symbols(self) -> list:
        """Return the list of symbols"""
        return [str(s[0]).title() for s in self.atoms]

    @property
    def total_atoms(self) -> int:
        """Return the total number of atoms"""
        return len(self.atoms)

    @property
    def total_mass(self) -> float:
        """Return the total mass of the molecule"""
        return sum(self.atomic_masses)

    @property
    def center_of_mass(self) -> tuple:
        """Center of mass for a N-body problem. `Jacobi coordinates`_

        .. rubric:: Notes

        total mass for dummy atoms (not in the Periodic Table) is equal
        to ONE (1)

        .. rubric:: Returns

        tuple : (float, float, float)
            List of N 3D tuples, where N is equal to the number of atoms

        .. _Jacobi coordinates:
            https://en.wikipedia.org/wiki/Jacobicoordinates
        """

        total_mass = 1 if not self.total_mass else self.total_mass

        return tuple(
            np.dot(
                np.asarray(self.atomic_masses),
                np.asarray(self.coordinates),
            )
            / total_mass
        )

    @property
    def principal_axes(self) -> list:
        """Principal axes for according to Jacobi coordinates"""
        return [
            tuple(c)
            for c in (  # noqa
                np.asarray(self.coordinates) - np.asarray(self.center_of_mass)
            )
        ]

    @property
    def xyz(self) -> str:
        """Printing Molecule coordinates using XYZ format"""
        comments = (
            f"-- charge={self.charge:<-g} and "
            f"multiplicity={self.multiplicity:<g} --"
        )
        write_xyz = f"""\t{self.total_atoms}\n{comments:<s}\n"""
        for atom in self.atoms:
            write_xyz += f"""{atom[0]:<6}"""
            write_xyz += f"""\t{atom[1]:> 15.8f}"""
            write_xyz += f"""\t{atom[2]:> 15.8f}"""
            write_xyz += f"""\t{atom[3]:> 15.8f}\n"""

        return write_xyz

    def add_atoms(self, new_atoms: list) -> object:
        """adding extra atoms can NOT be MOVED or ROTATED

        .. rubric:: Parameters

        other : list
            cartesian coordinates; like [(<element>, <X>, <Y>, <Y>), ...]

        .. rubric:: Returns

        Molecule : object
            a new Molecule

        .. rubric:: Raises

        TypeError
            for anything else
        """
        if not isinstance(new_atoms, list):
            raise TypeError(
                f"\n\ncoordinates format must be a list of tuple: "
                "[(str, float, float, float), ...]"
                f"check --> \n{new_atoms}\n"
            )

        total_atoms: list = self.atoms + new_atoms
        return self.__class__(total_atoms)

    def add_molecule(self, other) -> object:
        """adding molecule return a new Cluster object"""
        if not isinstance(other, Molecule):
            raise TypeError(
                "\nOnly type 'Molecule', list or dict could be added"
                f"\nyou have a type: '{type(other)}', check: \n{other}"
            )
        return Cluster(self, other)

    def get_atom(self, atom: int) -> list:
        """
        Getting catesian coordinate for an atom

        .. rubric:: Parameters

        atom : int
            atom index

        .. rubric:: Returns

        list
            ["element", "X", "Y", "Z"]

        .. rubric:: Raises

        IndexError
        """
        if not isinstance(atom, int) or atom >= self.total_atoms:
            raise IndexError(
                f"\nMolecule with {self.total_atoms} total atoms "
                f"and index [0-{self.total_atoms - 1}]"
                f"\n atom index must be less than {self.total_atoms}"
                f"\nCheck! You want to get atom with index {atom}"
            )
        return self.atoms[atom]

    def remove_atom(self, atom: int) -> object:
        """remove one atom"""
        if not isinstance(atom, int) or atom >= self.total_atoms:
            raise IndexError(
                f"\nMolecule with {self.total_atoms} total atoms "
                f"and index [0-{self.total_atoms - 1}]"
                f"\n atom index must be less than {self.total_atoms}"
                f"\nCheck! You want to remove atom with index '{atom}'"
            )

        new_atoms: list = list(self.atoms)

        del new_atoms[atom]

        return self.__class__(new_atoms)


# -------------------------------------------------------------
class Cluster(Molecule):
    """
    Create a Cluster with molecules/atoms to move and rotate
    using spherical boundary conditions (SBC).
    The format of the INPUT coordinates is as follows (any):

    1. Dictionary type: {"atoms": [(<element> <X> <Y> <Z>), ...]}
    2. List type: [(<element> <X> <Y> <Z>), ...]
    3. Molecule/Cluster type (Objects)

    .. rubric:: Parameters

    args : List, Dict, Molecule, Cluster
        coordinates of each molecule/atom comma separates (support +,-,*)
    freeze_molecule : integer, optional
        fixing molecule to NOT move or rotate, by default NEGATIVE
        integer means all molecules can be moved freely
    sphere_radius : float, optional
        radius for the spherical boundary condition, by default None
    sphere_center : tuple, optional
        Center of the sphere, by default (0, 0, 0)
    seed : int, optional
        seed to initialize the random generator function, by default None

    .. rubric:: Raises

    TypeError
        for a wrong input argument
    """

    def __init__(
        self,
        *args,
        freeze_molecule: list = None,
        sphere_radius: float = None,
        sphere_center: tuple = (0, 0, 0),
        seed: int = None,
    ):
        self._cluster_dict = dict()
        self._multiplicity = 1
        self._charge = 0

        # fixing molecule to NOT move or rotate
        # initialize with an empty list
        self._freeze_molecule = (  # noqa
            [] if freeze_molecule is None else freeze_molecule
        )

        self._sphere_radius = sphere_radius
        self._sphere_center = sphere_center

        # initialize random generator
        if not seed:
            self._seed = np.random.randint(0, 999999)
        else:
            self._seed: int = seed

        # ----------------------------------------------------
        # attrs post-initialization

        cluster_atoms: list = list()

        # for count, mol in enumerate(args):
        for mol in args:
            size: int = len(self._cluster_dict)
            if isinstance(mol, Cluster):
                for j in mol._cluster_dict:
                    self._cluster_dict[size + j] = mol._cluster_dict[j]
                self._charge += mol.charge
                cluster_atoms += mol.atoms
                # restarting the loop
                continue
            elif isinstance(mol, Molecule):
                new_molecule = deepcopy(mol)
            elif isinstance(mol, dict):
                new_molecule = Molecule.from_dict(mol)
            elif isinstance(mol, list):
                new_molecule = Molecule(mol)
            else:
                raise TypeError(
                    "\nOnly type 'Molecule', list or dict to initialize"
                    "\n\t- Dict: {'atoms': [(<element> <X> <Y> <Z>), ...]}"
                    "\n\t- List: [(<element> <X> <Y> <Z>), ...]"
                    f"\nyou have a NOT valid '{type(mol)}', check: \n{mol}"
                )

            cluster_atoms += new_molecule.atoms
            # ! how is computed the cluster total multiplicity?
            self._charge += new_molecule.charge
            self._cluster_dict[size] = new_molecule

        # initializing Cluster as a 'Molecule' (sum of all individual ones)
        super().__init__(
            atoms=cluster_atoms,
            charge=self.charge,
            multiplicity=self.multiplicity,
        )

    # ===============================================================
    # MAGIC METHODS
    # ===============================================================
    def __add__(self, other):
        """Adding two molecules/clusters, return a new Cluster object"""
        # ! Martin
        # ! ver en que puede se diferenciar de Molecule
        # * la idea es que debe ser similar para que ambos
        # * creen una nueva instancia nueva de Cluster
        return self.add_molecule(other)

    def __mul__(self, value: int):
        """multiply the cluster by a number"""
        return value * self

    def __rmul__(self, value: int):
        """to replicate a molecule

        Parameters
        ----------
        value : int
            quantity to replicate Molecue

        Return
        ------
        Cluster : object
            summing or multiplying Molecule classes produce a Cluster class
        """
        if value < 1 or not isinstance(value, int):
            raise ValueError(
                "\nMultiplier must be and integer larger than zero"
                f"\ncheck --> '{value}'"
            )

        new_cluster = deepcopy(self)
        for _ in range(value - 1):
            new_cluster = new_cluster.add_molecule(deepcopy(self))

        return new_cluster

    def __str__(self):
        """print the cluster"""
        cluster_dict: dict = self._cluster_dict

        cluster_string: str = (
            f"Cluster of ({self.total_molecules}) molecules"
            f" and ({self.total_atoms}) total atoms\n"
        )
        for key, molecule in cluster_dict.items():
            atoms = molecule.atoms
            cluster_string += f" #{key}: molecule with {len(atoms)} atoms:\n"
            cluster_string += f"     --> atoms: {atoms}\n"
            charge = molecule.charge
            cluster_string += f"     --> charge: {charge:>+}\n"
            multiplicity = molecule.multiplicity
            cluster_string += f"     --> multiplicity: {multiplicity}\n"

        return cluster_string

    # ===============================================================
    # PROPERTIES
    # ===============================================================
    @property
    def cluster_dictionary(self) -> dict:
        """return the cluster dictionary"""
        return self._cluster_dict

    @property
    def freeze_molecule(self) -> int:
        """return a list with freezed molecules"""
        return self._freeze_molecule

    @freeze_molecule.setter
    def freeze_molecule(self, values) -> None:
        """set the freeze molecules"""
        if isinstance(values, list):
            self._freeze_molecule = values
        else:
            self._freeze_molecule = [values]

    @property
    def random_generator(self) -> np.random.Generator:
        """return the random generator"""
        # self._random_gen: np.random.Generator = np.random.default_rng(seed)
        return np.random.default_rng(self.seed)

    @property
    def seed(self) -> int:
        """return the seed for the random generator"""
        return self._seed

    @seed.setter
    def seed(self, new_seed: int) -> None:
        """set the seed for the random generator"""
        self._seed = new_seed
        self._random_gen = np.random.default_rng(new_seed)

    @property
    def sphere_center(self) -> tuple:
        """return the sphere center for the Cluster boundary conditions"""
        return self._sphere_center

    @sphere_center.setter
    def sphere_center(self, new_center: tuple) -> None:
        """set the sphere center for the Cluster boundary conditions"""
        if len(new_center) != 3:
            raise ValueError(
                "\n\nThe Sphere center must be a tuple with three elements: "
                "(float, float, float)"
                f"\nplease, check: '{new_center}'\n"
            )

        self._sphere_center = new_center

    @property
    def sphere_radius(self) -> float:
        """return the sphere radius for the Cluster boundary conditions"""
        return self._sphere_radius

    @sphere_radius.setter
    def sphere_radius(self, new_radius: float) -> None:
        """set the sphere radius for the Cluster boundary conditions"""
        if not isinstance(new_radius, (int, float)) or new_radius < 0.9:
            raise ValueError(
                "\n\nThe Sphere  Radius must be larger than 1 Angstrom"
                f"\nplease, check: '{new_radius}'\n"
            )

        self._sphere_radius = new_radius

    @property
    def total_molecules(self) -> int:
        """return the total number of molecules in the cluster"""
        return len(self._cluster_dict)

    # ===============================================================
    # METHODS
    # ===============================================================
    @staticmethod
    def overlapping(
        first_coordinates: list,
        second_coordinates: list,
        max_closeness: float = 1.0,
    ) -> bool:
        """pair-wise checking if any overlapping among points
        with a radius defined by `max_closeness`

        .. rubric:: Parameters

        first_coordinates : list
            list of tuples [(float, float, float), ...]
        second_coordinates : list
            list of tuples [(float, float, float), ...]
        max_closeness : float, optional
            maximun closeness between two pairs, by default 1.0

        .. rubric:: Returns

        bool
            True if two point are closer than `max_closeness`
        """
        # ! Martin
        # ! itertools para optimizar los for
        for first_atom in first_coordinates:
            for second_atom in second_coordinates:
                distance = np.linalg.norm(
                    np.asarray(first_atom) - np.asarray(second_atom)
                )

                if distance < max_closeness:
                    return True

        return False

    def add_molecule(self, other: Molecule) -> object:
        new_cluster = deepcopy(self)
        return self.__class__(
            new_cluster,
            other,
            freeze_molecule=new_cluster.freeze_molecule,
            sphere_radius=new_cluster.sphere_radius,
            sphere_center=new_cluster.sphere_center,
        )

    def initialize_cluster(self, max_closeness: float = 1.0) -> object:
        """Create a new cluster object which any atom is overlapped

        .. rubric:: Parameters

        max_closeness : float, optional
            maximun closeness between two pairs, by default 1.0

        .. rubric:: Returns

        Cluster : object
            returns a new Cluster object
        """
        # center of mass coordinates
        sc_x = self.sphere_center[0]
        sc_y = self.sphere_center[1]
        sc_z = self.sphere_center[2]

        # initializing a new cluster moving the first molecule
        # to the center of the cluster sphere
        molecule = self.get_molecule(0)
        new_cluster = molecule.translate(0, sc_x, sc_y, sc_z)

        for i in range(1, self.total_molecules):
            # moving the next single molecule into the cluster sphere
            molecule = self.get_molecule(i).translate(0, sc_x, sc_y, sc_z)

            if Cluster.overlapping(  # noqa
                molecule.coordinates, new_cluster.coordinates
            ):
                new_cluster += molecule
                new_cluster = new_cluster.move_molecule(
                    i,
                    max_step=None,
                    max_rotation=None,
                    max_closeness=max_closeness,
                )
            else:
                new_cluster += molecule

        return Cluster(
            new_cluster,
            freeze_molecule=self.freeze_molecule,
            sphere_radius=self.sphere_radius,
            sphere_center=self.sphere_center,
        )

    def get_molecule(self, molecule: int):
        """extract a molecule from the cluster and return a new Cluster"""
        if molecule not in self.cluster_dictionary:
            raise IndexError(
                f"\nMolecule with {self.total_molecules} total molecules "
                f"and index [0-{self.total_molecules - 1}]"
                f"\nmolecule index must be less than {self.total_molecules}"
                f"\nCheck! You want to get molecule with index {molecule}"
            )

        cluster_dict: dict = deepcopy(self).cluster_dictionary
        new_molecule: Molecule = cluster_dict.pop(molecule)

        return self.__class__(
            new_molecule,
            freeze_molecule=self.freeze_molecule,
            sphere_radius=self.sphere_radius,
            sphere_center=self.sphere_center,
        )

    def move_molecule(
        self,
        molecule: int = 0,
        max_step: float = None,
        max_rotation: float = None,
        max_closeness: int = 1.0,
    ) -> object:
        """Moving (translating and rotating) randomly without overlapping
        any atom

        .. rubric:: Parameters

        molecule : int, optional
            molecule to move randomly, by default molecule with index zero (0)
        max_step : float, optional
            maximun value for any translation, by default None
        max_rotation : float, optional
            maximun angle fro any rotation, by default None
        max_closeness : float
            maximun closeness between any pair of atoms, by default 1.0 A

        .. rubric:: Returns

        object : Cluster
            returns a Cluster object whit a molecule moved to a random place
            without overlapping any other

        .. rubric:: Raises

        AttributeError : OverlappingError
            After serching for max_overlap_cycle and no place found for the
            molecule without overlapping any other
        """
        if not isinstance(max_closeness, (int, float)) or max_closeness < 0.1:
            raise ValueError(
                "\n\n Maximun closeness between any pair of atom must be"
                f" larger than '0.1' Angstrom\nPlease, check '{max_closeness}'"
            )

        if not max_step or not isinstance(max_step, (int, float)):
            max_step = 1.1 * max_closeness

        if not max_rotation or not isinstance(max_rotation, (int, float)):
            max_rotation = 30

        molecule_to_move: Cluster = self.get_molecule(molecule)

        cluster_without_molecule: Cluster = self.remove_molecule(molecule)
        cluster_coordinates: Cluster = cluster_without_molecule.coordinates

        random_gen: np.random.Generator = self.random_generator

        max_overlap_cycle: int = 10000

        for count in range(max_overlap_cycle):

            if count % 10 == 0:
                max_step *= 1.1
                max_rotation *= 1.1

            # angle between [0, max_rotation) degrees
            rotation_x = random_gen.uniform(-1, 1) * max_rotation
            rotation_y = random_gen.uniform(-1, 1) * max_rotation
            rotation_z = random_gen.uniform(-1, 1) * max_rotation

            # moving between [-max_step, +max_step] Angstrom
            tranlation_x = max_step * random_gen.uniform(-1, 1)
            tranlation_y = max_step * random_gen.uniform(-1, 1)
            tranlation_z = max_step * random_gen.uniform(-1, 1)

            new_molecule: Cluster = molecule_to_move.translate(
                0,
                tranlation_x,
                tranlation_y,
                tranlation_z,
            ).rotate(
                0,
                rotation_x,
                rotation_y,
                rotation_z,
            )

            molecule_coordinates: list = new_molecule.coordinates

            overlap: bool = Cluster.overlapping(
                molecule_coordinates,
                cluster_coordinates,
                max_closeness=max_closeness,
            )

            if not overlap:
                break
        # if overlapping and max_overlap_cycle reached
        else:
            raise AttributeError(
                "\n\n *** Overlapping Error ***"
                "\nat least one atom is overlapped with a distance"
                f" less than '{max_closeness}' Angstroms"
                "\nfor a cluster into a sphere of radius"
                f" '{self.sphere_radius}' Angstroms"
                # f"\nPlease, check: \n\n{self.xyz}"
            )

        cluster_dict: dict = deepcopy(self.cluster_dictionary)
        cluster_dict[molecule] = new_molecule

        return self.__class__(
            *cluster_dict.values(),
            freeze_molecule=self.freeze_molecule,
            sphere_radius=self.sphere_radius,
            sphere_center=self.sphere_center,
        )

    def remove_molecule(self, molecule: int) -> object:
        """Removing molecule from cluster"""
        if molecule not in self.cluster_dictionary:
            raise IndexError(
                f"\nMolecule with {self.total_molecules} total atoms "
                f"and index [0-{self.total_molecules - 1}]"
                f"\n molecule index must be less than {self.total_molecules}"
                f"\nCheck! You want to remove molecule with index {molecule}"
            )
        new_cluster: Cluster = deepcopy(self)
        new_cluster_dict: dict = new_cluster.cluster_dictionary
        del new_cluster_dict[molecule]
        # ! Martin
        # ! tener cuidado con el self porque se puede compartir Molecule
        # ! o Cluster
        # ! Preferible usar Cluster(...)
        return self.__class__(
            *new_cluster._cluster_dict.values(),
            freeze_molecule=new_cluster.freeze_molecule,
            sphere_radius=new_cluster.sphere_radius,
            sphere_center=new_cluster.sphere_center,
        )

    def rotate(  # noqa
        self, molecule: int = None, x: float = 0, y: float = 0, z: float = 0
    ):
        """
        Returns a NEW Cluster Object with a ROTATED molecule (CLOCKWISE)
        around molecule internal center of mass
        """
        # avoiding to rotate a FROZEN molecule
        if molecule in self.freeze_molecule:
            return deepcopy(self)

        if (
            not isinstance(molecule, int)
            or molecule >= self.total_molecules
            or molecule < 0
        ):
            raise IndexError(
                f"\nMolecule with {self.total_molecules} total molecules "
                f"and index [0-{self.total_molecules - 1}]"
                f"\nmolecule index must be less than {self.total_molecules}"
                f"\nCheck! You want to remove molecule with index {molecule}"
            )

        molecule_to_rotate: Molecule = self._cluster_dict[molecule]
        molecule_symbols: list = molecule_to_rotate.symbols

        # avoid any rotatation attemp for a single atom system
        if len(molecule_symbols) <= 1:
            return deepcopy(self)

        molecule_center_of_mass = molecule_to_rotate.center_of_mass
        molecule_principal_axes = molecule_to_rotate.principal_axes

        # rotate around sphere center
        x, y, z = np.asarray(self.sphere_center) + np.asarray([x, y, z])

        rotation_matrix = Rotation.from_euler(
            "xyz",
            [x, y, z],
            degrees=True,
        ).as_matrix()

        rotatedcoordinates = (
            np.dot(molecule_principal_axes, rotation_matrix)  # noqa
            + molecule_center_of_mass
        )

        rotated_molecule = list()
        for i, atom in enumerate(molecule_symbols):
            rotated_molecule.append(  # noqa
                tuple([atom] + rotatedcoordinates[i].tolist())
            )

        new_cluster = deepcopy(self)
        new_cluster._cluster_dict[molecule] = Molecule(rotated_molecule)

        return self.__class__(
            *new_cluster._cluster_dict.values(),
            freeze_molecule=new_cluster.freeze_molecule,
            sphere_radius=new_cluster.sphere_radius,
            sphere_center=new_cluster.sphere_center,
        )

    def translate(  # noqa
        self, molecule: int = None, x: float = 0, y: float = 0, z: float = 0
    ):
        """Returns a NEW Molecule Object with a TRANSLATED fragment"""
        # avoiding to rotate a FROZEN molecule
        if molecule in self.freeze_molecule:
            return deepcopy(self)

        if (
            not isinstance(molecule, int)
            or molecule >= self.total_molecules
            or molecule < 0
        ):
            raise IndexError(
                f"\nMolecule with {self.total_molecules} total molecules "
                f"and index [0-{self.total_molecules - 1}]"
                f"\nmolecule index must be less than {self.total_molecules}"
                f"\nCheck! You want to remove molecule with index {molecule}"
            )

        molecule_to_move: Molecule = self._cluster_dict[molecule]
        molecule_symbols: list = molecule_to_move.symbols

        molecule_center_of_mass = molecule_to_move.center_of_mass
        molecule_principal_axes = molecule_to_move.principal_axes

        translatedcoordinates = np.asarray(  # noqa
            molecule_center_of_mass
        ) + np.asarray([x, y, z])

        # checking if the new coordinates are into the boundary conditions
        # if it is out of our sphere, we rescale it to match the sphere radius
        distance: float = np.linalg.norm(
            translatedcoordinates - np.asarray(self.sphere_center)
        )
        if self.sphere_radius and (distance > self.sphere_radius):

            max_distance: float = self.sphere_radius / np.linalg.norm(
                translatedcoordinates - np.asarray(self.sphere_center)
            )

            # rescaling to match radius
            translatedcoordinates = max_distance * translatedcoordinates + (
                1 - max_distance
            ) * np.asarray(self.sphere_center)

        translatedcoordinates = molecule_principal_axes + translatedcoordinates

        translated_molecule = list()
        for i, atom in enumerate(molecule_symbols):
            translated_molecule.append(
                tuple([atom] + translatedcoordinates[i].tolist())
            )

        new_cluster = deepcopy(self)
        new_cluster._cluster_dict[molecule] = Molecule(translated_molecule)

        return self.__class__(
            *new_cluster._cluster_dict.values(),
            freeze_molecule=new_cluster.freeze_molecule,
            sphere_radius=new_cluster.sphere_radius,
            sphere_center=new_cluster.sphere_center,
        )

    def center_radius_sphere(self, add_tolerance_radius: float = 1.0):
        """
        Define a spherical outline that contains our cluster

        .. rubric:: Parameters

        add_tolerance_radius : float
            Tolerance with the radius between the mass center to the
            furthest atom

        .. rubric:: Returns

        sphere_center : tuple
            Mass center of the biggest molecule
        sphere_radius : float
            Radius between the sphere center to the furthest atom

        """
        # ----------------------------------------------------------------
        # Verfication
        if not isinstance(add_tolerance_radius, float):
            raise TypeError(
                "\n\nThe tolerance for radius is not a float"
                f"\nplease, check: '{type(add_tolerance_radius)}'\n"
            )
        # ----------------------------------------------------------------
        # Initialize cluster to avoid overlaping, then can calculate of
        # radius
        self.initialize_cluster()
        # ---------------------------------------------------------------
        maximum_r_cm = 0.0
        molecule = 0
        max_atoms = 0
        # ---------------------------------------------------------------
        # The biggest molecule
        molecules_number: Cluster = self.total_molecules
        for i in range(molecules_number):
            if self.get_molecule(i).total_atoms > max_atoms:
                max_atoms = self.get_molecule(i).total_atoms
                molecule = i
        # ---------------------------------------------------------------
        # Define sphere center above the cm of the biggest molecule
        center = self.get_molecule(molecule).center_of_mass
        # ---------------------------------------------------------------
        # Radius between the sphere center to the furthest atom
        for xyz in self.coordinates:
            temporal_r = np.linalg.norm(
                np.asarray(self._sphere_center) - np.asarray(xyz)
            )
            if temporal_r > maximum_r_cm:
                maximum_r_cm = temporal_r
        # ---------------------------------------------------------------
        # Move the biggest molecule to the first position in the cluster
        # object, if is necessary
        if molecule != 0:
            new_geom = dict()
            for i in range(molecules_number):
                if i == 0:
                    new_geom[i] = self.get_molecule(molecule)
                elif i == molecule:
                    new_geom[i] = self.get_molecule(0)
                else:
                    new_geom[i] = self.get_molecule(i)
            # ---------------------------------------------------------------
            # Instantiation of Cluster object with radius and center sphere
            return Cluster(
                *new_geom.values(),
                sphere_center=center,
                sphere_radius=maximum_r_cm,
            )
        else:
            return Cluster(
                *self._cluster_dict.values(),
                sphere_center=center,
                sphere_radius=maximum_r_cm,
            )


# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
