import ctypes
import pathlib

lib_file = pathlib.Path(__file__).parent / "libstructureshelper.so"
_structures_helper = ctypes.CDLL(str(lib_file))


class Pos(ctypes.Structure):
    _fields_ = [('x', ctypes.c_int),
                ('z', ctypes.c_int)]


class Pos3(ctypes.Structure):
    _fields_ = [('x', ctypes.c_int),
                ('z', ctypes.c_int),
                ('z', ctypes.c_int)]


# For recursion
class Piece(ctypes.Structure):
    pass


class Piece(ctypes.Structure):
    _fields_ = [('name', ctypes.POINTER(ctypes.c_char)),
                ('pos', Pos3),
                ('bb0', Pos3),
                ('bb1', Pos3),
                ('rot', ctypes.c_uint8),
                ('depth', ctypes.c_int8),
                ('type', ctypes.c_int8),
                ('next', ctypes.POINTER(Piece))]


class FindElytrasArguments(ctypes.Structure):
    _fields_ = [('seed', ctypes.c_uint64),
                ('mc_version', ctypes.c_char_p),
                ('x', ctypes.c_int),
                ('z', ctypes.c_int),
                ('r', ctypes.c_int)]


_structures_helper.get_elytras_positions.argtypes = (FindElytrasArguments, ctypes.POINTER(ctypes.c_int))
_structures_helper.get_elytras_positions.restype = ctypes.POINTER(Piece)


def get_elytras_positions(seed: int, mc_version: str = '1.20', x: int = 0, z: int = 0, r: int = 10000) -> list[Piece]:
    arguments = FindElytrasArguments(seed=seed, mc_version=mc_version.encode('utf-8'), x=x, z=z, r=r)
    n_ships = ctypes.c_int(0)
    output_ptr = _structures_helper.get_elytras_positions(arguments, ctypes.byref(n_ships))

    if not output_ptr:
        return []

    output_size = n_ships.value
    output_array = (Piece * output_size).from_address(ctypes.addressof(output_ptr.contents))
    output_list = [output_array[i] for i in range(output_size)]

    return output_list
