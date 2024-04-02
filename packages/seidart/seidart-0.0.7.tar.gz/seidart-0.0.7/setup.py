from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration

def configuration(parent_package='', top_path=None):
    config = Configuration(None, parent_package, top_path)

    # Define Fortran extensions
    fortran_sources = [
        # 'src/seidart/fortran/readwrite_routines.f95',
        # 'src/seidart/fortran/seismicfdtd.f95',
        # 'src/seidart/fortran/electromagfdtd.f95',
        'src/seidart/fortran/cpmlfdtd.f95'
    ]
    
    config.add_extension(
        name='seidart.fortran.cpmlfdtd',
        sources=fortran_sources,
        # f2py_options=['--fcompiler=gnu95'],
        # extra_f90_compile_args=['-std=f95']
    )
    
    return config

if __name__ == "__main__":
    setup(
        name='seidart',
        version='0.0.7',
        packages=[
            'seidart', 
            'seidart.fortran', 
            'seidart.routines', 
            'seidart.simulations', 
            'seidart.visualization'
        ],
        configuration=configuration
    )
