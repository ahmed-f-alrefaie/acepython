incdir_numpy = run_command(py3, [
    '-c',
    '''import os, numpy as np
try:
    print(os.path.relpath(np.get_include()))
except:
    print(np.get_include())
    ''',
], check: true).stdout().strip()
inc_np = include_directories(incdir_numpy)
incdir_f2py = incdir_numpy / '..' / '..' / 'f2py' / 'src'
inc_f2py = include_directories(incdir_f2py)
fortranobject_c = incdir_f2py / 'fortranobject.c'

numpy_nodepr_api = '-DNPY_NO_DEPRECATED_API=NPY_1_9_API_VERSION'

# Dependencies for Fortran
fortranobject_lib = static_library(
    '_fortranobject',
    fortranobject_c,
    c_args: numpy_nodepr_api,
    dependencies: py3_dep,
    include_directories: [inc_np, inc_f2py],
)
fortranobject_dep = declare_dependency(
    link_with: fortranobject_lib,
    include_directories: [inc_np, inc_f2py],
)


ace_module = custom_target(
    'mdacemodule',
    output : ['mdacemodule.c', 'mdace-f2pywrappers2.f90'],
    input : '../../ace_sources/ace.pyf',
    command: [py3, '-m', 'numpy.f2py', '@INPUT@', '--build-dir', '@OUTDIR@', '--lower']
)


py3.extension_module('mdace',
  [

  '../../ace_sources/Md_Constantes.f90', 
  '../../ace_sources/Md_Types_Numeriques.f90',
  '../../ace_sources/Md_numerical_recipes.f90', 
  '../../ace_sources/Md_Utilitaires.f90', 
  '../../ace_sources/Md_ACE.f90', 
  ace_module
  ],
  c_args: numpy_nodepr_api,
  dependencies: fortranobject_dep,
  install : true,
  link_language: 'fortran',
  subdir: 'acepython',
)

py3.install_sources(
    ['__init__.py', 'ace.py', 'taurex3.py'],
    pure: false,
    subdir: 'acepython'
)

py3.install_sources(
    ['../../ace_data/Data/NASA.therm', '../../ace_data/Data/composes.dat'],
    pure: false,
    subdir: 'acepython/data'
)

