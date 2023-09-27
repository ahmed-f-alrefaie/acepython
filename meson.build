project(
    'python-ace',
    'c',
    version: '1.3.1',
    license: 'BSD-3',
    meson_version: '>= 0.64.0',
    default_options: [
        'c_std=c99',
        'fortran_std=legacy',
    ],
)

py_mod = import('python')
py3 = py_mod.find_installation(pure: false)
py3_dep = py3.dependency()

# Compilers
add_languages('fortran', native: false)

ff = meson.get_compiler('fortran')
if ff.has_argument('-Wno-conversion')
  add_project_arguments('-Wno-conversion', language: 'fortran')
endif


subdir('python-ace')