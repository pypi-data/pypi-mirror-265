import os
from setuptools import Extension, setup, find_packages
from setuptools.command.build_ext import build_ext
from pathlib import Path


class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])


class CMakeBuild(build_ext):
    def run(self):
        ext = self.extensions[0]
        build_temp = Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        extdir = Path(self.get_ext_fullpath(ext.name))
        extdir.mkdir(parents=True, exist_ok=True)

        script_path = os.path.abspath(os.path.dirname(__file__))
        cmake_list_dir = script_path + "/src/"
        build_dir = os.path.join(script_path, "build")
        library_path = "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(
            extdir.parent.absolute()
        )
        self.spawn(["cmake", cmake_list_dir, library_path, "-B", build_dir])
        self.spawn(
            [
                "cmake",
                "--build",
                build_dir,
                "--target all",
                "--",
                "-j",
            ]
        )


with open("README.md", "r") as fh:
    long_description = fh.read()
short_description = "todo"


setup(
    name="pyfdmss",
    version="0.0.3",
    description=short_description,
    long_description=long_description,
    author="Kirill M. Gerke, Marina V. Karsanina, Andrey A. Ananev, Andrey Zubov",
    license="GPLv3",
    author_email="andrey.ananev@phystech.edu",
    ext_modules=[CMakeExtension("pyfdmss")],
    cmdclass={"build_ext": CMakeBuild},
    packages=find_packages("src"),
    # package_dir={"": "src"},
    package_dir={"": "src"},
    package_data={
        "fdmss_lib": ["./src/*", "./include/*", "./CMakeLists.txt"],
        "pyfdmss": ["./*.cpp"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3 :: Only",
        # 'Operating System :: OS Independent',
    ],
)
