import platform

from setuptools.command.build_ext import build_ext as build_ext_orig
from setuptools import Extension, setup


class CTypesExtension(Extension):
    pass


cubiomes_sources = [
    "src/cubiomes/finders.c",
    "src/cubiomes/generator.c",
    "src/cubiomes/util.c",
    "src/cubiomes/biomenoise.c",
    "src/cubiomes/biometree.c",
    "src/cubiomes/layers.c",
    "src/cubiomes/noise.c",
    "src/cubiomes/quadbase.c"
]

extensions = [
    CTypesExtension("seedhelper.libstructureshelper",
                    sources=["src/c_seedhelper/structures_helper.c"] + cubiomes_sources)]


class ExtBuilder(build_ext_orig):
    def get_export_symbols(self, ext):
        return ext.export_symbols

    def get_ext_filename(self, ext_name):
        if platform.system() == "Windows":
            return ext_name + ".dll"
        else:
            return ext_name + ".so"


setup(
    name="seedhelper",
    py_modules=["seedhelper.structures"],
    ext_modules=extensions,
    cmdclass={"build_ext": ExtBuilder},
    package_dir={"": "src"},
)
