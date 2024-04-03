#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by Steven Bernsen
We are given a range of velocities of different materials found empirically. 
For isotropic materials we can determine the Lame constants from the equations:
    Vp = sqrt( lambda + 2 mu  / rho ),
    Vs = sqrt( mu / rho ),
    c11 = c22 = c33 = lambda + 2 mu,
    c12 = c13 = c23 = lambda,
    c44 = c55 = c66 = mu
"""

import numpy as np
from typing import Union, Tuple
from scipy.interpolate import interp1d

eps0 = 8.85418782e-12 # used for em only
mu0 = 4.0*np.pi*1.0e-7 # used for em only
# =============================================================================
#                               Class Variables
# =============================================================================



# =============================================================================
#                       Define material dictionaries
# =============================================================================

"""
Seismic values can be found in: 
      Acoustics of Porous Media (1992), Bourbie, Coussy, and Zinszner
      
Permittivity values can be found in:
        Electrical Properties of Rocks and Minerals
    The following values are provided by:
        Seismic Velocities - https://pangea.stanford.edu/courses/gp262/Notes/8.SeismicVelocity.pdf
        Permeabilitues - http://www.geo.umass.edu/faculty/wclement/dielec.html
        Conductivities - Duba et al. (1977), Duba et al. (1978), Watanabe (1970), 
                    Mohammadi and Mohammadi (2016),
                    https://www.nrcs.usda.gov/INTERNET/FSE_DOCUMENTS/NRCS142P2_053280.PDF,
                    https://en.wikipedia.org/wiki/Electrical_resistivity_and_conductivity
    Values are: 
        Vp_min, Vp_max, Vs_min, Vs_max, Rel_Perm_min, Rel_Perm_max, Conductivity_min, Conductivity_max
    
    Permittivity is given as the relative permittivity and for most cases we 
    will assume that relative permeability is unity; however, if we include
    materials that are high in magnetite, hematite, etc. then we will need to
    accomodate for better permeability estimates.
"""


isotropic_materials = {
    "air":np.array([343, 343, 0.0, 0.0, 1.0, 1.0, 1.0e-16, 1.0e-15]),
    "ice1h":np.array([3400, 3800, 1700, 1900, 3.1, 3.22, 1.0e-7, 1.0e-6]),
    "snow":np.array([100, 2000, 50, 500, 1.0, 70, 1.0e-9, 1.0e-4]),
    "soil":np.array([300, 700, 100, 300, 3.9, 29.4, 1.0e-2, 1.0e-1]), # Permittivity estimates are best constructed with the snow_permittivity() function
    "water":np.array([1450, 1500, 0, 0, 80.36, 80.36, 5.5e-6, 5.0e-2]), # This can change drastically depending on the ions in solution
    "oil":np.array([1200, 1250, 0, 0, 2.07, 2.14, 5.7e-8, 2.1e-7]),
    "dry_sand":np.array([400, 1200, 100, 500, 2.9, 4.7, 1.0e-3, 1.0e-3]), # perm porositiy dependence
    "wet_sand":np.array([1500, 2000, 400, 600, 2.9, 105, 2.5e-4, 1.2e-3]), 
    "granite":np.array([4500, 6000, 2500, 3300, 4.8, 18.9, 4.0e-5, 2.5e-4]),
    "gneiss":np.array([4400, 5200, 2700, 3200, 8.5, 8.5, 2.5e-4, 2.5e-3]),
    "basalt":np.array([5000, 6000, 2800, 3400, 12, 12, 1.0e-6, 1.0e-4]),
    "limestone":np.array([3500, 6000, 2000, 3300, 7.8, 8.5, 2.5e-4, 1.0e-3]),
    "anhydrite":np.array([4000, 5500, 2200, 3100, 5, 11.5, 1.0e-6, 1.0e-5]), # permittivity value from Gypsum
    "coal":np.array([2200, 2700, 1000, 1400, 5.6, 6.3, 1.0e-8, 1.0e-3]), # This has a water dependency
    "salt":np.array([4500, 5500, 2500, 3100, 5.6, 5.6, 1.0e-7, 1.0e2]) # This is dependent on ions and water content
}


# -----------------------------------------------------------------------------
def pressure_array(
        im: Union[list, np.ndarray], 
        temp: Union[list, np.ndarray], 
        rho: Union[list, np.ndarray], 
        dz: Union[list, np.ndarray], 
        porosity: Union[list, np.ndarray] = [0], 
        lwc: Union[list, np.ndarray] = [0]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]: 
    '''
    Compute the hydrostatic pressure for each grid point and correct the 
    stiffness matrix to reflect this. The hydrostatic pressure is computed
    using the overburden P = rho * g * h, but rho is not assumed to be
    constant. This is a lower order approximation and doesn't include external
    stress and dynamics. 

    temp and rho are k-by-1 indices

    :param im: an m-by-n array of integer values corresponding to the material
        ID. 
    :type im: list or np.ndarray 

    :param temp:  
    :type : 

    :return temperature:
    :rtype temperature: np.ndarray

    :return density: 
    :rtype density: np.ndarray

    :return pressure:
    :rtype pressure: np.ndarray

    '''
    
    # First match the size of 
    k = np.unique(im)

    m, n = im.shape
    # allocate the pressure, temperature and density
    pressure = np.zeros([m, n])
    density = np.zeros([m, n])

    if not temp.shape == im.shape:
        temperature = np.zeros([m, n])
    for j in range(0,n):
        for i in range(0, m):
            temperature[i,j] = temp[ im[i,j] ]
            density[i,j],_,_ = porewater_correction(temperature[i,j], rho[ im[i,j] ], 
                porosity[ im[i,j]], lwc[ im[i,j]])
            pressure[i,j] = np.mean(density[0:i,j]) * 9.80665 * i * dz
    
    return(temperature, density, pressure)


def anisotropic_boolean(im, matbool, angvect):
    '''
    :param :  Union[list, np.ndarray]
    :type : 

    :param :  
    :type : 

    :param :  
    :type : 

    :return :
    :rtype :

    :return :
    :rtype :
    '''
    m,n = im.shape
    anisotropic = np.zeros([m,n], dtype = bool)
    afile = np.zeros([m,n], dtype = str)

    for i in range(0, m):
        for j in range(0,n):

            # The booolean in anisotropic could be true, True, TRUE     
            anisotropic[i,j] = (
                matbool[ im[i,j] ] == 'true' or \
                matbool[ im[i,j] ] == 'TRUE' or \
                matbool[ im[i,j] ] == 'True'
            )
            
            if anisotropic[i,j]:
                afile[i,j] = angvect[ im[i,j] ]

    return(anisotropic, afile)

# =============================================================================
# -----------------------------------------------------------------------------
def get_seismic(
        material_name: Union[list, np.ndarray] = [None], 
        temp: Union[list, np.ndarray] = [None], 
        rho: Union[list, np.ndarray] = [None], 
        porosity: Union[list, np.ndarray] = [0], 
        lwc: Union[list, np.ndarray] = [0], 
        anisotropic: Union[list, np.ndarray] = [False], 
        angfile: Union[list, np.ndarray] = [None]
    ):
    '''
    Compute the seismic stiffness coefficients given the temperature, percent
    pore space, and water content. Anisotropic files will be flagged by the 
    boolean, and an angular file needs to be included. A single material can be
    computed or an array of materials. If an array is input, the length of each 
    parameter must match. For an anisotropic material, the tensor values are 
    calculated from the Hill estimate.
    
    Parameters
    ----------
    :param material_name: the string identifier of the material
    :type material_name: list or np.ndarray

    :param temp: The temperature of the material. 
    :type temp: list or np.array

    :param rho: The density of the material.
    :type rho: list or np.array

    :param porosity: the percent value for the porosity of the material
    :type porosity: list or np.array

    :param lwc: the percent value for liquid water content
    :type lwc: list or np.array

    :param anisotropic: A list or array of boolean values. If False, the 
        isotropic stiffness tensor is computed
    :type anisotropic: list or np.array

    :return tensor: An m-by-23 array of the material ID, the 21 tensor
        components of the upper triangular of the Voigt notation 
    :rtype tensor: np.ndarray

    '''
    m = len(temp)
    tensor = np.zeros([m, 23])

    # Adjust the stiffness tensor according to the pressure and temperature conditions for ice
    for ind in range(0, m):
        density,_,_ = porewater_correction(temp[ind], rho[ind], porosity[ind], lwc[ind] )

        if anisotropic[ind] and material_name[ind] == 'ice1h':
            euler = read_ang(angfile[ind])
            p = len(euler[:,0])

            cvoigt = np.zeros([6,6])
            creuss = np.zeros([6,6])
            C = np.zeros([6,6])
            
            # Assume a constant pressure of 0.1 MPa (Why? because this is approximately 1 ATM)
            C = ice_stiffness(temp[ind], 0.1)
            S = np.linalg.inv(C)

            for k in range(0, p):
                R = rotator_zxz(euler[k,:] )
                M = bond(R)
                N = np.linalg.inv(M)
                cvoigt = cvoigt + ( np.matmul( M, np.matmul(C, M.T) ) )
                creuss = creuss + ( np.matmul( N, np.matmul(S, N.T) ) )

            cvoigt = cvoigt/p
            creuss = creuss/p 
            creuss = np.linalg.inv(creuss) 

            # Calculate the hill average 
            C = (cvoigt + creuss)/2
        elif not anisotropic[ind] and material_name[ind] == 'ice1h':
            C = ice_stiffness(temp[ind], 0.1)
        else:
            material_limits = isotropic_materials[ material_name[ind] ]
            C = isotropic_stiffness_tensor(0.1, density, material_limits )

        tensor[ind, :] = (
            ind, 
            C[0,0], C[0,1], C[0,2], C[0,3], C[0,4], C[0,5],
            C[1,1], C[1,2], C[1,3], C[1,4], C[1,5],
            C[2,2], C[2,3], C[2,4], C[2,5],
            C[3,3], C[3,4], C[3,5],
            C[4,4], C[4,5],
            C[5,5], 
            density
        )

    return(tensor)


# -----------------------------------------------------------------------------
def get_perm(
        matclass,
        modelclass
    ):
    '''
    Compute the permittivity and conductivity tensors for a material and its
    attributes
    :param :  
    :type : 

    :return :
    :rtype :
    '''
    #!!!!! Use the material class as an input since it will have all of the values that you need instead of inputting all of them 
    matclass.temp
    
    m = len(matclass.temp)
    # We will always compute the complex tensor. 
    tensor = np.zeros([m, 13], dtype = complex)
    
    # Adjust the stiffness tensor according to the pressure and temperature 
    # conditions for ice
    for ind in range(0, m):
        
        if matclass.material[ind] == 'ice1h':
            permittivity = ice_permittivity(
                matclass.temp[ind],
                matclass.density[ind],
                center_frequency = modelclass.f0
            )
            conductivity = snow_conductivity(
                permittivity = permittivity, frequency = modelclass.f0
            )
            
        elif matclass.material[ind] == 'snow':
            permittivity = snow_permittivity(
                temperature = matclass.temp[ind],
                lwc = matclass.lwc[ind], 
                porosity = matclass.porosity[ind]
            )
            conductivity = snow_conductivity(
                permittivity = permittivity, frequency = modelclass.f0
            )
        else:
            permittivity = np.round(
                isotropic_permittivity_tensor(
                    matclass.temp[ind], 
                    matclass.porosity[ind], 
                    matclass.lwc[ind], 
                    matclass.material[ind])[0], 
                    3
                )
            conductivity = isotropic_permittivity_tensor(
                matclass.temp[ind], 
                matclass.porosity[ind], 
                matclass.lwc[ind], matclass.material[ind]
            )[1]
        
        if matclass.is_anisotropic[ind]:
            euler = read_ang(angfile[ind])
            p = len(euler[:,0])
            
            pvoigt = np.zeros([3,3])
            preuss = np.zeros([3,3])
            permittivity = np.zeros([3,3])
            
            # Assume a constant pressure of 0.1 MPa
            
            S = np.linalg.inv(permittivity)
            
            for k in range(0, p):
                R = rotator_zxz(euler[k,:] )
            
                Ri = np.linalg.inv(R)
                #!!!!! We need to do the same for conductivity.  
                pvoigt = pvoigt + ( np.matmul( R, np.matmul(permittivity, R.T) ) )
                preuss = preuss + ( np.matmul( Ri, np.matmul(S, Ri.T) ) )
            
            pvoigt = pvoigt/p
            preuss = preuss/p 
            preuss = np.linalg.inv(preuss) 
            
            # Calculate the hill average 
            permittivity = (pvoigt + preuss)/2
            
        tensor[ind, :] = np.array(
            [
                ind,
                permittivity[0,0], permittivity[0,1], permittivity[0,2],
                permittivity[1,1], permittivity[1,2],
                permittivity[2,2],
                conductivity[0,0], conductivity[0,1], conductivity[0,2],
                conductivity[1,1], conductivity[1,2],
                conductivity[2,2]
            ] 
        )
    
    return(tensor)


# -----------------------------------------------------------------------------
# =============================================================================
def rho_water_correction(temperature = 0):
    rho_water = (
        999.83952 + \
            16.945176 * temperature - \
                7.9870401e-3 * temperature**2 - \
                    46.170461e-6 * temperature**3 + \
                        105.56302e-9 * temperature**4 - \
                            280.54253e-12 * temperature**5
        )/(1 + 16.897850e-3 * temperature)
    return(rho_water)

def isotropic_stiffness_tensor(pressure, density, material_limits):
    '''
    Compute the isotropic stiffness tensor using values from the 
    'isotropic_materials' dictionary. The dictionary of values provides general
    set of p and s wave values which are then used to compute the stiffness 
    tensor. See the header for more details on the source of those values. 

    Parameters
    ----------
    :param :  
    :type : 

    :return :
    :rtype :
    '''
    Vp = material_limits[0:2]
    Vs = material_limits[2:4]
    cp = 2*(Vp[1] - Vp[0])/np.pi 
    cs = 2*(Vs[1] - Vs[0])/np.pi
    
    # Correct for pressure
    pvelocity = cp*np.arctan(pressure ) + Vp[0]
    svelocity = cs*np.arctan(pressure) + Vs[0]
    
    # Compute the lame parameters
    mu = density*(svelocity**2)
    lam = density*(pvelocity**2) - 2*mu

    # Assign the matrix
    C = np.zeros([6,6])
    C[0:3,0:3] = lam
    np.fill_diagonal(C, C.diagonal() + mu)
    C[0,0] = lam + 2*mu
    C[1,1]= C[1,1] + mu
    C[2,2] = C[2,2] + mu

    return(C)

# -----------------------------------------------------------------------------
def isotropic_permittivity_tensor(
        temperature, 
        porosity, 
        water_content, 
        material_name
    ):
    '''
    Compute the isotropic permittivity tensor using values from the 
    'isotropic_materials' dictionary. The dictionary of values provides general
    relative permittivity values which are then used to compute the 
    permittivity tensor.
    
    Parameters
    ----------
    :param temperature:  
    :type temperature: 

    :param porosity:  
    :type porosity:

    :param liquid_water_content:  
    :type liquid_water_content:

    :param material_name:  
    :type material_name:

    :return :
    :rtype :
    '''
    material_limits = isotropic_materials[ material_name ]
    perm0 = material_limits[4]
    perm1 = material_limits[5]

    cond0 = material_limits[6]
    cond1 = material_limits[7]

    # Calculate the slope         
    if material_name == 'ice1h':
        # We'll assume that the maximum porosity of ice (a.k.a. fresh pow pow)
        # is 85%. The porosity is given as percent [0,100]
        perm0 = 3.1884 + 9.1e-4 * temperature
        perm_coef = (perm1 - perm0)/85
        cond_coef = (cond1 - cond0)/85
        permittivity = np.eye(3,3) * (perm_coef*(porosity) + perm0)
        conductivity = np.eye(3,3) * (cond_coef*(porosity) + cond0)
            
    elif material_name == 'soil' or material_name == 'dry sand':
        # The limit of these two materials is around 55%
        perm_coef = (perm1 - perm0)/55
        cond_coef = (cond1 - cond0)/55
        permittivity = np.eye(3,3) * (perm_coef*(porosity) + perm0)
        conductivity = np.eye(3,3) * (cond_coef*(porosity) + cond0)
    
    elif material_name == 'salt':
        # Permittivity will change a little bit but let's neglect it for now
        permittivity = np.eye(3,3) * perm0
        # Let's use a simple linear trend for a maximum of 20%? water content
        cond_coef = (cond1 - cond0)/20
        conductivity = np.eye(3,3) * (cond_coef*(water_content) +  cond0 )
    
    elif material_name == 'water' or material_name == 'oil':
        # Water and oil do not have a porosity.
        permittivity = np.eye(3,3) * material_limits[4]
        conductivity = np.eye(3,3) * material_limits[6]
    else:
        # For other materials we'll assume the limit is around 3%
        perm_coef = (perm1 - perm0)/3
        cond_coef = (cond1 - cond0)/3
        permittivity = np.eye(3,3) * (perm_coef*(porosity) + perm0)
        conductivity = np.eye(3,3) * (cond_coef*(porosity) + cond0)
    
    return(permittivity, conductivity)

# -----------------------------------------------------------------------------
def porewater_correction(temperature, density, porosity, liquid_water_content ):
    '''
    Correct the bulk density given the amount of pore water content. The 
    water and air density are corrected given the temperature. The porosity 
    should already be incorporated in the material density, but we are 
    calculating the volumetric fractions of pore density and rock density
    
    Parameters
    ----------
    :param temperature:  
    :type temperature:

    :param density:  
    :type density:

    :param porosity:  
    :type porosity: 

    :param liquid_water_content:  
    :type liquid_water_content:

    :return :
    :rtype :
    '''
    rho_air = 0.02897/(8.2057338e-5 * (273 + temperature) )
    # Kell Equation; This doesn't incorporate pressure. That would be a nice
    # addition so that we can mimic super cooled water at depth. 
    rho_water = rho_water_correction(temperature)
    
    # rho_water = -4.6074e-7*temperature**4 + \
    #   1.0326e-4*temperature**3 - 1.0833e-2*temperature**2 + \
    #       9.4207e-2*temperature**1 + 999.998

    # There are certain limits such as phase changes so let's put practical limits on this
    rho_water = np.max( (rho_water, 950) ) # We can't quite accomodate supercooled water density
    rho_water = np.min( (rho_water, rho_water_correction() )) # beyond the freezing and vaporization temperatures, things get wonky
    
    # the water content is the percent of pores that contain water
    grams_air = (1-liquid_water_content/100)*rho_air
    grams_water = (liquid_water_content/100)*rho_water
    rho_wc = grams_air + grams_water
        
    density = (1-porosity/100)*density + (porosity/100)*rho_wc

    return(density, grams_air, grams_water)

# -----------------------------------------------------------------------------
def ice_stiffness(temperature = None, pressure = 0) :
    '''
    This equation is from G

    
    Parameters
    ----------
    :param :  
    :type : 

    :return :
    :rtype :
    '''
    # Allocate space for the stiffness tensor
    C = np.zeros([6,6])
    
    C[0,0] = 136.813 - 0.28940*temperature - 0.00178270*(temperature**2) \
      + 4.6648*pressure - 0.13501*(pressure**2) 
    C[0,1] = 69.4200 - 0.14673*temperature - 0.00090362*(temperature**2) \
      + 5.0743*pressure + .085917*(pressure**2)
    C[0,2] = 56.3410 - 0.11916*temperature - 0.00073120*(temperature**2) \
      + 6.4189*pressure - .52490*(pressure**2)
    C[2,2] = 147.607 - 0.31129*temperature - 0.0018948*(temperature**2) \
      + 4.7546*pressure - .11307*(pressure**2)
    C[3,3] = 29.7260 - 0.062874*temperature - 0.00038956*(temperature**2) \
      + 0.5662*pressure + .036917*(pressure**2)
    
    # Fill in the symmetry
    C[1,1] = C[0,0]
    C[1,0] = C[0,1]
    C[2,0] = C[0,2]
    C[1,2] = C[0,2]
    C[2,1] = C[1,2]
    C[4,4] = C[3,3]
    C[5,5] = (C[0,0] - C[0,1] )/2
    
    stiffness = C*1e8

    return(stiffness)

# -----------------------------------------------------------------------------

def ice_permittivity(
        temperature, 
        density, 
        center_frequency = None,
        method = "fujita"
    ):
    '''
    Parameters
    ----------
    :param :  
    :type : 

    :return :
    :rtype :
    '''
    #Allocate
    P = np.zeros([3,3], dtype = complex)

    # The following is for 2-10 GHz. The details can be found in 
    if method == "kovacs":
        perm = (1 + 0.845 * density)**2
    else: # Fujita et al. (2000)
        perm = 3.1884 + 9.1e-4 * temperature
        dP = 0.0256 + 3.57e-5 * (6.0e-6) * temperature
        complex_perm = fujita_complex_permittivity(
            temperature, center_frequency
        )
        perm = complex(perm, complex_perm)
    
    permittivity = np.eye(3,3) * perm 
    if method == 'fujita':
        permittivity[2,2] = perm + dP 

    return(permittivity)

# -----------------------------------------------------------------------------
def snow_permittivity(
        density: float = 917., 
        temperature: float = 0., 
        lwc: float = 0., 
        porosity: float = 50.,
        method: str = "shivola-tiuri"
    ):
    '''

    
    Parameters
    ----------
    :param :  
    :type : 

    :return :
    :rtype :
    '''
    # Temperature equations
    # jones (2005), liebe et al. (1991)
    # Density equations 
    # shivola and tiuri (1986), wise
    
    rho_d,grams_air,grams_water = porewater_correction(
        temperature, density, porosity, lwc
    )
    
    # LWC is in kg/m3 but we need it in g/cm3
    lwc = grams_water / 1000
    rho_d = rho_d / 1000
    # Put temperature in terms of kelvin
    T = temperature + 273.15

    if method == "shivola-tiuri":
        perm = 8.8*lwc + 70.4*(lwc**2) + 1 + 1.17*rho_d + 0.7*(rho_d**2)
    elif method == "wise":
        perm = 1 + 1.202*rho_d + 0.983*(rho_d**2) + 21.3*lwc
    elif method == "jones":
        perm = 78.51 * (
            1 - 4.579 * 1e-3 * (T - 298) + \
                1.19 * 1e-5 * (T - 298)**2 - \
                    2.8*1e-8 * (T - 298)**3
        )
    else: # Liebe et al.
        perm = 77.66 - 103.3 * (1 - (300/(T)) )
    
    # Compute the complex part
    complex_permittivity = 0.8*lwc + 0.72*(lwc**2)
    permittivity = np.eye(3,3) * complex(perm, complex_permittivity)

    return(permittivity)

# -----------------------------------------------------------------------------
def water_permittivity(temperature):
    '''

    
    Parameters
    ----------
    :param :  
    :type : 

    :return :
    :rtype :
    '''
    pass
    # return( snow_permativity() )

# -----------------------------------------------------------------------------
def snow_conductivity(lwc = None, permittivity = None, frequency = None):
    '''
    Parameters
    ----------
    :param :  
    :type : 

    :return :
    :rtype :
    '''
    if np.iscomplexobj(permittivity):
        sigma = permittivity.imag * frequency * eps0
    else:
        # granlund et al. (2010)
        _,_,grams_water = porewater_correction(
            temperature, density, porosity, lwc
        )
        
        # LWC is in kg/m3 but we need it in g/cm3
        lwc = grams_water / 1000
        # granlund provides an equation for micro-S/m so we multiply by 1e-4 to
        # put it in terms of S/m
        sigma = (20 + 3e3 * lwc) * 1e-4 
    
    conductivity = np.eye(3,3) * sigma 
    return(conductivity)

# -----------------------------------------------------------------------------

def read_ang(filepath):
    '''

    
    Parameters
    ----------
    :param :  
    :type : 

    :return :
    :rtype :

    The input .ang file will have the columns as 
        c1-3    Euler angles (radians; Bunge's notation - z-x-z rotation )
        c4,5    horizontal, vertical respectively
        c6      image quality
        c7      confidence index
        c8      phase ID
        c9      detector intensity
        c10     fit
    Refer to this thread for more description of the aforementioned
        https://www.researchgate.net/post/How_can_I_get_X_Y_position_data_of_a_single_grain_from_EBSD_scan
    '''
    
    # Load the file in as a data frame
    euler = np.genfromtxt(filepath, delimiter = " ")

    # take only the euler angles...for now
    if euler.shape[0] > 3 :
        euler = euler[:,0:3]

    # Unfortunately, the space delimiters are inconsistent :(
    # We know there are 10 columns and the rows shouldn't contain all NA's
    m, n = np.shape(euler)

    # reshape to M-by-1 vector
    euler = euler.reshape(m*n,1)

    # remvoe 'nan'
    euler = euler[~np.isnan(euler)]

    # reshape back to array
    euler = euler.reshape(m, int( len(euler)/m ) )

    # save ferris
    return(euler)


# -----------------------------------------------------------------------------
def rotator_zxz(eul):
    '''

    
    Parameters
    ----------
    :param :  
    :type : 

    :return :
    :rtype :
    '''
    # From the 3 euler angles for the zxz rotation, compute the rotation matrix
    R = np.zeros([3,3])
    D = np.zeros([3,3])
    C = np.zeros([3,3])
    B = np.zeros([3,3])

    D[0,:] = [ np.cos( eul[0] ), -np.sin( eul[0] ), 0.0 ]
    D[1,:] = [ np.sin( eul[0] ), np.cos( eul[0] ), 0.0 ]
    D[2,:] = [ 0.0, 0.0, 1.0 ]

    C[0,:] = [ 1.0, 0.0, 0.0 ]
    C[1,:] = [ 0.0, np.cos( eul[1] ), -np.sin( eul[1] ) ]
    C[2,:] = [ 0.0, np.sin( eul[1] ), np.cos( eul[1] ) ]

    B[0,:] = [ np.cos( eul[2] ), -np.sin( eul[2] ), 0.0 ] 
    B[1,:] = [ np.sin( eul[2] ), np.cos( eul[2] ), 0.0 ]
    B[2,:] = [ 0.0, 0.0, 1.0 ]

    R = np.matmul(D, C)
    R = np.matmul(R, B)

    return(R)

# -----------------------------------------------------------------------------

def bond(R):
    '''
    
    
    Parameters
    ----------
    :param :  
    :type : 

    :return :
    :rtype :
    '''
    # From the euler rotation matrix, compute the 6-by-6 bond matrix
    M = np.zeros([6,6])
    M[0,:] = [ R[0,0]**2, R[0,1]**2, R[0,2]**2, 2*R[0,1]*R[0,2], 2*R[0,2]*R[0,0], 2*R[0,0]*R[0,1] ]
    M[1,:] = [ R[1,0]**2, R[1,1]**2, R[1,2]**2, 2*R[1,1]*R[1,2], 2*R[1,2]*R[1,0], 2*R[1,0] * R[1,1] ]
    M[2,:] = [ R[2,0]**2, R[2,1]**2, R[2,2]**2, 2*R[2,1]*R[2,2], 2*R[2,2]*R[2,0], 2*R[2,0] * R[2,1] ]
    M[3,:] = [ R[1,0]* R[2,0], R[1,1] * R[2,1], R[1,2] * R[2,2], R[1,1] * R[2,2] + R[1,2]*R[2,1], R[1,0]*R[2,2] + R[1,2]*R[2,0], R[1,1]*R[2,0] + R[1,0]*R[2,1] ]
    M[4,:] = [ R[2,0]* R[0,0], R[2,1] * R[0,1], R[2,2] * R[0,2], R[0,1] * R[2,2] + R[0,2]*R[2,1], R[0,2]*R[2,0] + R[0,0]*R[2,2], R[0,0]*R[2,1] + R[0,1]*R[2,0] ]
    M[5,:] = [ R[0,0]* R[1,0], R[0,1] * R[1,1], R[0,2] * R[1,2], R[0,1] * R[1,2] + R[0,2]*R[1,1], R[0,2]*R[1,0] + R[0,0]*R[1,2], R[0,0]*R[1,1] + R[0,1]*R[1,0] ]

    return(M)
    

# -----------------------------------------------------------------------------
T = np.array(
    [190, 200, 220, 240, 248, 253, 258, 263, 265]
)
A = np.array(
    [0.005, 0.010, 0.031, .268, .635, 1.059, 1.728, 2.769, 3.326]
)*10.e-4
B = np.array(
    [1.537, 1.747, 2.469, 3.495, 4.006, 4.380, 4.696, 5.277, 5.646]
)*10.e-5
C = np.array(
    [1.175, 1.168, 1.129, 1.088, 1.073, 1.062, 1.056, 1.038, 1.024]
)
# Interpolation functions for A, B, and C
A_interp = interp1d(T, A, kind='cubic', fill_value='extrapolate')
B_interp = interp1d(T, B, kind='cubic', fill_value='extrapolate')
C_interp = interp1d(T, C, kind='cubic', fill_value='extrapolate')

def fujita_complex_permittivity(temperature, frequency):
    # 
    # frequency = 1 is equivalent to 1 GHz or 1e9 Hz. The input is in Hz.
    frequency = frequency / 1e9
    A_val = A_interp(T_given)
    B_val = B_interp(T_given)
    C_val = C_interp(T_given)
    epsilon_val = A_val/f + B_val*(f**C_val)
    return epsilon_val
    