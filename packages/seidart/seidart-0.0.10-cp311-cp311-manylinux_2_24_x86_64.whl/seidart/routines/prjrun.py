#!/usr/bin/env python3

# This script will read the parameters given from a project file and run the 
# specified models. 

# -----------------------------------------------------------------------------

import argparse
import os.path
import os
import numpy as np
import matplotlib.image as mpimg
from subprocess import call
# import seidart.routines.materials as mf
from seidart.routines.definitions import *

# Modeling modules
from seidart.fortran.cpmlfdtd import cpmlfdtd

# ------------- Globals ----------------
clight = 2.99792458e8 # In general
# Define constants
NP = 2 
NPA = 2 
k_max = 1.1e1 # 1.25e1 #This is the value determined from the litterature. 
eps0 = 8.85418782e-12 # used for em only
mu0 = 4.0*np.pi*1.0e-7 # used for em only
Rcoef = 0.0010 # used for seismic only

# ============================ Create the objects =============================
# Let's initiate the domain and check to make sure everything is good to go
def domain_initialization(prjfile: str):
    """

    :param prjfile:
    :type prjfile: str 
    """

    domain, material, seismic, electromag = loadproject(
        prjfile,
        Domain(), 
        Material(),
        Model(),
        Model()
    )

    # =================================== Model ===================================
    # Check to make sure all the domain values were given
    domain.para_check()

    # Check the model inputs
    seismic.para_check()
    electromag.para_check()

    # Check to make sure all the model inputs are satisfied
    seismic.tensor_check()
    electromag.tensor_check()

    # Drop the rgb values 
    material.material_list = np.delete(material.material_list, 2, axis = 1)
    # print(material.material_list)

    # Check the material list
    material.para_check()
    return(domain, material, seismic, electromag)

# -----------------------------------------------------------------------------
def status_check(
    modelclass, 
    material,
    domain,
    prjfile: str, 
    seismic: bool = True, 
    append_to_prjfile: bool = True,
    ):
    if modelclass.exit_status == 0 and \
        material.material_flag and \
            append_to_prjfile:
        # The coefficients aren't provided but the materials are so we can 
        # compute them
        # Assign the materials to their respective corners
        material.sort_material_list()
        
        if seismic:
            print('Computing the stiffness coefficients.')
            tensor = material.functions.get_seismic(
                temp = material.temp, 
                rho = material.rho,
                porosity = material.porosity,
                lwc = material.lwc, 
                anisotropic = material.is_anisotropic,
                angfile = material.angfiles, 
                material_name = material.material
            )
            modelclass.tensor_coefficients = tensor
        else:
            print('Computing the permittivity and conductivity coefficients.')
            
            tensor = material.functions.get_perm(
                material, modelclass
            )
            modelclass.tensor_coefficients = tensor
        
        # Before we append the coefficients to the text file let's round to the second decimal
        tensor = np.round(tensor, 2)
        if seismic:
            ind = np.where(tensor.max() == tensor)
            max_rho = tensor[ ind[0][0], -1]
        
        # We're going to find the lines marked 'C' or 'P' and input the values there

        if seismic:
            modelclass.dt = np.min([domain.dx, domain.dz]) / np.sqrt(3.0 * tensor.max()/max_rho )
            append_coefficients(prjfile, tensor, CP = 'C', dt = modelclass.dt)
        else:
            modelclass.dt = np.min([domain.dx, domain.dz]) / \
                (2.0 * clight/ \
                    np.sqrt(np.min(
                        [
                            tensor[:,1].astype(float).min(), 
                            tensor[:,4].astype(float).min()
                        ]
                    )) 
                )
            append_coefficients(prjfile, tensor, CP = 'P', dt = modelclass.dt)
        
        # The time step needs to satisfy the Courant number and also have a nyquist
        # that will resolve the source frequency
        src_nyquist = 1/(2*modelclass.f0)
        if src_nyquist < modelclass.dt:
            print(
                '''Nyquist is not small enough for the source frequency. Change
                the source frequency or decrease the spatial step size'''
            )

        print("Finished. Appending to project file.\n")

# -----------------------------------------------------------------------------
def cpmlcompute(
    modelclass, 
    domain, 
    direction: str, 
    half: bool = False, 
    seismic: bool = True
    ):
    # For 2D models, we don't need to compute the cpml in the y-direction
    if domain.dim == 2 and direction == 'y':
        return 
    
    nx = domain.nx + 2*domain.cpml
    nz = domain.nz + 2*domain.cpml
    if domain.dim == 2.5:
        ny = domain.ny + 2*domain.cpml
        deltamin = np.min([domain.dx, domain.dy, domain.dz]) 
    else:
        deltamin = np.min([domain.dx, domain.dz]) 

    # Allocate space
    if direction == 'x':
        N = int(nx)
        dx = float(domain.dx)
    elif direction == 'y':
        N = int(ny)
        dx = float(domain.dy) 
    else:
        N = int(nz)
        dx = float(domain.dz)
    
    # -----------------------------------------------------------------------------
    # Compute the distance along the absorbing boundary relative to the end of the 
    # original model space. 
    dist = dx * np.arange(0, domain.cpml)
    if half:
        dist = dist + dx/2 

    dist = dx*domain.cpml - dist
    dist = dist/(dx*domain.cpml)

    quasi_cp_max = 0.7* deltamin / (2.0 * modelclass.dt)
    alpha_max = np.pi*modelclass.f0
    if seismic:
        sig_max = - np.log(Rcoef) * (NP+1) * quasi_cp_max / (2.0 * domain.cpml )
    else:
        sig_max = 0.7 * (NP+1) / (dx * np.sqrt(mu0/eps0) )

    kappa = np.ones([N])
    alpha = np.zeros([N])
    sigma = np.zeros([N])
    acoeff = np.zeros([N])
    bcoeff = np.zeros([N])

    # Compute in the x, and z directions
    for ind in range(0, domain.cpml):
        # From 0
        sigma[ind] = sig_max*dist[ind]**NP
        kappa[ind] = 1.0 + (k_max - 1.0) * dist[ind]**NP
        alpha[ind] = alpha_max * (1 - dist[ind])**NPA
        sigma[-(ind+1)] = sig_max*dist[ind]**NP
        kappa[-(ind+1)] = 1 + (k_max - 1) * dist[ind]**NP
        alpha[-(ind+1)] = alpha_max * (1 - dist[ind])**NPA
        bcoeff[-(ind+1)] = np.exp(- (sigma[-(ind+1)] / kappa[-(ind+1)] + alpha[-(ind+1)]) * modelclass.dt)
        bcoeff[ind] = np.exp( - (sigma[ind] / kappa[ind] + alpha[ind]) * modelclass.dt)

    # Compute the a-coefficients 
    alpha[np.where(alpha < 0.0)] = 0.0
    indices = np.where(np.abs(sigma) > 1.0e-6)
    acoeff[indices] = sigma[indices] * (bcoeff[indices] - 1) / \
            (kappa[indices] * sigma[indices] + kappa[indices] * alpha[indices] )

    # Save the results to a fortran binary
    if half:
        sigma.tofile('sigma' + direction + '_half_cpml.dat')
        kappa.tofile('kappa' + direction + '_half_cpml.dat')
        alpha.tofile('alpha' + direction + '_half_cpml.dat')
        acoeff.tofile('acoef' + direction + '_half_cpml.dat')
        bcoeff.tofile('bcoef' + direction + '_half_cpml.dat')
    else:
        sigma.tofile('sigma' + direction + '_cpml.dat')
        kappa.tofile('kappa' + direction + '_cpml.dat')
        alpha.tofile('alpha' + direction + '_cpml.dat')
        acoeff.tofile('acoef' + direction + '_cpml.dat')
        bcoeff.tofile('bcoef' + direction + '_cpml.dat')

# ================================== SEISMIC ==================================
def runseismic(
        modelclass,
        material, 
        domain,
        single_precision: bool,
    ):
    modelclass, domain = prepme(modelclass, domain, complex_tensor = False)
    direction = ['x', 'y', 'z']
    # Compute CPML
    print(direction)
    print('computing cpml')
    for d in direction:
        cpmlcompute(modelclass, domain, d, seismic = seismic)
        cpmlcompute(modelclass, domain, d, half = True, seismic = seismic)
    
    # We need to set a density gradient at air interfaces because high
    # density gradients lead to numerical instability
    rhograd = airsurf(material, domain, 2)
    # Write the coefficient images to a fortran file
    
    # Create the stiffness .dat files
    cpmlfdtd.stiffness_write(
        domain.geometry + 1,
        modelclass.tensor_coefficients,
        domain.cpml,
        rhograd,
        domain.nx,
        domain.nz
    )
    attenuation_coefficients = modelclass.attenuation_coefficients * \
        modelclass.dt / (np.ones([domain.nmats, 3]) * \
            material.material_list[:,3].astype(float) ).T
    # Create the attenuation .dat files
    cpmlfdtd.attenuation_write(
        domain.geometry + 1,
        attenuation_coefficients,
        domain.cpml,
        # domain.nx, 
        # domain.nz,
        domain.cpml_attenuation,
        True
    )
    
    if domain.dim == 2.5:
        print('Running 2.5D model')
        # Run the FDTD
        cpmlfdtd.seismic25(
            domain.nx + 2*domain.cpml, 
            domain.ny + 2*domain.cpml, 
            domain.nz + 2*domain.cpml,
            domain.dx, domain.dy, domain.dz,
            domain.cpml,
            modelclass.src,
            modelclass.time_steps,
            single_precision
        )
    else:
            print('Running 2D model')
            cpmlfdtd.seismic2c(
                domain.nx + 2*domain.cpml, 
                domain.nz + 2*domain.cpml,
                domain.dx, domain.dz,
                domain.cpml,
                modelclass.src,
                modelclass.time_steps,
                single_precision
            )     

# =============================================================================
def runelectromag(
        modelclass,
        material, 
        domain,
        use_complex_equations: bool = False,
        single_precision: bool = True,
    ):
    modelclass, domain = prepme(
        modelclass, domain, complex_tensor = use_complex_equations
    )
    direction = ['x', 'y', 'z']
    # Compute CPML
    print(direction)
    print('computing cpml')
    for d in direction:
        cpmlcompute(modelclass, domain, d, seismic = False)
        cpmlcompute(modelclass, domain, d, half = True, seismic = False)
    
    if use_complex_equations:
        cpmlfdtd.permittivity_write_c(
            domain.geometry+1,
            modelclass.tensor_coefficients,
            domain.cpml,
            domain.nx, 
            domain.nz
        )
        if domain.dim == 2.5:
            print('Running complex 3D model.')
            cpmlfdtd.electromag25c(
                domain.nx + 2*domain.cpml, 
                domain.ny + 2*domain.cpml, 
                domain.nz + 2*domain.cpml,
                domain.dx, domain.dy, domain.dz,
                domain.cpml,
                modelclass.src,
                modelclass.time_steps,
                single_precision
            )
        else:
            print('Running complex 2D model')
            cpmlfdtd.electromag2c(
                domain.nx + 2*domain.cpml,
                domain.nz + 2*domain.cpml,
                domain.dx, domain.dz,
                domain.cpml,
                modelclass.src,
                modelclass.time_steps,
                single_precision
            )
    else:
        
        cpmlfdtd.permittivity_write(
                domain.geometry+1,
                modelclass.tensor_coefficients.real,
                domain.cpml,
                domain.nx, 
                domain.nz
            )
        if domain.dim == 2.5:
            print('Running 2.5D model')
            cpmlfdtd.electromag25(
                domain.nx + 2*domain.cpml, 
                domain.ny + 2*domain.cpml, 
                domain.nz + 2*domain.cpml,
                domain.dx, domain.dy, domain.dz,
                domain.cpml,
                modelclass.src,
                modelclass.time_steps,
                single_precision
            )
        else:
            print('Running 2D model')
            cpmlfdtd.electromag2(
                domain.nx + 2*domain.cpml,
                domain.nz + 2*domain.cpml,
                domain.dx, domain.dz,
                domain.cpml,
                modelclass.src,
                modelclass.time_steps,
                single_precision
            )
        

# -------------------------- Command Line Arguments ---------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""The SeidarT software requires a
        .PNG image that is used to construct the model domain for seismic and
        electromagnetic wave propagation. Given the image file, a project file
        will be constructed which contains all the necessary parameters to be
        read in to the finite differences time domain modeling schemes."""
    )

    parser.add_argument(
        '-p', '--prjfile', nargs=1, type=str, required = True,
        help='the full file path for the project file', default=None
    )

    parser.add_argument(
        '-m', '--model', nargs = 1, type = str, required = False,
        help = """Specify whether to run the seismic (s), or electromagnetic (e), 
        or none (default = n)""",
        default = 'n'
    )

    parser.add_argument(
        '-a', '--append',
        nargs = 1, type = int, required = False, default = [1],
        help = """Append/recompute the coefficients to the permittivity and
        stiffness matrices; 1 = yes, 0 = no; default = 1."""
    )
    
    parser.add_argument(
        '-d', '--double_precision', action='store_false', required = False,
        help = """Specify double precision output of the simulation. If 
        complex, the outputs are real valued of each of the components of the 
        complex value. The default is True."""
    )
    
    parser.add_argument(
        '-c', '--use_complex_equations', action = 'store_true', required = False,
        help = """Flag whether to use the complex permittivity in the model
        simulation. The complex permittivity will be computed for ice and snow
        in all situations, but unless specified here, the complex permittivity 
        will only be used to compute the conductivity."""
    )
    
    parser.add_argument(
        '-o', '--output_directory_path', required = False, 
        nargs = 1, type = str, 
        help = '''Specify the output directory folder path to write the Fortran
        outputs to. '''
    )
    # parser.add_argument(
    #     '-A', '--attenuation', action='store_true', required = False,
    #     help = """Specify whether to include attenuation in the model. The 
    #     default is False."""
    # )

    # Get the arguments
    args = parser.parse_args()
    prjfile = ''.join(args.prjfile)
    model_type = ''.join(args.model)
    append_to_prjfile = args.append[0] == 1
    pwd = os.path.dirname(prjfile)
    double_precision = args.double_precision
    use_complex_equations = args.use_complex_equations
     
    # attenuation = args.attenuation
    #
    domain, material, seismic, electromag = domain_initialization(prjfile)
    status_check(
        seismic, 
        material,
        domain,
        prjfile, 
        seismic=True, 
        append_to_prjfile = append_to_prjfile
    )
    status_check(
        electromag, 
        material, 
        domain,
        prjfile, 
        seismic=False, 
        append_to_prjfile = append_to_prjfile,
        use_complex_equations = use_complex_equations
    )
    
    
    if model_type == 's':
        runseismic(
            seismic, material, domain, 
            double_precision
        )
    if model_type == 'e':
        runelectromag(
            electromag, material, domain, 
            use_complex_equations = use_complex_equations, 
            double_precision = double_precision
        )