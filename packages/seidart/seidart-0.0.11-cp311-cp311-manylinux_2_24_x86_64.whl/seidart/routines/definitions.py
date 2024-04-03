import numpy as np
import pandas as pd
import seidart.routines.materials as mf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as anim
import os.path
from subprocess import call
from scipy.io import FortranFile
import glob2

# =============================================================================
# =========================== Define Class Variables ==========================
# =============================================================================

# We need to define some class variables
class Domain:
    def __init__(self):
        super().__init__()
        self.build()

    def build(self):
        # Initialize variables
        self.geometry = None
        self.dim = None
        self.nx = None
        self.ny = None
        self.nz = None
        self.dx = None
        self.dy = None
        self.dz = None
        self.cpml = None
        self.write = None
        self.imfile = None
        self.exit_status = 1

        # Flag to specify whether the all inputs are fulfilled
        self.seismic_model = False
        self.electromag_model = False

    def para_check(self):
        self.exit_status = 0
        # make sure there's a geometry. This implies whether nx, and nz exist
        if self.geometry is None:
            self.exit_status = 1
            print('No geometry loaded\n')
        if not self.dx or self.dx is None:
            self.exit_status = 1
            print('No step size in the x-direction')
        if not self.dz or self.dz is None:
            self.exit_status = 1
            print('No step size in the y-direction')
        if not self.cpml or self.cpml is None:
            self.exit_status = 1
            print('No cpml thickness is given')

        # Check 2.5D
        if self.dim == '2.5' and exit_status == 0:
            if self.ny is None or self.ny == 'n/a':
                print('No dimension given for y-direction. Assigning default ny=3.')
                self.ny = 3
            if self.dy is None or self.dy == 'n/a':
                self.dy = np.min( [int(self.dx), int(self.dz)])
                print('No step size given for y-direction. Assigning min(dx,dz).')

        # Convert variables to required types. Ny and Dy are already converted if given
        if self.exit_status == 0:
            self.dim = float(self.dim)
            self.nx = int(self.nx)
            self.nz = int(self.nz)
            self.dx = float(self.dx)
            self.dz = float(self.dz)
            self.cpml = int(self.cpml)
        else:
            print('\n Domain inputs are not satisfied. I can"t go on anymore. \n')
            # quit()

# -----------------------------------------------------------------------------

class Material:
    """
    A class to manage materials for simulation purposes.

    Attributes
    ----------
    material_list : numpy.ndarray
        An array to store the list of materials.
    material_flag : bool
        A flag indicating whether the materials were read in successfully.
    material : numpy.ndarray or None
        Stores material information.
    rgb : numpy.ndarray or None
        Stores RGB values for materials (not used currently).
    temp : numpy.ndarray or None
        Stores temperature values for materials.
    rho : numpy.ndarray or None
        Stores density values for materials.
    porosity : numpy.ndarray or None
        Stores porosity values for materials.
    lwc : numpy.ndarray or None
        Stores liquid water content values for materials.
    is_anisotropic : numpy.ndarray or None
        Indicates if the material is anisotropic.
    angfiles : numpy.ndarray or None
        Stores ANG file paths for anisotropic materials.
    functions : Any
        Stores material processing functions.
    """
    # initialize the class
    def __init__(self) -> None:
        """
        Initializes the Material class by building the initial structure.
        """
        super().__init__()
        self.build()

    def build(self) -> None:
        """
        Initializes the material attributes with default values.
        """
        self.material_list = np.array([]) # initialize
        self.material_flag = False # Whether the materials were read in

        # We will assign each of the list variables
        self.material = None
        self.rgb = None
        self.temp = None
        # self.attenuation = None
        self.rho = None
        self.porosity = None
        self.lwc = None
        self.is_anisotropic = None
        self.angfiles = None

        # The processing functions
        self.functions = mf

    def sort_material_list(self) -> None:
        """
        Sorts the material list based on the material properties.
        """
        self.material = self.material_list[:,1]
        self.temp = self.material_list[:,2].astype(float)
        # self.attenuation = self.material_list[:,3].astype(float)
        self.rho = self.material_list[:,3].astype(float)
        self.porosity = self.material_list[:,4].astype(float)
        self.lwc = self.material_list[:,5].astype(float)
        self.is_anisotropic = self.material_list[:,6] == 'True'
        self.angfiles = self.material_list[:,7]

    def para_check(self) -> None:
        """
        Checks the parameters of the material list for completeness.

        It ensures that necessary fields are provided and checks for the presence of .ANG files for anisotropic materials.
        """
        # The fields for the materials in the input are defined as:
        # 'id, R/G/B, Temp., Dens., Por., WC, Anis, ANG_File'
        # but the R/G/B column is deleted

        if len(self.material_list) > 0:
            # Check to make sure the necessary fields are provided
            check = 0

            for row in self.material_list[:,0:6]:
                for val in row:
                    if not val:
                        check = check + 1

        if check == 0:
            file_check = 0
            for ind in range(0, self.material_list.shape[0]):
                if self.material_list[ind,6] == 'True' and not self.material_list[ind,7] or self.material_list[ind,7] == 'n/a':
                    file_check = file_check + 1
        else:
            print('Material inputs aren"t satisfied.')

        if check == 0:
            if file_check == 0:
                self.material_flag = True
            else:
                print('No .ANG file specified for anisotropic material')

# -----------------------------------------------------------------------------
class Model:
    """
    A class to manage the simulation model configuration.

    Attributes
    ----------
    dt : float or None
        The time step size.
    time_steps : int or None
        The total number of time steps in the simulation.
    x : float or None
        The x-coordinate of the source location.
    y : float or None
        The y-coordinate of the source location. Optional, defaults to None.
    z : float or None
        The z-coordinate of the source location.
    f0 : float or None
        The source frequency.
    theta : float or None
        The angle of incidence in the xz-plane. Optional, defaults to 0 if unspecified.
    phi : float or None
        The angle of incidence in the xy-plane. Optional, defaults to 0 if `y` is specified and `phi` is unspecified.
    src : Any
        The source information. Type is unspecified.
    tensor_coefficients : numpy.ndarray or None
        The tensor coefficients for the simulation. Optional, but required for tensor-based simulations.
    compute_coefficients : bool
        A flag indicating whether to compute coefficients. Defaults to True.
    attenuation_coefficients : numpy.ndarray or None
        The attenuation coefficients for the simulation. Optional.
    fref : float or None
        The reference frequency for attenuation. Optional.
    attenuation_fadjust : bool or None
        Flag to adjust frequency for attenuation. Optional.
    exit_status : int
        Status code to indicate the success or failure of parameter checks.
    """
    def __init__(self) -> None:
        """
        Initializes the Model class by building the initial configuration.
        """
        super().__init__()
        self.build()
    
    def build(self) -> None:
        """
        Initializes the simulation model attributes with default values.
        """
        self.dt = None
        self.time_steps = None
        self.x = None
        self.y = None
        self.z = None
        self.f0 = None
        self.theta = None
        self.phi = None
        self.src = None
        self.tensor_coefficients = None
        self.compute_coefficients = True
        self.attenuation_coefficients = None
        self.fref = None
        self.attenuation_fadjust = None
        self.exit_status = 0

    
    def tensor_check(self) -> None:
        """
        Checks if tensor coefficients are specified and valid. Disables coefficient computation if valid.
        """
        # If the tensors are there
        check = 0
        # if not self.tensor_coefficients:
        # 	print('ldkjf')
        for row in self.tensor_coefficients:
            for val in row:
                if not val:
                    check = check + 1
        
        if check == 0:
            self.compute_coefficients = False
    
    def para_check(self) -> None:
        """
        Performs parameter checks for essential simulation settings and updates the exit status accordingly.
        """
        if not self.time_steps:
            self.exit_status = 1
            print('Number of time steps aren"t satisfied.')
        
        if not self.x or not self.z:
            self.exit_status = 1
            print('No source location is specified.')
        
        if not self.f0:
            self.exit_status = 1
            print('No source frequency is specified.')
        
        # in case theta or phi aren't specified we can assign defaults
        if not self.theta:
            self.theta = 0
        
        # if y is specified but not phi
        if self.y and not self.phi:
            self.phi = 0

# -----------------------------------------------------------------------------
class AnimatedGif:
    def __init__(self, size=(640,480) ):
        self.fig = plt.figure()
        self.fig.set_size_inches(size[0]/100, size[1]/100)
        ax = self.fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1)
        ax.set_xticks([])
        ax.set_yticks([])
        self.images = []
        self.background = []
        self.source_location = []
        self.nx = size[0]
        self.nz = size[1]
        self.output_format = 0

    def add(self, image, label='', extent=None ):
        bound = np.max([abs(np.min(image)),abs(np.max(image))])
        plt_im = plt.imshow(
            image,cmap='seismic',
            animated=True,
            extent=(0, (self.nx), (self.nz), 0),
            vmin=-bound,vmax=bound
        )
        plt_bg = plt.imshow(
            self.background,
            alpha = 0.3,
            extent=extent,
            animated = True
        )
        plt.scatter(
            self.source_location[0],
            self.source_location[1],
            marker = '*',
            s = 30,
            linewidths = 1,
            edgecolor = (0.2, 0.2, 0.2, 1 )
        )
        plt_txt = plt.text(
            extent[0] + 20,
            extent[2] + 20,
            label,
            color='red'
        ) # Lower left corner
        self.images.append([plt_im, plt_bg, plt_txt])

    def save(self, filename, frame_rate = 50):
        animation = anim.ArtistAnimation(self.fig,
                                        self.images,
                                        interval = frame_rate,
                                        blit = True
                                        )
        if self.output_format == 1:
            animation.save(filename, dpi = 300)
        else:
            animation.save(filename, dpi = 300, writer = 'imagemagick')

    # -------------------------- Function Definitions -------------------------
def read_dat(
        fn: str, channel: str, domain, is_complex: bool, single: bool =False
    ):
    if single:
        dtype = np.float32 
    else:
        dtype = np.float64 
    
    if domain.dim == 2.5:
        if channel == 'Ex':
            NX = domain.nz
            NY = domain.ny
            NZ = domain.nx-1
        elif channel == 'Ey':
            NX = domain.nz
            NY = domain.ny-1
            NZ = domain.nx
        elif channel == 'Ez':
            NX = domain.nz-1
            NY = domain.ny
            NZ = domain.nx
        else:
            NX = domain.nz
            NY = domain.ny
            NZ = domain.nx
    else:
        if channel == 'Ex':
            NX = domain.nz
            NZ = domain.nx-1
        elif channel == 'Ez':
            NX = domain.nz-1
            NZ = domain.nx
        else:
            NX = domain.nz
            NZ = domain.nx
    #

    with FortranFile(fn, 'r') as f:
        if is_complex:
            if single:
                dat = f.read_reals(dtype=np.float32)#.reshape(nx, nz)
                dat = dat[:(NX*NZ)] + 1j * dat[(NX*NZ):]
            else:
                # Read complex data directly as double precision
                dat = f.read_complex(dtype=np.complex128)#.reshape(nx, nz)
        else:
            if single:
                dat = f.read_reals(dtype = np.float32)
            else:
                dat = f.read_reals(dtype = np.float64)

    if domain.dim == 2.5:
        dat = dat.reshape(NX, NY, NZ)
    else:
        dat = dat.reshape(NX, NZ)

    f.close()
    return(dat)

# =============================================================================
# ============================== Useful Functions =============================
# =============================================================================

def image2int(imfilename):
    # read the image
    img = mpimg.imread(imfilename)

    # Convert RGB to a single value
    rgb_int = np.array(65536*img[:,:,0] +  255*img[:,:,1] + img[:,:,2])

    # Get the unique values of the image
    rgb_uni = np.unique(rgb_int)

    # mat_id = np.array( range(0, len(rgb_uni) ) )
    for ind in range(0, len(rgb_uni) ):
        rgb_int[ rgb_int == rgb_uni[ind] ] = ind

    return rgb_int.astype(int)

# -----------------------------------------------------------------------------
# After computing tensor coefficients we want to append them to the given text
# file. In order to do this, we need to create a new file then move it to the
# original file

def complex2str(complex_vector):
    reals = complex_vector.real[1:]
    comps = complex_vector.imag[1:]
    id = complex_vector.real[0].astype(int)
    m = len(reals)
    complex_string_vector = np.zeros([m], dtype = object)
    for ind in range(m):
        complex_string_vector[ind] = str(reals[ind]) + 'j' + str(comps[ind])
    
    return( str(id) + ',' + ','.join(complex_string_vector))

def str2complex(strsplit):
    '''
    '''
    # strsplit = line.split(',')
    id = int(strsplit[0])
    m = len(strsplit)
    complex_vector = np.zeros([m], dtype = complex)
    complex_vector[0] = id
    for ind in range(1,m):
        realvalue, complexvalue = strsplit[ind].split('j')
        complex_vector[ind] = complex(float(realvalue), float(complexvalue))
    
    return(complex_vector)
        
def append_coefficients(prjfile, tensor, CP = None, dt=1 ):
    '''
    
    # CP is the line identifier (C - stiffness, P - permittivity). This has the
    # ability to be optional since there will is a difference between a 2nd
    # order tensor and a 4th order tensor in regards to length but we might
    # want to include other types of modeling in the future.
    '''
    newfile = 'newfile.txt'

    ogprj = open(prjfile, 'r')
    temp = open(newfile, 'a')
    # We need to append the dt for each modeling type
    if CP == 'C':
        mt = 'S'
    else:
        mt = 'E'

    for line in ogprj.readlines():
        if line[0] == CP:
            line = line.split(',')
            if np.iscomplexobj(tensor):
                temp.write( 
                    CP + ',' + complex2str(tensor[int(float(line[1])),:]) + '\n'
                )
            else:
                temp.write(
                    CP + ',' + \
                        ','.join(tensor[ int(float(line[1])),:].astype(str)) \
                            + '\n' )
        elif line[0] == mt and line[2:4] == 'dt':
            temp.write( mt + ',dt,' + str(dt) + '\n' )
        else:
            temp.write(line)

        # if line[0] == mt:
        # 	line = line.split(',')
        # 	if line[1] == 'dt':
        # 		temp.write( mt + ',dt,' + str(dt) + '\n' )

    call('mv ' + newfile + ' ' + prjfile, shell = True)

# =============================================================================
# ========================= Read/Assign Project File ==========================
# =============================================================================
def loadproject(project_file, domain, material, seismic, electromag):
    # domain, material, seismic, electromag are the objects that we will assign
    # values to
    f = open(project_file)

    # Let the if train begin
    for line in f:
        if line[0] == 'I':
            # There's a trailing new line value
            im = image2int(line[2:-1])
            domain.geometry = im.transpose().astype(int)
            # Get the image file
            domain.imfile = line[2:-1]

        # All domain inputs must be input except for ny and dy
        if line[0] == 'D':
            temp = line.split(',')

            if temp[1] == 'dim':
                domain.dim = float( (temp[2].rsplit())[0])
            if temp[1] == 'nx':
                domain.nx = int( (temp[2].rsplit())[0])
            if temp[1] == 'ny':
                try:
                    domain.ny = int( (temp[2].rsplit())[0])
                except:
                    pass
            if temp[1] == 'nz':
                domain.nz = int( (temp[2].rsplit())[0])
            if temp[1] == 'dx':
                domain.dx = float( (temp[2].rsplit())[0])
            if temp[1] == 'dy':
                try:
                    domain.dy = float( (temp[2].rsplit())[0])
                except:
                    pass
            if temp[1] == 'dz':
                domain.dz = float( (temp[2].rsplit())[0])
            if temp[1] == 'cpml':
                domain.cpml = int( (temp[2].rsplit())[0])
            # if temp[1] == 'write':
            #     domain.write = temp[2].rsplit()
            if temp[1] == 'nmats':
                domain.nmats = int( (temp[2].rsplit())[0])
            if temp[1] == 'cpml_alpha':
                domain.cpml_attenuation = float( (temp[2].rsplit())[0])
            

        if line[0] == 'S':
            temp = line.split(',')
            if temp[1] == 'dt':
                try :
                    seismic.dt = float( (temp[2].rsplit())[0])
                except:
                    pass
            if temp[1] == 'time_steps':
                seismic.time_steps = float( (temp[2].rsplit())[0])
            if temp[1] == 'x':
                seismic.x = float( (temp[2].rsplit())[0])
            if temp[1] == 'y':
                seismic.y = float( (temp[2].rsplit())[0])
            if temp[1] == 'z':
                seismic.z = float( (temp[2].rsplit())[0])
            if temp[1] == 'f0':
                seismic.f0 = float( (temp[2].rsplit())[0])
            if temp[1] == 'theta':
                seismic.theta = float( (temp[2].rsplit())[0])
            if temp[1] == 'phi':
                seismic.phi = float( (temp[2].rsplit())[0])

        if line[0] == 'E':
            temp = line.split(',')
            if temp[1] == 'dt':
                try:
                    electromag.dt = float( (temp[2].rsplit())[0])
                except:
                    pass
            if temp[1] == 'time_steps':
                electromag.time_steps = float( (temp[2].rsplit())[0])
            if temp[1] == 'x':
                electromag.x = float( (temp[2].rsplit())[0])
            if temp[1] == 'y':
                electromag.y = float( (temp[2].rsplit())[0])
            if temp[1] == 'z':
                electromag.z = float( (temp[2].rsplit())[0])
            if temp[1] == 'f0':
                electromag.f0 = float( (temp[2].rsplit())[0])
            if temp[1] == 'theta':
                electromag.theta = float( (temp[2].rsplit())[0])
            if temp[1] == 'phi':
                electromag.phi = float( (temp[2].rsplit())[0])

        if line[0] == 'M':
            line = line[0:-1]
            temp = line.split(',')
            if temp[1] == '0':
                material.material_list = temp[1:]
                material.rgb = temp[3]
            else:
                material.material_list = np.row_stack( (material.material_list, temp[1:]))
                material.rgb = np.append( material.rgb, temp[3] )

        if line[0] == 'C':
            temp = line.split(',')
            # We need to remove the '\n' at the end. Whether the coefficients are
            # given results in a different string
            try:
                temp[-1] = temp[-1].rsplit()[0]
            except:
                temp[-1] = ''

            if temp[1] == '0' or temp[1] == '0.0':
                seismic.tensor_coefficients = temp[1:]
            else:
                seismic.tensor_coefficients = np.row_stack((seismic.tensor_coefficients, temp[1:]))

        # Permittivity coefficients
        if line[0] == 'P':
            if 'j' in line:
                is_complex = True 
            else: 
                is_complex = False 
            
            temp = line.split(',')
            try:
                temp[-1] = temp[-1].rsplit()[0] # An index error will be given if coefficients are provided
            except:
                temp[-1] = ''

            if temp[1] == '0' or temp[1] == '0.0':
                if is_complex:
                    electromag.tensor_coefficients = str2complex(temp[1:])
                else:
                    electromag.tensor_coefficients = temp[1:]
                
            else:
                if is_complex:
                    electromag.tensor_coefficients = np.row_stack( 
                        (electromag.tensor_coefficients, str2complex(temp[1:]) )
                    )
                else:
                    electromag.tensor_coefficients = np.row_stack( 
                        (electromag.tensor_coefficients, temp[1:])
                    )
                    
        # Attenuation coefficients
        if line[0] == 'A':
            temp = line.split(',')
            try:
                electromag.attenuation_coefficients = np.row_stack(
                    (
                        electromag.attenuation_coefficients, 
                        np.array( temp[2:5], dtype = float)
                    )
                )
            except:
                electromag.attenuation_coefficients = np.array(
                    temp[2:5], dtype = float
                )
                
            try: 
                seismic.attenuation_coefficients = np.row_stack(
                    (
                        seismic.attenuation_coefficients,
                        np.array(temp[5:8], dtype = float)
                    )
                )
            except:
                seismic.attenuation_coefficients = np.array(
                    temp[5:8], dtype = float
                )
                
            electromag.fref = float(temp[8])
            seismic.fref = float(temp[9])



    f.close()
    return domain, material, seismic, electromag


# -----------------------------------------------------------------------------
# Make sure variables are in the correct type for Fortran
def prepme(modobj, domain, complex_tensor = True):
    # Check if there are no errors and the coefficients have been computed
    modobj.time_steps = int(modobj.time_steps)
    modobj.f0 = float(modobj.f0)
    modobj.theta = float(modobj.theta)
    modobj.x = float(modobj.x)
    modobj.z = float(modobj.z)
    if complex_tensor:
        modobj.tensor_coefficients = modobj.tensor_coefficients.astype(complex)
    else:
        modobj.tensor_coefficients = modobj.tensor_coefficients.astype(float)
    
    # Put source and domain parameters in correct order
    if domain.dim == 2.5:
        # There are additional values we need to assign
        domain.ny = int(domain.ny)
        domain.dy = float(domain.dy)
        modobj.y = float(modobj.y)
        modobj.phi = float(modobj.phi)

        modobj.src = np.array(
            [
                modobj.x/domain.dx,
                modobj.y/domain.dy,
                modobj.z/domain.dz
            ]
        ).astype(int)
    else:
        modobj.src = np.array(
            [
                modobj.x/domain.dx,
                modobj.z/domain.dz
            ]
        ).astype(int)

    return(modobj, domain)

# ----------------------
# Append coefficients
def coefs2prj(modobj, matobj, domobj, modtype):
    pass


def airsurf(material, domain, N = 2):
    # This can be generalized a little better, but for now...
    airnum = material.material_list[material.material_list[:,1] == 'air', 0]

    if airnum:
        airnum = int(airnum[0])
        gradmatrix = (domain.geometry != airnum).astype(int)
        # Take the gradient in both directions
        gradz = np.diff(gradmatrix, axis = 0)
        gradx = np.diff(gradmatrix, axis = 1)

        # For grady we will append a column of zeros at the beginning so that the value
        # 1 is located at the interface but on the non-air side
        gradzpos = np.row_stack([np.zeros([gradz.shape[1] ]),gradz])
        # For gradx we will append a row of zeros at the beginning
        gradxpos = np.column_stack([np.zeros([gradx.shape[0] ]),gradx])
        # -1 also means that there is an air interface. We will need to append to the
        # end of the array, then we can just flip the sign
        gradzneg = (np.row_stack( [gradz, np.zeros([gradz.shape[1]]) ] ) )
        gradxneg = (np.column_stack( [gradx, np.zeros([gradx.shape[0]]) ] ) )

        # At the surface we want to have 15% of density
        grad = np.zeros( [gradx.shape[0], gradz.shape[1], N] )
        grad[:,:,0] = gradzpos + gradxpos - gradzneg - gradxneg
        grad[ grad[:,:,0]>0, 0] = 0.15

        # We will make the change gradational by splitting the difference each step
        # For instance, 1 - 0.15 = 0.85, so the next percentage will be
        # 0.85/2 + 0.15 and so on
        pct = np.zeros([N])
        pct[0] = 0.15

        for ind in range(1, N):
            pct[ind] = pct[ind-1] + (1-pct[ind-1])/2
            gradzpos = np.row_stack( [np.zeros([gradz.shape[1] ]),gradzpos] )[:-1,:]
            gradxpos = np.column_stack( [np.zeros( [ gradx.shape[0] ] ),gradxpos ])[:,:-1]

            gradzneg = (np.row_stack( [ gradzneg, np.zeros( [gradz.shape[1] ]) ] )[1:,:])
            gradxneg = (np.column_stack( [ gradxneg, np.zeros( [gradx.shape[0] ]) ] )[:,1:])
            grad[:,:, ind] = gradzpos + gradxpos - gradzneg - gradxneg
            grad[ grad[:,:,ind] > 0, ind] = pct[ind]

        gradcomp = np.zeros( [grad.shape[0], grad.shape[1] ])
        for ind in range(N-1, -1, -1):
            gradcomp[ grad[:,:,ind] > 0] = pct[ind]

        gradcomp[ gradcomp == 0] = 1
    else:
        gradcomp = np.ones([int(domain.nx), int(domain.nz) ])

    return(gradcomp)

#===============================
def rcxgen(rgb, domain, material, filename = 'receivers.xyz'):
    """
    Create a receiver list from a given rgb value found in the model image.
    This is only setup for 2D receivers
    """
    rgb = '/'.join(np.array(rgb).astype(str))
    rgbint = int(material.material_list[material.rgb == rgb,0])
    z,x = np.where(domain.geometry == rgbint)
    y = np.zeros([len(x)])
    xyz = np.stack([z*domain.dz,y,x*domain.dx], axis = 1)
    df = pd.DataFrame(xyz, columns = ['X', 'Y', 'Z'])
    df.to_csv(filename, index = False)
    return(xyz)


# ============================== Source Functions =============================
def coherdt(alpha, v, n, dx, loc = 'left'):
    # Return a vector of time delays along the length of the domain. The angle
    # alpha, given in degrees between 90 and -90, is counter clockwise from the
    # x plane. Velocity and dx are in meters/second and meters, respectively.
    if alpha < 0:
        self.dz = None
        self.cpml = None
        self.write = None
        self.imfile = None
        self.exit_status = 1

        # Flag to specify whether the all inputs are fulfilled
        self.seismic_model = False
        self.electromag_model = False

    def para_check(self):
        self.exit_s
    if alpha > 90.0 or alpha < -90:
        alpha = 180 - np.sign(alpha) * alpha
    else:
        print('Alpha must be on the interval (-90,90)')
        quit()

    x = np.arange(0, n*dx, dx)
    dt = x * np.sin( np.deg2rad(alpha) ) / v
    return(dt)

def coherstf( timediff, sf, dt, m, n, cpml, bottom=False,):
    # 'topleft' origin is (0,0), 'topright' origin is (x_n, 0)
    # 'bottomleft' origin is (0, y_n), 'bottomright' origin is (x_n, y_n)
    #
    # timediff is the vector output of coherdt,
    # sf - is the source time function
    # dt is the time interval
    #
    # We want to time shift the source time function for each node along the
    # x-direction then save the file as an m-by-n-by-p matrix
    p = len(sf)
    sfmat = np.zeros([m, n, p], order='F') # m indices are in the y-direction
    cpmlmat = np.zeros([2*cpml + m, 2*cpml + n, p])
    sfarray = np.zeros([m, p])  # p indices are in the t-direction
    ndiff = int(np.round(timediff/dt))
    for ind in range(0, m):
        sfarray[ind,:] = np.roll(sf, timediff[i])
        sfarray[ind,0:timediff[i]] == 0
    if bottom == True:
        sfmat[m,:,:] = sfarray[:]
    else:
        sfmat[0,:,:] = sfarray[:]
    cpmlmat[cpml:,cpml:,:] = sfmat[:,:,:]
    cpmlmat.T.tofile('sourcefunctionmatrix.dat')

def stfvec2mat(sf,xind,zind, m,n, cpml,yind=None):
    # If 2D, y = None. So far we only have 2D. 3D will be implemented later
    p = len(st)
    sfmat = np.zeros([m,n,p], order = 'F')
    sfmat[zind, xind,:] = sf[:]
    cpmlmat = np.zeros([2*cpml + m, 2*cpml + n, p], order = 'F')
    cpmlmat[cpml:,cpml:,:] = sfmat[:,:,:]
    cpmlmat.T.tofile('sourcefunctionmatrix.dat')

def movingsrc(st, txlocs):
    # simulate a moving source given a stationary source function
    pass

# ----------------------------- Plotting Functions ----------------------------
def indvar(modobj, domain):
    nx = int(domain.nx[0])
    nz = int(domain.nz[0])
    dx = float(domain.dx[0])
    dz = float(domain.dz[0])
    dt = float(modobj.dt[0])
    nt = int(modobj.time_steps[0])

    x = np.linspace(0, dx * (nx - 1), nx)
    z = np.linspace(0, dz * (nz - 1), nz)
    t = np.linspace(0, dt * (nt - 1), nt)
    try:
        y = np.linspace(
            0, float(domain.dy[0]) * (int(domain.ny) - 1), int(domain.ny)
        )
    except:
        y = None

    return(x,y,z,t)



# ---------------------------- Processing functions ---------------------------
def agc(ts, k, agctype):
    # Auto-gain normalization using a running window
    # k is the window length
    # agctype is either mean, rms, median
    n = len(ts)

    k2 = int(k/2) # This will floor the number if k is even; (k-1)/2
    if np.mod(k, 2) == 0: # even numbers need will not have a centered window
        k = int( k + 1)

    stat = np.ones([n])
    # Normalize
    if agctype == "std":
        for i in range(0, k2):
            stat[i] = np.std( abs( ts[0:(i+k2)] ) )
            stat[ (n-k2+i) ] = np.std( abs(ts[ (n-2*k2+i):n] ) )
        for i in range(k2,n-k2):
            stat[i] = np.std( abs( ts[ (i-k2):(i+k2) ] ) )
    elif agctype == "mean":
        for i in range(0, k2):
            stat[i] = np.mean( abs( ts[0:(i+k2)] ) )
            stat[ (n-k2+i) ] = np.mean( abs(ts[ (n-2*k2+i):n] ) )
        for i in range(k2,n-k2):
            stat[i] = np.mean( abs( ts[ (i-k2):(i+k2) ] ) )
    else:
        for i in range(0, k2):
            stat[i] = np.std( ts[i:(i+k2)] )
            stat[ (n-k2+i) ] = np.std( ts[ (n-2*k2+i):n] )
        for i in range(k2,n-k2):
            stat[i] = np.std( ts[ (i-k2):(i+k2) ] )

    stat[stat == 0] = 1
    ts = ts/stat
    return ts
