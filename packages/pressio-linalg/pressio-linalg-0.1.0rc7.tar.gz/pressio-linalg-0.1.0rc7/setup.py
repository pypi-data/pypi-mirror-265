#!/usr/bin/env python3

# Authors:
# Francesco Rizzi  (francesco.rizzi@ng-analytics.com)
# Patrick Blonigan (pblonig@sandia.gov)
# Eric Parish      (ejparis@sandia.gov)
# John Tencer      (jtencer@sandia.gov)

import os
import sys
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install as _install

topdir = os.path.dirname(os.path.abspath(__file__))

pressio_python_only = True
pressio_cpp_bindings = False
pressio_trilinos = False
pressio_install_trilinos = False
pressio_find_trilinos = False
general_serial = False

if os.environ.get("PRESSIO_LINALG_CPP"):
    pressio_cpp_bindings = True
    pressio_python_only = False

if os.environ.get("PRESSIO_LINALG_INSTALL_TRILINOS"):
    pressio_install_trilinos = True
    pressio_trilinos = True
    pressio_python_only = False

if os.environ.get("PRESSIO_LINALG_FIND_TRILINOS"):
    pressio_find_trilinos = True
    pressio_trilinos = True
    trilinosBaseDir = os.environ.get("PRESSIO_LINALG_FIND_TRILINOS")
    pressio_python_only = False

# ----------------------------------------------
# Metadata
# ----------------------------------------------
def myname():
  return "pressio-linalg"

def myversion():
  with open(os.path.join(topdir, "version.txt")) as f:
    return f.read()

def description():
  with open(os.path.join(topdir, "DESCRIPTION.rst")) as f:
    return f.read()

# ----------------------------------------------
# Trilinos build for serial
# ----------------------------------------------
def trilinos_for_serial_build(buildDir):
  trilTarName = "trilinos-release-13-0-1.tar.gz"
  trilUnpackedName = "Trilinos-trilinos-release-13-0-1"
  trilUrl = "https://github.com/trilinos/Trilinos/archive/"+trilTarName

  cwd = os.getcwd()

  # create subdirs for trilinos
  trilinosSubDir = cwd + "/"+buildTemp+"/../trilinos"
  if not os.path.exists(trilinosSubDir): os.makedirs(trilinosSubDir)

  trilTarPath = trilinosSubDir+"/"+trilTarName
  print("trilTarPath ", trilTarPath)
  if not os.path.exists(trilTarPath):
    subprocess.check_call(
      ["wget", "--no-check-certificate", trilUrl], cwd=trilinosSubDir
    )

  trilSrcDir = trilinosSubDir+"/"+trilUnpackedName
  print("trilSrcPath ", trilSrcDir)
  if not os.path.exists(trilSrcDir):
    subprocess.check_call(
      ["tar", "zxf", trilTarName], cwd=trilinosSubDir
    )

  trilBuildDir = trilinosSubDir+"/build"
  print("trilBuildDir = ", trilBuildDir)
  trilInstallDir = trilinosSubDir+"/install"
  print("trilInstall = ", trilInstallDir)

  cmake_args = [
    "-DCMAKE_BUILD_TYPE={}".format("Release"),
    "-DBUILD_SHARED_LIBS={}".format("ON"),
    "-DCMAKE_C_COMPILER={}".format(os.environ.get("CC")),
    "-DCMAKE_CXX_COMPILER={}".format(os.environ.get("CXX")),
    "-DCMAKE_FC_COMPILER={}".format(os.environ.get("FC")),
    "-DCMAKE_VERBOSE_MAKEFILE={}".format("ON"),
    "-DTrilinos_ENABLE_Kokkos={}".format("OFF"),
    "-DTrilinos_ENABLE_TeuchosNumerics={}".format("ON"),
    "-DCMAKE_INSTALL_PREFIX={}".format(trilInstallDir),
  ]

  if not os.path.exists(trilBuildDir):
    os.makedirs(trilBuildDir)

    subprocess.check_call(
      ["cmake", trilSrcDir] + cmake_args, cwd=trilBuildDir
    )
    subprocess.check_call(
      ["cmake", "--build", ".", "-j4"], cwd=trilBuildDir
    )
    subprocess.check_call(
      ["cmake", "--install", "."], cwd=trilBuildDir
    )

  # set env var
  os.environ["TRILINOS_ROOT"] = trilInstallDir


# ----------------------------------------------
# Trilinos build for mpi
# ----------------------------------------------
def trilinos_for_mpi_build(buildDir):
  trilTarName      = "trilinos-release-13-0-1.tar.gz"
  trilUnpackedName = "Trilinos-trilinos-release-13-0-1"
  trilUrl          = "https://github.com/trilinos/Trilinos/archive/"+trilTarName

  cwd = os.getcwd()

  # create subdirs for trilinos
  trilinosSubDir = cwd + "/"+buildDir+"/../trilinos"
  if not os.path.exists(trilinosSubDir): os.makedirs(trilinosSubDir)

  trilTarPath = trilinosSubDir+"/"+trilTarName
  print("trilTarPath ", trilTarPath)
  if not os.path.exists(trilTarPath):
    subprocess.check_call(
      ["wget", "--no-check-certificate", trilUrl], cwd=trilinosSubDir
    )

  trilSrcDir = trilinosSubDir+"/"+trilUnpackedName
  print("trilSrcPath ", trilSrcDir)
  if not os.path.exists(trilSrcDir):
    subprocess.check_call(
      ["tar", "zxf", trilTarName], cwd=trilinosSubDir
    )

  trilBuildDir = trilinosSubDir+"/build"
  print("trilBuildDir = ", trilBuildDir)
  trilInstallDir = trilinosSubDir+"/install"
  print("trilInstall = ", trilInstallDir)

  cmake_args = [
    "-DCMAKE_BUILD_TYPE={}".format("Release"),
    "-DBUILD_SHARED_LIBS={}".format("ON"),
    "-DCMAKE_VERBOSE_MAKEFILE={}".format("ON"),
    "-DTPL_ENABLE_MPI={}".format("ON"),
    "-DMPI_BASE_DIR={}".format(os.environ.get("MPI_BASE_DIR")),
    "-DTrilinos_ENABLE_Tpetra={}".format("ON"),
    "-DTrilinos_ENABLE_TpetraTSQR={}".format("ON"),
    "-DTrilinos_ENABLE_Epetra={}".format("ON"),
    "-DTrilinos_ENABLE_Ifpack={}".format("ON"),
    "-DTrilinos_ENABLE_Ifpack2={}".format("ON"),
    "-DTrilinos_ENABLE_Triutils={}".format("ON"),
    "-DCMAKE_INSTALL_PREFIX={}".format(trilInstallDir),
  ]

  if not os.path.exists(trilBuildDir):
    os.makedirs(trilBuildDir)

    subprocess.check_call(
      ["cmake", trilSrcDir] + cmake_args, cwd=trilBuildDir
    )
    subprocess.check_call(
      ["cmake", "--build", ".", "-j4"], cwd=trilBuildDir
    )
    subprocess.check_call(
      ["cmake", "--install", "."], cwd=trilBuildDir
    )

  # set env var
  return trilInstallDir
  #os.environ["TRILINOS_ROOT"] = trilInstallDir

# ----------------------------------------------
# overload install command
# ----------------------------------------------
class install(_install):
  user_options = _install.user_options + [
    #('single-node=',      None, "Boolean to tell if you just want a build for single-node.")
  ]
  if pressio_trilinos:
      user_options.append(('trilinos-basedir=', None, "Full path to base directory where Trilinos is installed."))

  def initialize_options(self):
    _install.initialize_options(self)
    # self.trilinos_basedir = "void"
    # self.single_node = False

  def finalize_options(self):
    _install.finalize_options(self)

  def run(self):
    # global trilinosBaseDir
    #serialOnly      = self.single_node
    # trilinosBaseDir = self.trilinos_basedir
    _install.run(self)

# ----------------------------------------------
# overload build command
# ----------------------------------------------
# A CMakeExtension needs a sourcedir instead of a file list.
class CMakeExtension(Extension):
  def __init__(self, name, sourcedir=""):
    print("self.name ", name)
    Extension.__init__(self, name, sources=[])
    self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
  def build_extension(self, ext):
    extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
    if not extdir.endswith(os.path.sep): extdir += os.path.sep
    print("self.extdir ",extdir)

    # create build directory
    if not os.path.exists(self.build_temp): os.makedirs(self.build_temp)
    print("self.build_temp ", self.build_temp)

    # debug/release mode
    buildMode = "Debug" if self.debug else "Release"
    print("self.debug = ", self.debug)

    # CMake lets you override the generator - we need to check this.
    # Can be set with Conda-Build, for example.
    cmake_generator = os.environ.get("CMAKE_GENERATOR", "")

    serial = False

    #-----------------------
    # IF ONLY SERIAL IS TRUE
    #-----------------------
    # if trilinosBaseDir == "void":
    if general_serial:
      if "CXX" not in os.environ:
        msg = "\n **ERROR**: \n CXX env var is missing, needs to point to your C++ compiler"
        raise RuntimeError(msg)

      # no need (for now) for trilinos in serial version
      #trilinos_for_serial_build(self.build_temp)

      # build/install pressio-tools
      cmake_args = [
        "-DCMAKE_CXX_COMPILER={}".format(os.environ.get("CXX")),
        "-DCMAKE_VERBOSE_MAKEFILE={}".format("ON"),
        "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={}".format(extdir),
        "-DPYTHON_EXECUTABLE={}".format(sys.executable),
        "-DCMAKE_BUILD_TYPE={}".format(buildMode),
      ]
      build_args = []

      if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ: build_args += ["-j4"]

      subprocess.check_call(
        ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp
      )
      subprocess.check_call(
        ["cmake", "--build", "."] + build_args, cwd=self.build_temp
      )

    elif pressio_cpp_bindings:
      #-----------------------------
      # WANT TO USE MPI AND TRILINOS
      #-----------------------------
      # check that MPI_BASE_DIR is in the environment
      if "MPI_BASE_DIR" not in os.environ:
        msg = "\n **ERROR**: \n MPI_BASE_DIR env var is missing, needs to point to your MPI installation directory "
        raise RuntimeError(msg)

      # check if trilinos_basedir is present, if not attemp build
      trilinosRoot=""
      if pressio_install_trilinos:
        msg = "You did not specify --trilinos-basedir, so attempting to build Trilinos on my own"
        print(msg)
        trilinosRoot = trilinos_for_mpi_build(self.build_temp)
      elif pressio_find_trilinos:
        msg = "Found trilinos base dir={}".format(trilinosBaseDir)
        print(msg)
        trilinosRoot = trilinosBaseDir

      # build/install pressio-tools
      #cc = os.environ.get("MPI_BASE_DIR")+"/bin/mpicc"
      cxx = os.environ.get("MPI_BASE_DIR")+"/bin/mpicxx"
      cmake_args = [
        "-DCMAKE_CXX_COMPILER={}".format(cxx),
        "-DCMAKE_VERBOSE_MAKEFILE={}".format("ON"),
        "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={}".format(extdir),
        "-DPYTHON_EXECUTABLE={}".format(sys.executable),
        "-DCMAKE_BUILD_TYPE={}".format(buildMode),
      ]
      if pressio_trilinos:
          cmake_args.append("-DTRILINOS_ROOT={}".format(trilinosRoot))

      build_args = []

      if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ: build_args += ["-j4"]

      subprocess.check_call(
        ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp
      )
      subprocess.check_call(
        ["cmake", "--build", "."] + build_args, cwd=self.build_temp
      )

# -----------------------------
# Check if the script is run with "python setup.py install"
# -----------------------------

if pressio_python_only:
  cmdclass = {
      "install": install,
  }
  ext_modules=None
else:
  cmdclass = {
      "build_ext": CMakeBuild,
      "install": install
  }
  ext_modules=[CMakeExtension("pressiolinalg._linalg")]

# -----------------------------
# setup
# -----------------------------
def run_setup():
  setup(
    name=myname(),
    version=myversion(),
    author_email="francesco.rizzi@ng-analytics.com",
    description="Parallel linear algebra library",
    long_description=description(),
    ext_modules=ext_modules,
    cmdclass=cmdclass,
    install_requires=["numpy", "scipy", "pytest-mpi", "pytest"],
    zip_safe=False,

    python_requires='>=3',
    classifiers=[
      "License :: OSI Approved :: BSD License",
      "Operating System :: Unix",
      "Environment :: MacOS X",
      "Programming Language :: C++",
      "Programming Language :: Python :: 3 :: Only",
      "Topic :: Scientific/Engineering",
      "Topic :: Scientific/Engineering :: Mathematics",
      "Topic :: Scientific/Engineering :: Physics",
      "Topic :: Software Development :: Libraries",
      "Development Status :: 4 - Beta"
    ],

    keywords=["model reduction",
              "scientific computing",
              "dense linear algebra",
              "parallel computing",
              "hyper-reduction",
              "HPC"],
    packages=['pressiolinalg'],
  )

if __name__ == '__main__':
  run_setup()
