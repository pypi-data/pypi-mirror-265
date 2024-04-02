module cpmlfdtd
    ! This module is specified in the setup.py so there is no need to 
    ! precompile is using the pip install. For individual compilation to 
    ! generate the shared object file to be imported as a python module use:
    !
    ! f2py3 -c --fcompiler=gnu95 -m cpmlfdtd readwrite_routines.f95 \
    !           seismicfdtd.f95 electromagfdtd.f95 cpmlfdtd.f95
    ! 
    ! For debugging: 
    !   gfortran -Wall -Wextra -fcheck=all -Og -g -o your_program_name cpmlfdtd.f95
    ! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ! write_image2 and write_image3 were replicated in the image_write module 
    ! so that complex and real inputs were allowed.
    
    ! The cpmlfdtd package is split up into a few different modules to help 
    ! with organization and debugging 
    
    ! use readwrite_routines
    ! use electromagfdtd 
    ! use seismicfdtd 
    
    implicit none

    contains 
    
    !==========================================================================
    subroutine loadsource(filename, N, srcfn)
        
        implicit none

        integer,parameter :: dp = kind(0.d0)
        character(len=*) :: filename
        integer :: N
        real(kind=dp),dimension(N) :: srcfn
        
        open(unit = 13, form="unformatted", file = trim(filename))
        read(13) srcfn
        
        close(unit = 13)

    end subroutine loadsource

    !==========================================================================
    subroutine loadcpml(filename, image_data)

        implicit none

        integer,parameter :: dp = kind(0.d0)
        character(len=*) :: filename
        real(kind=dp),dimension(:) :: image_data

        open(unit = 13, form="unformatted", file = trim(filename), access='stream')
        read(13) image_data
        close(unit = 13)
    end subroutine loadcpml
    
    !==========================================================================
    subroutine permittivity_write(im, mlist, npoints_pml, nx, nz) 
        ! STIFFNESS_ARRAYS takes a matrix containing the material integer 
        ! identifiers and creates the same size array for each independent 
        ! coefficient of the stiffness matrix along with a density matrix. 
        ! Since we ae using PML boundaries, we will extend the the boundary 
        ! values through the PML region.
        ! 
        ! INPUT 
        !   im (INTEGER)  
        !   mlist (REAL)
        !   eps11(i,j), sig11(i,j), eps22(i,j), sig22, (REAL) -
        !   npoints_pml (INTEGER) - the 
        !   
        ! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        implicit none 
        
        integer :: nx,nz
        integer,parameter :: dp = kind(0.d0)
        integer,dimension(nx,nz) :: im
        integer :: i, j, npoints_pml
        real(kind=dp), dimension(:,:) :: mlist
        real(kind=dp), dimension(2*npoints_pml+nx,2*npoints_pml+nz) :: &
                eps11, eps22, eps33, &
                eps12, eps13, eps23, &
                sig11, sig22, sig33, &
                sig12, sig13, sig23
        
        !f2py3 intent(in):: im, mlist, npoints_pml, nx, nz
        
        ! Allocate space for permittivity and conductivity values
        eps11(:,:) = 0.d0
        eps12(:,:) = 0.d0
        eps13(:,:) = 0.d0
        eps22(:,:) = 0.d0
        eps23(:,:) = 0.d0
        eps33(:,:) = 0.d0
        sig11(:,:) = 0.d0
        sig12(:,:) = 0.d0
        sig13(:,:) = 0.d0
        sig22(:,:) = 0.d0
        sig23(:,:) = 0.d0
        sig33(:,:) = 0.d0
        
        do i=npoints_pml+1,nx + npoints_pml
            do j=npoints_pml+1,nz + npoints_pml
                eps11(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 2)
                eps12(i,j) = mlist( im(i-npoints_pml, j-npoints_pml),3)
                eps13(i,j) = mlist( im(i-npoints_pml, j-npoints_pml),4)
                eps22(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 5)
                eps23(i,j) = mlist( im(i-npoints_pml, j-npoints_pml),6)
                eps33(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 7)
                
                sig11(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 8) 
                sig12(i,j) = mlist( im(i-npoints_pml, j-npoints_pml),9)
                sig13(i,j) = mlist( im(i-npoints_pml, j-npoints_pml),10)
                sig22(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 11)
                sig23(i,j) = mlist( im(i-npoints_pml, j-npoints_pml),12)
                sig33(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 13)
            end do
        end do
        
        ! Extend the boundary values of the stiffnesses into the PML region
        do i = 1,npoints_pml+1
            ! top and bottom
            eps11( i, : ) = eps11(npoints_pml+1,:)
            eps22( i, : ) = eps22(npoints_pml+1,:)
            eps33( i, : ) = eps33(npoints_pml+1,:)
            eps12( i, : ) = eps12(npoints_pml+1,:)
            eps13( i, : ) = eps13(npoints_pml+1,:)
            eps23( i, : ) = eps23(npoints_pml+1,:)

            eps11( nx+npoints_pml-1+i, : ) = eps11(nx+npoints_pml-1,:)
            eps22( nx+npoints_pml-1+i, : ) = eps22(nx+npoints_pml-1,:)
            eps33( nx+npoints_pml-1+i, : ) = eps33(nx+npoints_pml-1,:)
            eps12( nx+npoints_pml-1+i, : ) = eps12(nx+npoints_pml-1,:)
            eps13( nx+npoints_pml-1+i, : ) = eps13(nx+npoints_pml-1,:)
            eps23( nx+npoints_pml-1+i, : ) = eps23(nx+npoints_pml-1,:)
            
            sig11( i, : ) = sig11(npoints_pml+1,:)
            sig22( i, : ) = sig22(npoints_pml+1,:)
            sig33( i, : ) = sig33(npoints_pml+1,:)
            sig12( i, : ) = sig12(npoints_pml+1,:)
            sig13( i, : ) = sig13(npoints_pml+1,:)
            sig23( i, : ) = sig23(npoints_pml+1,:)

            sig11( nx+npoints_pml-1+i, : ) = sig11(nx+npoints_pml-1,:)
            sig22( nx+npoints_pml-1+i, : ) = sig22(nx+npoints_pml-1,:)
            sig33( nx+npoints_pml-1+i, : ) = sig33(nx+npoints_pml-1,:)
            sig13( nx+npoints_pml-1+i, : ) = sig12(nx+npoints_pml-1,:)
            sig13( nx+npoints_pml-1+i, : ) = sig13(nx+npoints_pml-1,:)
            sig23( nx+npoints_pml-1+i, : ) = sig23(nx+npoints_pml-1,:)
            
            !!!!!  ! left and right
            eps11( :, i ) = eps11(:, npoints_pml+1)
            eps22( :, i ) = eps22(:, npoints_pml+1)
            eps33( :, i ) = eps33(:, npoints_pml+1)
            eps12( :, i ) = eps12(:, npoints_pml+1)
            eps13( :, i ) = eps13(:, npoints_pml+1)
            eps23( :, i ) = eps23(:, npoints_pml+1)

            eps11( :, nz+npoints_pml-1+i ) = eps11(:,nz+npoints_pml-1)    
            eps22( :, nz+npoints_pml-1+i ) = eps22(:,nz+npoints_pml-1)
            eps33( :, nz+npoints_pml-1+i ) = eps33(:,nz+npoints_pml-1)
            eps12( :, nz+npoints_pml-1+i ) = eps12(:,nz+npoints_pml-1)    
            eps13( :, nz+npoints_pml-1+i ) = eps13(:,nz+npoints_pml-1)
            eps23( :, nz+npoints_pml-1+i ) = eps23(:,nz+npoints_pml-1)
            
            sig11( :, i ) = sig11(:, npoints_pml+1)
            sig22( :, i ) = sig22(:, npoints_pml+1)
            sig33( :, i ) = sig33(:, npoints_pml+1)
            sig12( :, i ) = sig11(:, npoints_pml+1)
            sig13( :, i ) = sig13(:, npoints_pml+1)
            sig23( :, i ) = sig33(:, npoints_pml+1)
            
            sig11( :, nz+npoints_pml-1+i ) = sig11(:,nz+npoints_pml-1)    
            sig22( :, nz+npoints_pml-1+i ) = sig22(:,nz+npoints_pml-1)
            sig33( :, nz+npoints_pml-1+i ) = sig33(:,nz+npoints_pml-1)
            sig12( :, nz+npoints_pml-1+i ) = sig12(:,nz+npoints_pml-1)    
            sig13( :, nz+npoints_pml-1+i ) = sig13(:,nz+npoints_pml-1)
            sig23( :, nz+npoints_pml-1+i ) = sig23(:,nz+npoints_pml-1)
        end do 

        ! Write each of the matrices to file
        call material_rw('eps11.dat', eps11, .FALSE.)
        call material_rw('eps12.dat', eps12, .FALSE.)
        call material_rw('eps13.dat', eps13, .FALSE.)
        call material_rw('eps22.dat', eps22, .FALSE.)
        call material_rw('eps23.dat', eps23, .FALSE.)
        call material_rw('eps33.dat', eps33, .FALSE.)
        call material_rw('sig11.dat', sig11, .FALSE.)
        call material_rw('sig12.dat', sig12, .FALSE.)
        call material_rw('sig13.dat', sig13, .FALSE.)
        call material_rw('sig22.dat', sig22, .FALSE.)
        call material_rw('sig23.dat', sig23, .FALSE.)
        call material_rw('sig33.dat', sig33, .FALSE.)

    end subroutine permittivity_write
    
    !==========================================================================
    subroutine permittivity_write_c(im, mlist, npoints_pml, nx, nz) 
        ! STIFFNESS_ARRAYS takes a matrix containing the material integer 
        ! identifiers and creates the same size array for each independent 
        ! coefficient of the stiffness matrix along with a density matrix. 
        ! Since we ae using PML boundaries, we will extend the the boundary 
        ! values through the PML region.
        ! 
        ! INPUT 
        !   im (INTEGER)  
        !   mlist (REAL)
        !   eps11(i,j), sig11(i,j), eps22(i,j), sig22, (REAL) -
        !   npoints_pml (INTEGER) - the 
        !   
        ! sigma is related to the complex permittivity value, but it is not a 
        ! complex valued number. The variable mlist is a complex valued array 
        ! but for sigma values, the complex component is 0. 
        ! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        implicit none 
        
        integer :: nx,nz
        integer,parameter :: dp = kind(0.d0)
        integer,dimension(nx,nz) :: im
        integer :: i, j, npoints_pml
        complex(kind=dp), dimension(:,:) :: mlist
        complex(kind=dp), dimension(2*npoints_pml+nx,2*npoints_pml+nz) :: &
                eps11, eps22, eps33, &
                eps12, eps13, eps23
        real(kind=dp), dimension(2*npoints_pml+nx,2*npoints_pml+nz) :: &
                sig11, sig22, sig33, &
                sig12, sig13, sig23
        
        !f2py3 intent(in):: im, mlist, npoints_pml, nx, nz
        
        ! Allocate space for permittivity and conductivity values
        eps11(:,:) = 0.d0
        eps12(:,:) = 0.d0
        eps13(:,:) = 0.d0
        eps22(:,:) = 0.d0
        eps23(:,:) = 0.d0
        eps33(:,:) = 0.d0
        sig11(:,:) = 0.d0
        sig12(:,:) = 0.d0
        sig13(:,:) = 0.d0
        sig22(:,:) = 0.d0
        sig23(:,:) = 0.d0
        sig33(:,:) = 0.d0
        
        do i=npoints_pml+1,nx + npoints_pml
            do j=npoints_pml+1,nz + npoints_pml
                eps11(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 2)
                eps12(i,j) = mlist( im(i-npoints_pml, j-npoints_pml),3)
                eps13(i,j) = mlist( im(i-npoints_pml, j-npoints_pml),4)
                eps22(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 5)
                eps23(i,j) = mlist( im(i-npoints_pml, j-npoints_pml),6)
                eps33(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 7)
                
                sig11(i,j) = abs(mlist( im(i-npoints_pml,j-npoints_pml), 8) )
                sig12(i,j) = abs(mlist( im(i-npoints_pml, j-npoints_pml),9) )
                sig13(i,j) = abs(mlist( im(i-npoints_pml, j-npoints_pml),10) )
                sig22(i,j) = abs(mlist( im(i-npoints_pml,j-npoints_pml), 11) )
                sig23(i,j) = abs(mlist( im(i-npoints_pml, j-npoints_pml),12) )
                sig33(i,j) = abs(mlist( im(i-npoints_pml,j-npoints_pml), 13) )
            end do
        end do
        
        ! Extend the boundary values of the stiffnesses into the PML region
        do i = 1,npoints_pml+1
            ! top and bottom
            eps11( i, : ) = eps11(npoints_pml+1,:)
            eps22( i, : ) = eps22(npoints_pml+1,:)
            eps33( i, : ) = eps33(npoints_pml+1,:)
            eps12( i, : ) = eps12(npoints_pml+1,:)
            eps13( i, : ) = eps13(npoints_pml+1,:)
            eps23( i, : ) = eps23(npoints_pml+1,:)

            eps11( nx+npoints_pml-1+i, : ) = eps11(nx+npoints_pml-1,:)
            eps22( nx+npoints_pml-1+i, : ) = eps22(nx+npoints_pml-1,:)
            eps33( nx+npoints_pml-1+i, : ) = eps33(nx+npoints_pml-1,:)
            eps12( nx+npoints_pml-1+i, : ) = eps12(nx+npoints_pml-1,:)
            eps13( nx+npoints_pml-1+i, : ) = eps13(nx+npoints_pml-1,:)
            eps23( nx+npoints_pml-1+i, : ) = eps23(nx+npoints_pml-1,:)
            
            sig11( i, : ) = sig11(npoints_pml+1,:)
            sig22( i, : ) = sig22(npoints_pml+1,:)
            sig33( i, : ) = sig33(npoints_pml+1,:)
            sig12( i, : ) = sig12(npoints_pml+1,:)
            sig13( i, : ) = sig13(npoints_pml+1,:)
            sig23( i, : ) = sig23(npoints_pml+1,:)

            sig11( nx+npoints_pml-1+i, : ) = sig11(nx+npoints_pml-1,:)
            sig22( nx+npoints_pml-1+i, : ) = sig22(nx+npoints_pml-1,:)
            sig33( nx+npoints_pml-1+i, : ) = sig33(nx+npoints_pml-1,:)
            sig13( nx+npoints_pml-1+i, : ) = sig12(nx+npoints_pml-1,:)
            sig13( nx+npoints_pml-1+i, : ) = sig13(nx+npoints_pml-1,:)
            sig23( nx+npoints_pml-1+i, : ) = sig23(nx+npoints_pml-1,:)
            
            !!!!!  ! left and right
            eps11( :, i ) = eps11(:, npoints_pml+1)
            eps22( :, i ) = eps22(:, npoints_pml+1)
            eps33( :, i ) = eps33(:, npoints_pml+1)
            eps12( :, i ) = eps12(:, npoints_pml+1)
            eps13( :, i ) = eps13(:, npoints_pml+1)
            eps23( :, i ) = eps23(:, npoints_pml+1)

            eps11( :, nz+npoints_pml-1+i ) = eps11(:,nz+npoints_pml-1)    
            eps22( :, nz+npoints_pml-1+i ) = eps22(:,nz+npoints_pml-1)
            eps33( :, nz+npoints_pml-1+i ) = eps33(:,nz+npoints_pml-1)
            eps12( :, nz+npoints_pml-1+i ) = eps12(:,nz+npoints_pml-1)    
            eps13( :, nz+npoints_pml-1+i ) = eps13(:,nz+npoints_pml-1)
            eps23( :, nz+npoints_pml-1+i ) = eps23(:,nz+npoints_pml-1)
            
            sig11( :, i ) = sig11(:, npoints_pml+1)
            sig22( :, i ) = sig22(:, npoints_pml+1)
            sig33( :, i ) = sig33(:, npoints_pml+1)
            sig12( :, i ) = sig11(:, npoints_pml+1)
            sig13( :, i ) = sig13(:, npoints_pml+1)
            sig23( :, i ) = sig33(:, npoints_pml+1)
            
            sig11( :, nz+npoints_pml-1+i ) = sig11(:,nz+npoints_pml-1)    
            sig22( :, nz+npoints_pml-1+i ) = sig22(:,nz+npoints_pml-1)
            sig33( :, nz+npoints_pml-1+i ) = sig33(:,nz+npoints_pml-1)
            sig12( :, nz+npoints_pml-1+i ) = sig12(:,nz+npoints_pml-1)    
            sig13( :, nz+npoints_pml-1+i ) = sig13(:,nz+npoints_pml-1)
            sig23( :, nz+npoints_pml-1+i ) = sig23(:,nz+npoints_pml-1)
        end do 

        ! Write each of the matrices to file
        call material_rwc('eps11.dat', eps11, .FALSE.)
        call material_rwc('eps12.dat', eps12, .FALSE.)
        call material_rwc('eps13.dat', eps13, .FALSE.)
        call material_rwc('eps22.dat', eps22, .FALSE.)
        call material_rwc('eps23.dat', eps23, .FALSE.)
        call material_rwc('eps33.dat', eps33, .FALSE.)
        call material_rw('sig11.dat', sig11, .FALSE.)
        call material_rw('sig12.dat', sig12, .FALSE.)
        call material_rw('sig13.dat', sig13, .FALSE.)
        call material_rw('sig22.dat', sig22, .FALSE.)
        call material_rw('sig23.dat', sig23, .FALSE.)
        call material_rw('sig33.dat', sig33, .FALSE.)

    end subroutine permittivity_write_c
    
    !==========================================================================
    subroutine stiffness_write(im, mlist, npoints_pml, nx, nz, gradient) 
        ! STIFFNESS_ARRAYS takes a matrix containing the material integer identifiers 
        ! and creates the same size array for each independent coefficient of the 
        ! stiffness matrix along with a density matrix. Since we ae using PML
        ! boundaries, we will extend the the boundary values through the PML region.
        ! 
        ! INPUT 
        !   im (INTEGER)  
        !   mlist (REAL)
        !   c11(i,j), c12(i,j), c22(i,j), c66, rho(i,j) (REAL) -
        !   npoints_pml (INTEGER) - the 
        !   
        ! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        implicit none 

        integer,parameter :: dp = kind(0.d0)
        integer :: nx, nz
        integer,dimension(nx,nz) :: im
        integer :: i, j, npoints_pml
        real(kind=dp),dimension(:,:) :: mlist
        real(kind=dp),dimension(nx,nz) :: gradient
        real(kind=dp),dimension(2*npoints_pml+nx,2*npoints_pml+nz) :: c11,c12,c13,&
                                                                    c14,c15,c16, &
                                                                    c22,c23,c24,c25,c26,&
                                                                    c33,c34,c35,c36, &
                                                                    c44,c45,c46, &
                                                                    c55,c56,c66, &
                                                                    rho
        

        !f2py3 intent(in) :: im, mlist, npoints_pml, nx, nz, gradient

        c11(:,:) = 0.d0 
        c12(:,:) = 0.d0 
        c13(:,:) = 0.d0
        c14(:,:) = 0.d0 
        c15(:,:) = 0.d0 
        c16(:,:) = 0.d0 
        c22(:,:) = 0.d0 
        c23(:,:) = 0.d0 
        c24(:,:) = 0.d0 
        c25(:,:) = 0.d0 
        c26(:,:) = 0.d0 
        c33(:,:) = 0.d0 
        c34(:,:) = 0.d0 
        c35(:,:) = 0.d0 
        c36(:,:) = 0.d0 
        c44(:,:) = 0.d0 
        c45(:,:) = 0.d0 
        c46(:,:) = 0.d0 
        c55(:,:) = 0.d0 
        c56(:,:) = 0.d0 
        c66(:,:) = 0.d0 
        rho(:,:) = 0.d0 

        !Assign between the PML regions
        do i = npoints_pml+1, nx+npoints_pml
            do j = npoints_pml+1, nz+npoints_pml
                c11(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 2)
                c12(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 3)
                c13(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 4)
                c14(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 5)
                c15(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 6)
                c16(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 7)
                c22(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 8)
                c23(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 9)
                c24(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 10)
                c25(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 11)
                c26(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 12)
                c33(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 13)
                c34(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 14)
                c35(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 15)
                c36(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 16)
                c44(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 17)
                c45(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 18)
                c46(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 19)
                c55(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 20)
                c56(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 21)
                c66(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 22)
                rho(i,j) = mlist( im(i-npoints_pml,j-npoints_pml), 23) 
            enddo
        enddo

        rho(npoints_pml+1:nx+npoints_pml,npoints_pml+1:nz+npoints_pml) = &
            rho(npoints_pml+1:nx+npoints_pml,npoints_pml+1:nz+npoints_pml)*gradient

        ! Extend the boundary values of the stiffnesses into the PML region
        do i = 1,npoints_pml+1
            ! top 
            c11( i, :) = c11(npoints_pml+1,:)
            c12( i, :) = c12(npoints_pml+1,:)
            c13( i, :) = c13(npoints_pml+1,:)
            c14( i, :) = c14(npoints_pml+1,:)
            c15( i, :) = c15(npoints_pml+1,:)
            c16( i, :) = c16(npoints_pml+1,:)
            c22( i, :) = c22(npoints_pml+1,:)
            c23( i, :) = c23(npoints_pml+1,:)
            c24( i, :) = c24(npoints_pml+1,:)
            c25( i, :) = c25(npoints_pml+1,:)
            c26( i, :) = c26(npoints_pml+1,:)
            c33( i, :) = c33(npoints_pml+1,:)
            c34( i, :) = c34(npoints_pml+1,:)
            c35( i, :) = c35(npoints_pml+1,:)
            c36( i, :) = c36(npoints_pml+1,:)
            c44( i, :) = c44(npoints_pml+1,:)
            c45( i, :) = c45(npoints_pml+1,:)
            c46( i, :) = c46(npoints_pml+1,:)
            c55( i, :) = c55(npoints_pml+1,:)
            c56( i, :) = c56(npoints_pml+1,:)
            c66( i, :) = c66(npoints_pml+1,:)
            rho( i, :) = rho(npoints_pml+1,:)

            ! bottom
            c11( nx+npoints_pml-1+i, :) = c11(nx+npoints_pml-1,:)
            c12( nx+npoints_pml-1+i, :) = c12(nx+npoints_pml-1,:)
            c13( nx+npoints_pml-1+i, :) = c13(nx+npoints_pml-1,:)
            c14( nx+npoints_pml-1+i, :) = c14(nx+npoints_pml-1,:)
            c15( nx+npoints_pml-1+i, :) = c15(nx+npoints_pml-1,:)
            c16( nx+npoints_pml-1+i, :) = c16(nx+npoints_pml-1,:)
            c22( nx+npoints_pml-1+i, :) = c22(nx+npoints_pml-1,:)
            c23( nx+npoints_pml-1+i, :) = c23(nx+npoints_pml-1,:)
            c24( nx+npoints_pml-1+i, :) = c24(nx+npoints_pml-1,:)
            c25( nx+npoints_pml-1+i, :) = c25(nx+npoints_pml-1,:)
            c26( nx+npoints_pml-1+i, :) = c26(nx+npoints_pml-1,:)
            c33( nx+npoints_pml-1+i, :) = c33(nx+npoints_pml-1,:)
            c34( nx+npoints_pml-1+i, :) = c34(nx+npoints_pml-1,:)
            c35( nx+npoints_pml-1+i, :) = c35(nx+npoints_pml-1,:)
            c36( nx+npoints_pml-1+i, :) = c36(nx+npoints_pml-1,:)
            c44( nx+npoints_pml-1+i, :) = c44(nx+npoints_pml-1,:)
            c45( nx+npoints_pml-1+i, :) = c45(nx+npoints_pml-1,:)
            c46( nx+npoints_pml-1+i, :) = c46(nx+npoints_pml-1,:)
            c55( nx+npoints_pml-1+i, :) = c55(nx+npoints_pml-1,:)
            c56( nx+npoints_pml-1+i, :) = c56(nx+npoints_pml-1,:)
            c66( nx+npoints_pml-1+i, :) = c66(nx+npoints_pml-1,:)
            rho( nx+npoints_pml-1+i, :) = rho(nx+npoints_pml-1,:)

            ! left 
            c11( :, i) = c11(:, npoints_pml+1)
            c12( :, i) = c12(:, npoints_pml+1)
            c13( :, i) = c13(:, npoints_pml+1)
            c14( :, i) = c14(:, npoints_pml+1)
            c15( :, i) = c15(:, npoints_pml+1)
            c16( :, i) = c16(:, npoints_pml+1)
            c22( :, i) = c22(:, npoints_pml+1)
            c23( :, i) = c23(:, npoints_pml+1)
            c24( :, i) = c24(:, npoints_pml+1)
            c25( :, i) = c25(:, npoints_pml+1)
            c26( :, i) = c26(:, npoints_pml+1)
            c33( :, i) = c33(:, npoints_pml+1)
            c34( :, i) = c34(:, npoints_pml+1)
            c35( :, i) = c35(:, npoints_pml+1)
            c36( :, i) = c36(:, npoints_pml+1)
            c44( :, i) = c44(:, npoints_pml+1)
            c45( :, i) = c45(:, npoints_pml+1)
            c46( :, i) = c46(:, npoints_pml+1)
            c55( :, i) = c55(:, npoints_pml+1)
            c56( :, i) = c56(:, npoints_pml+1)
            c66( :, i) = c66(:, npoints_pml+1)
            rho( :, i) = rho(:, npoints_pml+1)

            ! right
            c11( :, nz+npoints_pml-1+i) = c11(:,nz+npoints_pml-1)
            c12( :, nz+npoints_pml-1+i) = c12(:,nz+npoints_pml-1)
            c13( :, nz+npoints_pml-1+i) = c13(:,nz+npoints_pml-1)      
            c14( :, nz+npoints_pml-1+i) = c14(:,nz+npoints_pml-1)      
            c15( :, nz+npoints_pml-1+i) = c15(:,nz+npoints_pml-1)      
            c16( :, nz+npoints_pml-1+i) = c16(:,nz+npoints_pml-1)      
            c22( :, nz+npoints_pml-1+i) = c22(:,nz+npoints_pml-1)
            c23( :, nz+npoints_pml-1+i) = c23(:,nz+npoints_pml-1)
            c24( :, nz+npoints_pml-1+i) = c24(:,nz+npoints_pml-1)
            c25( :, nz+npoints_pml-1+i) = c25(:,nz+npoints_pml-1)
            c26( :, nz+npoints_pml-1+i) = c26(:,nz+npoints_pml-1)
            c33( :, nz+npoints_pml-1+i) = c33(:,nz+npoints_pml-1)
            c34( :, nz+npoints_pml-1+i) = c34(:,nz+npoints_pml-1)
            c35( :, nz+npoints_pml-1+i) = c35(:,nz+npoints_pml-1)
            c36( :, nz+npoints_pml-1+i) = c36(:,nz+npoints_pml-1)
            c44( :, nz+npoints_pml-1+i) = c44(:,nz+npoints_pml-1)
            c45( :, nz+npoints_pml-1+i) = c45(:,nz+npoints_pml-1)
            c46( :, nz+npoints_pml-1+i) = c46(:,nz+npoints_pml-1)
            c55( :, nz+npoints_pml-1+i) = c55(:,nz+npoints_pml-1)      
            c56( :, nz+npoints_pml-1+i) = c56(:,nz+npoints_pml-1)      
            c66( :, nz+npoints_pml-1+i) = c66(:,nz+npoints_pml-1)
            rho( :, nz+npoints_pml-1+i) = rho(:,nz+npoints_pml-1)

        end do 

        ! Write each of the matrices to file
        call material_rw('c11.dat', c11, .FALSE.)
        call material_rw('c12.dat', c12, .FALSE.)
        call material_rw('c13.dat', c13, .FALSE.)
        call material_rw('c14.dat', c14, .FALSE.)
        call material_rw('c15.dat', c15, .FALSE.)
        call material_rw('c16.dat', c16, .FALSE.)
        call material_rw('c22.dat', c22, .FALSE.)
        call material_rw('c23.dat', c23, .FALSE.)
        call material_rw('c24.dat', c24, .FALSE.)
        call material_rw('c25.dat', c25, .FALSE.)
        call material_rw('c26.dat', c26, .FALSE.)
        call material_rw('c33.dat', c33, .FALSE.)
        call material_rw('c34.dat', c34, .FALSE.)
        call material_rw('c35.dat', c35, .FALSE.)
        call material_rw('c36.dat', c36, .FALSE.)
        call material_rw('c44.dat', c44, .FALSE.)
        call material_rw('c45.dat', c45, .FALSE.)
        call material_rw('c46.dat', c46, .FALSE.)
        call material_rw('c55.dat', c55, .FALSE.)
        call material_rw('c56.dat', c56, .FALSE.)
        call material_rw('c66.dat', c66, .FALSE.)
        call material_rw('rho.dat', rho, .FALSE. )

    end subroutine stiffness_write
    
    !==========================================================================
    subroutine attenuation_write(im, alist, npoints_pml, nx, nz, cpmlvalue, seismic) 
        ! STIFFNESS_ARRAYS takes a matrix containing the material integer identifiers 
        ! and creates the same size array for each independent coefficient of the 
        ! stiffness matrix along with a density matrix. Since we ae using PML
        ! boundaries, we will extend the the boundary values through the PML region.
        ! 
        ! INPUT 
        !   im (INTEGER)  
        !   mlist (REAL)
        !   c11(i,j), c12(i,j), c22(i,j), c66, rho(i,j) (REAL) -
        !   npoints_pml (INTEGER) - the 
        !   
        ! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        implicit none 

        integer,parameter :: dp = kind(0.d0)
        integer :: nx, nz
        integer,dimension(nx,nz) :: im
        integer :: i, j, npoints_pml
        real(kind=dp),dimension(:,:) :: alist
        real(kind=dp) :: cpmlvalue
        logical :: seismic
        real(kind=dp),dimension(2*npoints_pml+nx,2*npoints_pml+nz) :: gamma_x, gamma_y, gamma_z
                                                                     

        !f2py3 intent(in) :: im, alist, npoints_pml, nx, nz, gradient
        
        ! call material_rw('rho.dat', rho, .TRUE. )
        gamma_x(:,:) = cpmlvalue 
        gamma_y(:,:) = cpmlvalue 
        gamma_z(:,:) = cpmlvalue 
        
        !Assign between the PML regions
        do i = npoints_pml+1, nx+npoints_pml
            do j = npoints_pml+1, nz+npoints_pml
                gamma_x(i,j) = alist( im(i-npoints_pml,j-npoints_pml), 1)!*dt/rho(i,j)
                gamma_y(i,j) = alist( im(i-npoints_pml,j-npoints_pml), 2)!*dt/rho(i,j)
                gamma_z(i,j) = alist( im(i-npoints_pml,j-npoints_pml), 3)!*dt/rho(i,j)
            enddo
        enddo
        
        ! Write each of the matrices to file
        if ( seismic ) then
            call material_rw('gammas_x.dat', gamma_x, .FALSE.)
            call material_rw('gammas_y.dat', gamma_y, .FALSE.)
            call material_rw('gammas_z.dat', gamma_z, .FALSE.)
        else
            call material_rw('gammae_x.dat', gamma_x, .FALSE.)
            call material_rw('gammae_y.dat', gamma_y, .FALSE.)
            call material_rw('gammae_z.dat', gamma_z, .FALSE.)
        end if    

    end subroutine attenuation_write
    
    !==========================================================================
    subroutine material_rw(filename, image_data, readfile)

        implicit none
        
        integer,parameter :: dp = kind(0.d0)
        character(len=*) :: filename
        real(kind=dp),dimension(:,:) :: image_data
        logical :: readfile
        
        open(unit = 13, form="unformatted", file = trim(filename))
        
        if ( readfile ) then
            read(13) image_data
        else
            write(13) image_data
        endif
        
        close(unit = 13)

    end subroutine material_rw
    
    !==========================================================================
    subroutine material_rwc(filename, image_data, readfile)

        implicit none
        
        integer,parameter :: dp = kind(0.d0)
        character(len=*) :: filename
        complex(kind=dp),dimension(:,:) :: image_data
        logical :: readfile
        
        open(unit = 13, form="unformatted", file = trim(filename))
        
        if ( readfile ) then
            read(13) image_data
        else
            write(13) image_data
        endif
        
        close(unit = 13)

    end subroutine material_rwc

    ! =========================================================================
    subroutine write_image2(image_data, nx, nz, src, it, channel, SINGLE)
    
        implicit none

        integer, parameter :: dp = kind(0.d0)
        integer :: nx, nz, it
        integer,dimension(2) :: src
        real(kind=dp) :: image_data(nx, nz)
        character(len=2) :: channel
        character(len=100) :: filename
        logical :: SINGLE

        ! WRITE (filename, "(a2, i6.6, '.dat')" ) channel, it
        WRITE (filename, "(a2, a1, i6.6, a1, i0, a1, i0, a1, a4)" ) &
                    channel,'.', it,'.', src(1),'.', src(2), '.','.dat'
        open(unit = 10, form = 'unformatted', file = trim(filename) )

        if (SINGLE) then
            write(10) sngl(image_data)
        else
            write(10) image_data 
        end if 


        close(unit = 10)

    end subroutine write_image2
    
    ! ---------------------------------------------------------------------
    subroutine write_image2c(image_data, nx, nz, src, it, channel, SINGLE)
    
        implicit none

        integer, parameter :: dp = kind(0.d0)
        integer, parameter :: sp = kind(1e0)
        integer :: nx, nz, it
        integer,dimension(2) :: src
        complex(kind=dp) :: image_data(nx, nz)
        real(kind=sp) :: real_part(nx, nz), imag_part(nx, nz)
        character(len=2) :: channel
        character(len=100) :: filename
        logical :: SINGLE

        ! WRITE (filename, "(a2, i6.6, '.dat')" ) channel, it
        WRITE (filename, "(a2, a1, i6.6, a1, i0, a1, i0, a1, a4)" ) &
                    channel,'.', it,'.', src(1),'.', src(2), '.','.dat'
        
        open(unit = 10, form = 'unformatted', file = trim(filename) )
        if (SINGLE) then
            real_part = real(image_data, kind = sp)
            imag_part = aimag(image_data)
            write(10) real_part, imag_part
        else
            ! For double precision data, there is no need to split the real and
            ! imaginary parts since the data isn't being converted to single
            ! precision. 
            write(10) image_data 
        end if 
        
        close(unit = 10)

    end subroutine write_image2c
    
    ! =========================================================================
    subroutine write_image3(image_data, nx, ny, nz, src, it, channel, SINGLE)
    
        implicit none
    
        integer, parameter :: dp = kind(0.d0)
        integer :: nx, ny, nz, it
        integer,dimension(3) :: src
        real(kind=dp) :: image_data(nx, ny, nz)
        character(len=2) :: channel
        character(len=80) :: filename
        logical :: SINGLE
        
        WRITE (filename, "(a2, a1, i6.6, a1, i0, a1, i0, a1, i0, a4)" ) &
                        channel,'.',it,'.', src(1),'.',src(2),'.',src(3),'.dat'
        
        open(unit = 10, form = 'unformatted', file = trim(filename) )
        
        if (SINGLE) then
            write(10) sngl(image_data)
        else
            write(10) image_data 
        end if 
        
        close(unit = 10)

    end subroutine write_image3
    
    ! =========================================================================    
    ! Computations are done in double precision and written to binary as single
    ! precision unless specified by the optional logical, OUTPUT_SINGLE.
    subroutine seismic2(nx, nz, dx, dz, npoints_pml, src, nstep, OUTPUT_SINGLE)

        ! 2D elastic finite-difference code in velocity and stress formulation
        ! with Convolutional-PML (C-PML) absorbing conditions for an 
        ! anisotropic medium
        !
        ! If using this program please give credit to the following: 
        !
        ! Dimitri Komatitsch, University of Pau, France, April 2007.
        ! Anisotropic implementation by Roland Martin and Dimitri Komatitsch, 
        ! University of Pau, France, April 2007.
        
        ! The second-order staggered-grid formulation of Madariaga (1976) and 
        ! Virieux (1986) is used:
    
        ! INPUT
        !   im (INTEGER)
        !   nx, ny (INTEGER)
        !   c11, c12, c22, c66, rho (REAL)
        !   dx, dy (REAL)
        !   npoints_pml (INTEGER) - the thickness of the pml
        ! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        
            implicit none
        
            integer, parameter :: dp=kind(0.d0)

            ! total number of grid points in each direction of the grid
            integer :: nx
            integer :: nz
        
            ! thickness of the PML layer in grid points
            integer :: npoints_pml
            ! integer, dimension(nx,nz)
            real(kind=dp), dimension(nx,nz) :: c11, c13, c15, c33, c35, c55, rho
            real(kind=dp) :: deltarho
        
            ! total number of time steps
            integer :: nstep
        
            ! time step in seconds 
            real(kind=dp) :: DT
            real(kind=dp) :: dx, dz 

            ! source
            integer,dimension(:) :: src
            integer :: isource, jsource
        
            ! velocity threshold above which we consider that the code became unstable
            real(kind=dp), parameter :: STABILITY_THRESHOLD = 1.d+25
        
            ! main arrays
            real(kind=dp), dimension(nx,nz) :: vx,vz,sigmaxx,sigmazz,sigmaxz
                   
            ! arrays for the memory variables
            ! could declare these arrays in PML only to save a lot of memory, but proof of concept only here
            real(kind=dp), dimension(NX,NZ) :: &
                memory_dvx_dx, &
                memory_dvx_dz, &
                memory_dvz_dx, &
                memory_dvz_dz, &
                memory_dsigmaxx_dx, &
                memory_dsigmazz_dz, &
                memory_dsigmaxz_dx, &
                memory_dsigmaxz_dz
        
            real(kind=dp) :: &
                value_dvx_dx, &
                value_dvx_dz, &
                value_dvz_dx, &
                value_dvz_dz, &
                value_dsigmaxx_dx, &
                value_dsigmazz_dz, &
                value_dsigmaxz_dx, &
                value_dsigmaxz_dz
        
            ! 1D arrays for the damping profiles
            real(kind=dp), dimension(nx) :: K_x, alpha_x, a_x, b_x, &
                                        K_x_half, alpha_x_half, &
                                        a_x_half, b_x_half
            real(kind=dp), dimension(nz) ::K_z, alpha_z, a_z, b_z, &
                                        K_z_half, alpha_z_half, &
                                        a_z_half, b_z_half
        
            real(kind=dp), dimension(nx,nz) :: gamma_x, gamma_z
            ! for the source
            real(kind=dp),dimension(nstep) :: srcx, srcz
        
            integer :: i,j,it
        
            real(kind=dp) :: velocnorm

            ! Boolean flag to save as double precision or single precision 
            logical :: SINGLE
            logical, intent(in), optional :: OUTPUT_SINGLE 

            ! Name the f2py inputs 
            !f2py3 intent(in) :: nx, nx, dx, dx,
            !f2py3 intent(in) :: noints_pml, src, nstep, OUTPUT_SINGLE

            ! The default data output is single precision unless OUTPUT_SINGLE is 
            ! set to .FALSE.
            if (present(OUTPUT_SINGLE)) then 
                SINGLE = OUTPUT_SINGLE 
            else
                SINGLE = .TRUE.
            endif
        
            ! -------------------- Load Stiffness Coefficients --------------------
        
            call material_rw('c11.dat', c11, .TRUE.)
            call material_rw('c13.dat', c13, .TRUE.)
            call material_rw('c15.dat', c15, .TRUE.)
            call material_rw('c33.dat', c33, .TRUE.)
            call material_rw('c35.dat', c35, .TRUE.)
            call material_rw('c55.dat', c55, .TRUE.)
            call material_rw('rho.dat', rho, .TRUE.)
            
            ! ------------------- Load Attenuation Coefficients --------------------
            call material_rw('gammas_x.dat', gamma_x, .TRUE.)
            call material_rw('gammas_z.dat', gamma_x, .TRUE.)
            
            ! ------------------------ Assign some constants -----------------------
        
            isource = src(1)+npoints_pml
            jsource = src(2)+npoints_pml
        
            DT = minval( (/dx,dz/) )/ &
                (sqrt( 3.d0*( maxval( (/ c11/rho, c33/rho /) ) ) ) ) 

                ! ================================ LOAD SOURCE ================================
        
            call loadsource('seismicsourcex.dat', nstep, srcx)
            ! We are using the coordinate names x, Z but the math computes the source in 
            ! the x-z plane
            call loadsource('seismicsourcez.dat', nstep, srcz)
        
            ! -----------------------------------------------------------------------------
            !--- define profile of absorption in PML region

            ! Initialize PML 
            K_x(:) = 1.d0
            K_x_half(:) = 1.d0
            alpha_x(:) = 0.d0
            alpha_x_half(:) = 0.d0
            a_x(:) = 0.d0
            a_x_half(:) = 0.d0
            b_x(:) = 0.d0 
            b_x_half(:) = 0.d0

            K_z(:) = 1.d0
            K_z_half(:) = 1.d0 
            alpha_z(:) = 0.d0
            alpha_z_half(:) = 0.d0
            a_z(:) = 0.d0
            a_z_half(:) = 0.d0
            b_z(:) = 0.d0
            b_z_half(:) = 0.d0

        ! ------------------------------ Load the boundary ----------------------------        
            call loadcpml('kappax_cpml.dat', K_x)
            call loadcpml('alphax_cpml.dat', alpha_x)
            call loadcpml('acoefx_cpml.dat', a_x)
            call loadcpml('bcoefx_cpml.dat', b_x)
            
            call loadcpml('kappaz_cpml.dat', K_z)
            call loadcpml('alphaz_cpml.dat', alpha_z)
            call loadcpml('acoefz_cpml.dat', a_z)
            call loadcpml('bcoefz_cpml.dat', b_z)
            
            call loadcpml('kappax_half_cpml.dat', K_x_half)
            call loadcpml('alphax_half_cpml.dat', alpha_x_half)
            call loadcpml('acoefx_half_cpml.dat', a_x_half)
            call loadcpml('bcoefx_half_cpml.dat', b_x_half)
            
            call loadcpml('kappaz_half_cpml.dat', K_z_half)
            call loadcpml('alphaz_half_cpml.dat', alpha_z_half)
            call loadcpml('acoefz_half_cpml.dat', a_z_half)
            call loadcpml('bcoefz_half_cpml.dat', b_z_half)
        
            ! =============================================================================
        
        
            ! initialize arrays
            vx(:,:) = 0.d0
            vz(:,:) = 0.d0
            sigmaxx(:,:) = 0.d0
            sigmazz(:,:) = 0.d0
            sigmaxz(:,:) = 0.d0
        
            ! PML
            memory_dvx_dx(:,:) = 0.d0
            memory_dvx_dz(:,:) = 0.d0
            memory_dvz_dx(:,:) = 0.d0
            memory_dvz_dz(:,:) = 0.d0
            memory_dsigmaxx_dx(:,:) = 0.d0
            memory_dsigmazz_dz(:,:) = 0.d0
            memory_dsigmaxz_dx(:,:) = 0.d0
            memory_dsigmaxz_dz(:,:) = 0.d0
        
            !---
            !---  beginning of time loop
            !---
        
            do it = 1,NSTEP
            !------------------------------------------------------------
            ! compute stress sigma and update memory variables for C-PML
            !------------------------------------------------------------
            do j = 2,NZ
                do i = 1,NX-1
        
                value_dvx_dx = (vx(i+1,j) - vx(i,j)) / DX
                value_dvz_dz = (vz(i,j) - vz(i,j-1)) / DZ
                value_dvz_dx = (vz(i+1,j) - vz(i,j)) / DX
                value_dvx_dz = (vx(i,j) - vx(i,j-1)) / DZ

                memory_dvx_dx(i,j) = b_x_half(j) * memory_dvx_dx(i,j) + &
                                        a_x_half(i) * value_dvx_dx
                memory_dvz_dz(i,j) = b_z(j) * memory_dvz_dz(i,j) + &
                                        a_z(j) * value_dvz_dz
                memory_dvx_dz(i,j) = b_z_half(j) * memory_dvx_dz(i,j) + &
                                        a_z_half(j) * value_dvx_dz 
                memory_dvz_dx(i,j) = b_x(i) * memory_dvz_dx(i,j) + &
                                        a_x(i) * value_dvz_dx

                value_dvx_dx = value_dvx_dx / K_x_half(i) + memory_dvx_dx(i,j)
                value_dvz_dz = value_dvz_dz / K_z(j) + memory_dvz_dz(i,j)
                value_dvz_dx = value_dvz_dx / K_x(i) + memory_dvz_dx(i,j)
                value_dvx_dz = value_dvx_dz / K_z_half(j) + memory_dvx_dz(i,j)
                
                sigmaxx(i,j) = sigmaxx(i,j) + &
                    ( ( ( c11(i+1,j) + 2*c11(i,j) + c11(i,j-1) )/4) * value_dvx_dx + &
                    ( ( c13(i+1,j) + 2*c13(i,j) + c13(i,j-1) )/4) * value_dvz_dz + &
                    ( ( c15(i+1,j) + 2*c15(i,j) + c15(i,j-1) )/4) * &
                            (value_dvz_dx + value_dvx_dz) ) * DT
                sigmazz(i,j) = sigmazz(i,j) + &
                    ( ( ( c13(i+1,j) + 2*c13(i,j) + c13(i,j-1) )/4) * value_dvx_dx + &
                    ( ( c33(i+1,j) + 2*c33(i,j) + c33(i,j-1) )/4) * value_dvz_dz + &
                    ( ( c35(i+1,j) + 2*c35(i,j) + c35(i,j-1) )/4) * &
                            (value_dvz_dx + value_dvx_dz) ) * DT
        
                enddo
            enddo
        
            do j = 1,NZ-1
                do i = 2,NX
        
                value_dvx_dx = (vx(i,j) - vx(i-1,j)) / DX
                value_dvz_dz = (vz(i,j+1) - vz(i,j)) / DZ
                value_dvz_dx = (vz(i,j) - vz(i-1,j)) / DX
                value_dvx_dz = (vx(i,j+1) - vx(i,j)) / DZ
                
                memory_dvx_dx(i,j) = b_x_half(i) * memory_dvx_dx(i,j) + &
                                        a_x_half(i) * value_dvx_dx
                memory_dvz_dz(i,j) = b_z(j) * memory_dvz_dz(i,j) + &
                                        a_z(j) * value_dvz_dz
                memory_dvx_dz(i,j) = b_z_half(j) * memory_dvx_dz(i,j) + &
                                        a_z_half(j) * value_dvx_dz 
                memory_dvz_dx(i,j) = b_x(i) * memory_dvz_dx(i,j) + &
                                        a_x(i) * value_dvz_dx
                
                value_dvx_dx = value_dvx_dx / K_x_half(i) + memory_dvx_dx(i,j)
                value_dvz_dz = value_dvz_dz / K_z(j) + memory_dvz_dz(i,j)
                value_dvz_dx = value_dvz_dx / K_x(i) + memory_dvz_dx(i,j)
                value_dvx_dz = value_dvx_dz / K_z_half(j) + memory_dvx_dz(i,j)
        
                sigmaxz(i,j) = sigmaxz(i,j) + &
                    ( ( (c15(i,j+1) + 2*c15(i,j) + c15(i-1,j))/4) * value_dvx_dx + &
                    ( (c35(i,j+1) + 2*c35(i,j) + c35(i-1,j))/4) * value_dvz_dz + &
                    ( (c55(i,j+1) + 2*c55(i,j) + c55(i-1,j))/4) * &
                            (value_dvz_dx + value_dvx_dz) ) * DT
        
                enddo
            enddo
        
            !--------------------------------------------------------
            ! compute velocity and update memory variables for C-PML
            !--------------------------------------------------------
            do j = 2,NZ
                do i = 2,NX
        
                deltarho = ( 2*rho(i,j) + rho(i-1,j) + rho(i,j-1) )/4
                value_dsigmaxx_dx = (sigmaxx(i,j) - sigmaxx(i-1,j)) / DX
                value_dsigmaxz_dz = (sigmaxz(i,j) - sigmaxz(i,j-1)) / DZ
        
                memory_dsigmaxx_dx(i,j) = b_x(i) * memory_dsigmaxx_dx(i,j) + &
                            a_x(i) * value_dsigmaxx_dx
                memory_dsigmaxz_dz(i,j) = b_z(j) * memory_dsigmaxz_dz(i,j) + &
                            a_z(j) * value_dsigmaxz_dz
        
                value_dsigmaxx_dx = value_dsigmaxx_dx / K_x(i) + &
                            memory_dsigmaxx_dx(i,j)
                value_dsigmaxz_dz = value_dsigmaxz_dz / K_z(j) + &
                            memory_dsigmaxz_dz(i,j)
        
                vx(i,j) = vx(i,j)*(1 - gamma_x(i,j) ) + (value_dsigmaxx_dx + value_dsigmaxz_dz) * DT / rho(i,j)
        
                enddo
            enddo
        
            do j = 1,NZ-1
                do i = 1,NX-1
        
                deltarho = ( 2*rho(i,j) + rho(i+1,j) + rho(i,j+1) )/4
                value_dsigmaxz_dx = (sigmaxz(i+1,j) - sigmaxz(i,j)) / DX
                value_dsigmazz_dz = (sigmazz(i,j+1) - sigmazz(i,j)) / DZ
        
                memory_dsigmaxz_dx(i,j) = b_x_half(i) * memory_dsigmaxz_dx(i,j) + &
                            a_x_half(i) * value_dsigmaxz_dx
                memory_dsigmazz_dz(i,j) = b_z_half(j) * memory_dsigmazz_dz(i,j) + &
                            a_z_half(j) * value_dsigmazz_dz
        
                value_dsigmaxz_dx = value_dsigmaxz_dx / K_x_half(i) + memory_dsigmaxz_dx(i,j)
                value_dsigmazz_dz = value_dsigmazz_dz / K_z_half(j) + memory_dsigmazz_dz(i,j)
        
                vz(i,j) = vz(i,j)*(1 - gamma_z(i,j) ) + (value_dsigmaxz_dx + value_dsigmazz_dz) * DT / deltarho
        
                enddo
            enddo
        
            ! Add the source term
            vx(isource,jsource) = vx(isource,jsource) + srcx(it) * DT / rho(isource,jsource)
            vz(isource,jsource) = vz(isource,jsource) + srcz(it) * DT / rho(isource,jsource)
        
            ! Dirichlet conditions (rigid boundaries) on the edges or at the 
            ! bottom of the PML layers
            vx(1,:) = 0.d0
            vx(NX,:) = 0.d0
        
            vx(:,1) = 0.d0
            vx(:,NZ) = 0.d0
        
            vz(1,:) = 0.d0
            vz(NX,:) = 0.d0
        
            vz(:,1) = 0.d0
            vz(:,NZ) = 0.d0
        
            ! print maximum of norm of velocity
            velocnorm = maxval(sqrt(vx**2 + vz**2))
            if (velocnorm > STABILITY_THRESHOLD) stop 'code became unstable and blew up'
        
            call write_image2(vx, nx, nz, src, it, 'Vx', SINGLE)
            call write_image2(vz, nx, nz, src, it, 'Vz', SINGLE)
        
            enddo   ! end of time loop
    end subroutine seismic2
    
    ! =========================================================================
    subroutine electromag2(nx, nz, dx, dz, npoints_pml, src, nstep, OUTPUT_SINGLE)

        ! 2D elastic finite-difference code in velocity and stress formulation
        ! with Convolutional-PML (C-PML) absorbing conditions for an anisotropic medium

        ! Dimitri Komatitsch, University of Pau, France, April 2007.
        ! Anisotropic implementation by Roland Martin and Dimitri Komatitsch, University of Pau, France, April 2007.

        ! The second-order staggered-grid formulation of Madariaga (1976) and Virieux (1986) is used:
        !
        !            ^ y
        !            |
        !            |
        !
        !            +-------------------+
        !            |                   |
        !            |                   |
        !            |                   |
        !            |                   |
        !            |        v_y        |
        !   sigma_xy +---------+         |
        !            |         |         |
        !            |         |         |
        !            |         |         |
        !            |         |         |
        !            |         |         |
        !            +---------+---------+  ---> x
        !           v_x    sigma_xx
        !                  sigma_yy
        !
        ! IMPORTANT : all our CPML codes work fine in single precision as well (which is significantly faster).
        !             If you want you can thus force automatic conversion to single precision at compile time
        !             or change all the declarations and constants in the code from real(kind=dp) to single.
        !
        ! INPUT
        !   im (INTEGER)
        !   nx, nz (INTEGER)
        !   eps11, sig11, eps22, sig22 (REAL)
        !   dx, dz (REAL)
        !   npoints_pml (INTEGER) - the thickness of the pml
        !   rcx (INTEGER) - the x and y indices for an array of recievers
        !


        implicit none

        integer,parameter :: dp=kind(0.d0)

        ! total number of grid points in each direction of the grid
        integer :: nx, nz
        ! integer, dimension(:,:) :: rcx 

        ! thickness of the PML layer in grid points
        integer :: npoints_pml, nstep

        ! integer, dimension(nx,nz)
        real(kind=dp), dimension(nx,nz) :: eps11, eps13, eps33, &
                                        sig11, sig13, sig33, &
                                        epsilonx, epsilonz, &
                                        sigmax, sigmaz


        ! time step in seconds. decreasing the time step improves the pml attenuation
        ! but it should be inversely proportional to the center frequency of the 
        ! source frequency 
        real(kind=dp) :: DT, dx, dz 

        ! source
        integer,dimension(:) :: src
        real(kind=dp),dimension(nstep) :: srcx, srcz
        integer :: isource, jsource

        ! value of PI
        real(kind=dp), parameter :: PI = 3.141592653589793238462643d0

        ! speed of mother fuckin' light 
        real(kind=dp), parameter :: Clight = 2.9979458d+8

        ! permability and permittivity of free space 
        real(kind=dp), parameter :: mu0 = 4.0d0*pi*1.0d-7, eps0 = 8.85418782d-12

        ! typical relative permeability of common materials is close to unity but for
        ! the more specific case we can edit the following line to input permeability 
        ! as a 2D array 
        real(kind=dp), parameter :: mu = 1.d0

        ! E-field threshold above which we consider that the code became unstable
        real(kind=dp), parameter :: STABILITY_THRESHOLD = 1.d+25

        ! main arrays
        real(kind=dp), dimension(nx-1,nz) :: Ex
        real(kind=dp), dimension(nx,nz-1) :: Ez
        real(kind=dp), dimension(nx-1,nz-1) :: Hy

        ! we will compute the coefficients for the finite difference scheme 
        real(kind=dp), dimension(nx, nz) :: caEx, cbEx
        real(kind=dp), dimension(nx, nz) :: caEz, cbEz
        real(kind=dp) :: daHy, dbHy

        real(kind=dp) :: value_dEx_dz, value_dEz_dx, value_dHy_dz, value_dHy_dx

        ! arrays for the memory variables
        ! could declare these arrays in PML only to save a lot of memory, but proof of concept only here
        real(kind=dp), dimension(nx,nz) ::  memory_dEz_dx,  memory_dEx_dz 
        real(kind=dp), dimension(nx,nz) :: memory_dHy_dx
        real(kind=dp), dimension(nx,nz) ::  memory_dHy_dz

        ! parameters for the source
        ! angle of source force clockwise with respect to vertical (Y) axis
        ! character(len=6) :: src_type
        integer :: i,j, it

        real(kind=dp) :: velocnorm

        ! -------------------------------- PML parameters 
        ! 1D arrays for the damping profiles
        real(kind=dp), dimension(nx) :: K_x,alpha_x,a_x,b_x, &
                                        K_x_half, alpha_x_half,a_x_half,b_x_half
        real(kind=dp), dimension(nz) :: K_z,alpha_z,a_z,b_z, &
                                        K_z_half, alpha_z_half,a_z_half,b_z_half
                                        
        logical :: SINGLE
        logical, intent(in), optional :: OUTPUT_SINGLE 

        ! ------------------- Name the f2py inputs 
        !f2py3 intent(in) :: nx, nz, dx, dz,
        !f2py3 intent(in) :: noints_pml, src, nstep
        
        ! The default data output is single precision unless OUTPUT_SINGLE is 
        ! set to .FALSE.
        if (present(OUTPUT_SINGLE)) then 
            SINGLE = OUTPUT_SINGLE 
        else
            SINGLE = .TRUE.
        endif
        ! =============================================================================
        ! ----------------------- Load Permittivity Coefficients ----------------------
        call material_rw('eps11.dat', eps11, .TRUE.)
        call material_rw('eps13.dat', eps13, .TRUE.)
        call material_rw('eps33.dat', eps33, .TRUE.) ! We will change y to z soon
        call material_rw('sig11.dat', sig11, .TRUE.)
        call material_rw('sig13.dat', sig13, .TRUE.)
        call material_rw('sig33.dat', sig33, .TRUE.)

        ! ------------------------ Assign some constants -----------------------
        ! Assign the source location indices
        isource = int(src(1)) + npoints_pml
        jsource = int(src(2)) + npoints_pml

        ! Define the 
        DT = minval( (/dx, dz/) )/ ( 2.d0 * Clight/sqrt( minval( (/ eps11, eps33 /) ) ) ) 

        ! Compute the coefficients of the FD scheme. First scale the relative 
        ! permittivity and permeabilities to get the absolute values 
        epsilonx(:,:) = (eps11 + eps13)*eps0
        epsilonz(:,:) = (eps13 + eps33)*eps0
        sigmax(:,:) = sig11 + sig13 
        sigmaz(:,:) = sig13 + sig33 

        ! We need to change sigma to dsigma, same for epsilon

        caEx(:,:) = ( 1.0d0 - sigmax * dt / ( 2.0d0 * epsilonx ) ) / &
                    ( 1.0d0 + sigmax * dt / (2.0d0 * epsilonx ) )
        cbEx(:,:) = (dt / epsilonx ) / ( 1.0d0 + sigmax * dt / ( 2.0d0 * epsilonx ) )

        caEz(:,:) = ( 1.0d0 - sigmaz * dt / ( 2.0d0 * epsilonz ) ) / &
                    ( 1.0d0 + sigmaz * dt / (2.0d0 * epsilonz ) )
        cbEz(:,:) = (dt / epsilonz ) / ( 1.0d0 + sigmaz * dt / ( 2.0d0 * epsilonz ) )

        daHy = dt/(4.0d0*mu0*mu)
        dbHy = dt/mu0 !dt/(mu*mu*dx*(1+daHy) ) 
        daHy = 1.0d0 ! (1-daHy)/(1+daHy) ! 

        ! ================================ LOAD SOURCE ================================
        call loadsource('electromagneticsourcex.dat', nstep, srcx)
        call loadsource('electromagneticsourcez.dat', nstep, srcz)

        ! ----------------------------------------------------------------------

        ! Initialize CPML damping variables
        K_x(:) = 1.0d0
        K_x_half(:) = 1.0d0
        alpha_x(:) = 0.0d0
        alpha_x_half(:) = 0.0d0
        a_x(:) = 0.0d0
        a_x_half(:) = 0.0d0
        b_x(:) = 0.0d0 
        b_x_half(:) = 0.0d0 

        K_z(:) = 1.0d0
        K_z_half(:) = 1.0d0
        alpha_z(:) = 0.0d0
        alpha_z_half(:) = 0.0d0
        a_z(:) = 0.0d0
        a_z_half(:) = 0.0d0


        call loadcpml('kappax_cpml.dat', K_x)
        call loadcpml('alphax_cpml.dat', alpha_x)
        call loadcpml('acoefx_cpml.dat', a_x)
        call loadcpml('bcoefx_cpml.dat', b_x)

        call loadcpml('kappaz_cpml.dat', K_z)
        call loadcpml('alphaz_cpml.dat', alpha_z)
        call loadcpml('acoefz_cpml.dat', a_z)
        call loadcpml('bcoefz_cpml.dat', b_z)

        call loadcpml('kappax_half_cpml.dat', K_x_half)
        call loadcpml('alphax_half_cpml.dat', alpha_x_half)
        call loadcpml('acoefx_half_cpml.dat', a_x_half)
        call loadcpml('bcoefx_half_cpml.dat', b_x_half)

        call loadcpml('kappaz_half_cpml.dat', K_z_half)
        call loadcpml('alphaz_half_cpml.dat', alpha_z_half)
        call loadcpml('acoefz_half_cpml.dat', a_z_half)
        call loadcpml('bcoefz_half_cpml.dat', b_z_half)


        ! initialize arrays
        Ex(:,:) = 0.0d0
        Ez(:,:) = 0.0d0
        Hy(:,:) = 0.0d0

        ! PML
        memory_dEx_dz(:,:) = 0.0d0
        memory_dEz_dx(:,:) = 0.0d0

        memory_dHy_dx(:,:) = 0.0d0
        memory_dHy_dz(:,:) = 0.0d0

        !---
        !---  beginning of time loop
        !---

        do it = 1,NSTEP
        
            !--------------------------------------------------------
            ! compute magnetic field and update memory variables for C-PML
            !--------------------------------------------------------
            do i = 1,nx-1  
                do j = 1,nz-1
                
                    ! Values needed for the magnetic field updates
                    value_dEx_dz = ( Ex(i,j+1) - Ex(i,j) )/dz
                    memory_dEx_dz(i,j) = b_z(j) * memory_dEx_dz(i,j) + a_z(j) * value_dEx_dz
                    value_dEx_dz = value_dEx_dz/ K_z(j) + memory_dEx_dz(i,j)

                    ! The rest of the equation needed for agnetic field updates
                    value_dEz_dx = ( Ez(i+1,j) - Ez(i,j) )/dx
                    memory_dEz_dx(i,j) = b_x(i) * memory_dEz_dx(i,j) + a_x(i) * value_dEz_dx
                    value_dEz_dx = value_dEz_dx/ K_x(i) + memory_dEz_dx(i,j)

                    ! Now update the Magnetic field
                    Hy(i,j) = daHy*Hy(i,j) + dbHy*( value_dEz_dx + value_dEx_dz )

                enddo  
            enddo

            !--------------------------------------------------------
            ! compute electric field and update memory variables for C-PML
            !--------------------------------------------------------
            
            ! Compute the differences in the y-direction
            do j = 2,nz-1
                do i = 1,nx-1
                    ! Update the Ex field
                    value_dHy_dz = ( Hy(i,j) - Hy(i,j-1) )/dz ! this is nz-1 length vector
                    memory_dHy_dz(i,j) = b_z_half(j) * memory_dHy_dz(i,j) + a_z_half(j) * value_dHy_dz
                    value_dHy_dz = value_dHy_dz/K_z_half(j) + memory_dHy_dz(i,j)

                    Ex(i,j) = (( caEx(i,j) + caEx(i,j-1) )/2) * Ex(i,j) + &
                        (( cbEx(i,j) + cbEx(i,j-1) )/2 ) * value_dHy_dz
                enddo
            enddo

            do j = 1,nz-1
                do i = 2,nx-1
                    ! Update the Ez field
                    value_dHy_dx = ( Hy(i,j) - Hy(i-1,j) )/dx
                    memory_dHy_dx(i,j) = b_x_half(i) * memory_dHy_dx(i,j) + a_x_half(i) * value_dHy_dx
                    value_dHy_dx = value_dHy_dx/K_x_half(i) + memory_dHy_dx(i,j)
                    
                    Ez(i,j) = (( caEz(i,j) + caEz(i-1,j) )/2) * Ez(i,j) + &
                        (( cbEz(i,j) + cbEz(i-1,j) )/2) * value_dHy_dx 
                enddo
            enddo


            !----------------------------------------------------------------------------

            Ex(isource,jsource) = Ex(isource,jsource) + srcx(it) * DT / eps11(isource,jsource)
            Ez(isource,jsource) = Ez(isource,jsource) + srcz(it) * DT / eps33(isource,jsource) 
            
            ! Dirichlet conditions (rigid boundaries) on the edges or at the bottom of the PML layers
            Ex(1,:) = 0.d0
            Ex(nx-1,:) = 0.d0
            Ex(:,1) = 0.d0
            Ex(:,nz) = 0.d0

            Ez(1,:) = 0.d0
            Ez(nx,:) = 0.d0
            Ez(:,1) = 0.d0
            Ez(:,nz-1) = 0.d0

            Hy(1,:) = 0.d0
            Hy(nx-1,:) = 0.d0
            Hy(:,1) = 0.d0
            Hy(:,nz-1) = 0.d0

            ! print maximum of norm of velocity
            velocnorm = maxval(sqrt(Ex**2 + Ez**2))
            if (velocnorm > STABILITY_THRESHOLD) stop 'code became unstable and blew up'

            call write_image2(Ex, nx-1, nz, src, it, 'Ex', SINGLE)
            call write_image2(Ez, nx, nz-1, src, it, 'Ez', SINGLE)
        enddo
    end subroutine electromag2

    ! =========================================================================
    subroutine electromag2c(nx, nz, dx, dz, npoints_pml, src, nstep, OUTPUT_SINGLE)

        implicit none

        integer,parameter :: dp=kind(0.d0)

        ! total number of grid points in each direction of the grid
        integer :: nx, nz
        ! integer, dimension(:,:) :: rcx 

        ! thickness of the PML layer in grid points
        integer :: npoints_pml, nstep

        ! integer, dimension(nx,nz)
        complex(kind=dp), dimension(nx,nz) :: eps11, eps13, eps33, epsilonx, epsilonz
        real(kind=dp), dimension(nx,nz) :: sig11, sig13, sig33, sigmax, sigmaz

        ! time step in seconds. decreasing the time step improves the pml attenuation
        ! but it should be inversely proportional to the center frequency of the 
        ! source frequency 
        real(kind=dp) :: DT, dx, dz 

        ! source
        integer,dimension(:) :: src
        real(kind=dp),dimension(nstep) :: srcx, srcz
        integer :: isource, jsource

        ! value of PI
        real(kind=dp), parameter :: PI = 3.141592653589793238462643d0

        ! speed of mother fuckin' light 
        real(kind=dp), parameter :: Clight = 2.9979458d+8

        ! permability and permittivity of free space 
        real(kind=dp), parameter :: mu0 = 4.0d0*pi*1.0d-7, eps0 = 8.85418782d-12

        ! typical relative permeability of common materials is close to unity but for
        ! the more specific case we can edit the following line to input permeability 
        ! as a 2D array 
        real(kind=dp), parameter :: mu = 1.d0

        ! E-field threshold above which we consider that the code became unstable
        real(kind=dp), parameter :: STABILITY_THRESHOLD = 1.d+25

        ! main arrays
        complex(kind=dp), dimension(nx-1,nz) :: Ex
        complex(kind=dp), dimension(nx,nz-1) :: Ez
        complex(kind=dp), dimension(nx-1,nz-1) :: Hy

        ! we will compute the coefficients for the finite difference scheme 
        complex(kind=dp), dimension(nx, nz) :: caEx, cbEx
        complex(kind=dp), dimension(nx, nz) :: caEz, cbEz
        real(kind=dp) :: daHy, dbHy

        complex(kind=dp) :: value_dEx_dz, value_dEz_dx, value_dHy_dz, value_dHy_dx

        ! arrays for the memory variables
        ! could declare these arrays in PML only to save a lot of memory, but proof of concept only here
        complex(kind=dp), dimension(nx,nz) ::  memory_dEz_dx,  memory_dEx_dz 
        complex(kind=dp), dimension(nx,nz) :: memory_dHy_dx
        complex(kind=dp), dimension(nx,nz) ::  memory_dHy_dz

        ! character(len=6) :: src_type
        integer :: i,j, it

        real(kind=dp) :: velocnorm

        ! -------------------------------- PML parameters 
        ! 1D arrays for the damping profiles
        real(kind=dp), dimension(nx) :: K_x,alpha_x,a_x,b_x, &
                                        K_x_half, alpha_x_half,a_x_half,b_x_half
        real(kind=dp), dimension(nz) :: K_z,alpha_z,a_z,b_z, &
                                        K_z_half, alpha_z_half,a_z_half,b_z_half
                                        
        ! Boolean flag to save as double precision or single precision 
        logical :: SINGLE
        logical, intent(in), optional :: OUTPUT_SINGLE 

        ! ------------------- Name the f2py inputs 
        !f2py3 intent(in) :: nx, nz, dx, dz,
        !f2py3 intent(in) :: noints_pml, src, nstep

        ! =============================================================================
        ! The default data output is single precision unless OUTPUT_SINGLE is 
        ! set to .FALSE.
        if (present(OUTPUT_SINGLE)) then 
            SINGLE = OUTPUT_SINGLE 
        else
            SINGLE = .TRUE.
        endif

        ! ----------------------- Load Permittivity Coefficients ----------------------

        call material_rwc('eps11.dat', eps11, .TRUE.)
        call material_rwc('eps13.dat', eps13, .TRUE.)
        call material_rwc('eps33.dat', eps33, .TRUE.) ! We will change y to z soon
        call material_rw('sig11.dat', sig11, .TRUE.)
        call material_rw('sig13.dat', sig13, .TRUE.)
        call material_rw('sig33.dat', sig33, .TRUE.)

        ! ------------------------ Assign some constants -----------------------

        ! Assign the source location indices
        isource = int(src(1)) + npoints_pml
        jsource = int(src(2)) + npoints_pml

        ! Define the 
        DT = minval( (/dx, dz/) )/ ( 2.d0 * Clight/sqrt( minval( (/ REAL(eps11), REAL(eps33) /) ) ) ) 

        ! Compute the coefficients of the FD scheme. First scale the relative 
        ! permittivity and permeabilities to get the absolute values 
        epsilonx(:,:) = (eps11 + eps13)*eps0
        epsilonz(:,:) = (eps13 + eps33)*eps0
        sigmax(:,:) = sig11 + sig13 
        sigmaz(:,:) = sig13 + sig33

        ! We need to change sigma to dsigma, same for epsilon

        caEx(:,:) = ( 1.0d0 - sigmax * dt / ( 2.0d0 * epsilonx ) ) / &
                    ( 1.0d0 + sigmax * dt / (2.0d0 * epsilonx ) )
        cbEx(:,:) = (dt / epsilonx ) / ( 1.0d0 + sigmax * dt / ( 2.0d0 * epsilonx ) )

        caEz(:,:) = ( 1.0d0 - sigmaz * dt / ( 2.0d0 * epsilonz ) ) / &
                    ( 1.0d0 + sigmaz * dt / (2.0d0 * epsilonz ) )
        cbEz(:,:) = (dt / epsilonz ) / ( 1.0d0 + sigmaz * dt / ( 2.0d0 * epsilonz ) )

        daHy = dt/(4.0d0*mu0*mu)
        dbHy = dt/mu0 !dt/(mu*mu*dx*(1+daHy) ) 
        daHy = 1.0d0 ! (1-daHy)/(1+daHy) ! 


        ! ----------------------------------------------------------------------

        ! ================================ LOAD SOURCE ================================

        call loadsource('electromagneticsourcex.dat', nstep, srcx)
        call loadsource('electromagneticsourcez.dat', nstep, srcz)



        ! ----------------------------------------------------------------------

        ! Initialize CPML damping variables
        K_x(:) = 1.0d0
        K_x_half(:) = 1.0d0
        alpha_x(:) = 0.0d0
        alpha_x_half(:) = 0.0d0
        a_x(:) = 0.0d0
        a_x_half(:) = 0.0d0
        b_x(:) = 0.0d0 
        b_x_half(:) = 0.0d0 

        K_z(:) = 1.0d0
        K_z_half(:) = 1.0d0
        alpha_z(:) = 0.0d0
        alpha_z_half(:) = 0.0d0
        a_z(:) = 0.0d0
        a_z_half(:) = 0.0d0


        call loadcpml('kappax_cpml.dat', K_x)
        call loadcpml('alphax_cpml.dat', alpha_x)
        call loadcpml('acoefx_cpml.dat', a_x)
        call loadcpml('bcoefx_cpml.dat', b_x)

        call loadcpml('kappaz_cpml.dat', K_z)
        call loadcpml('alphaz_cpml.dat', alpha_z)
        call loadcpml('acoefz_cpml.dat', a_z)
        call loadcpml('bcoefz_cpml.dat', b_z)

        call loadcpml('kappax_half_cpml.dat', K_x_half)
        call loadcpml('alphax_half_cpml.dat', alpha_x_half)
        call loadcpml('acoefx_half_cpml.dat', a_x_half)
        call loadcpml('bcoefx_half_cpml.dat', b_x_half)

        call loadcpml('kappaz_half_cpml.dat', K_z_half)
        call loadcpml('alphaz_half_cpml.dat', alpha_z_half)
        call loadcpml('acoefz_half_cpml.dat', a_z_half)
        call loadcpml('bcoefz_half_cpml.dat', b_z_half)


        ! initialize arrays
        Ex(:,:) = complex(0.d0, 0.0d0)
        Ez(:,:) = complex(0.d0, 0.0d0)
        Hy(:,:) = complex(0.d0, 0.0d0)

        ! PML
        memory_dEx_dz(:,:) = complex(0.d0, 0.0d0)
        memory_dEz_dx(:,:) = complex(0.d0, 0.0d0)

        memory_dHy_dx(:,:) = complex(0.d0, 0.0d0)
        memory_dHy_dz(:,:) = complex(0.d0, 0.0d0)

        !---
        !---  beginning of time loop
        !---

        do it = 1,NSTEP
        
        !--------------------------------------------------------
        ! compute magnetic field and update memory variables for C-PML
        !--------------------------------------------------------
        do i = 1,nx-1  
            do j = 1,nz-1
            
            ! Values needed for the magnetic field updates
            value_dEx_dz = ( Ex(i,j+1) - Ex(i,j) )/dz
            memory_dEx_dz(i,j) = b_z(j) * memory_dEx_dz(i,j) + a_z(j) * value_dEx_dz
            value_dEx_dz = value_dEx_dz/ K_z(j) + memory_dEx_dz(i,j)

            ! The rest of the equation needed for agnetic field updates
            value_dEz_dx = ( Ez(i+1,j) - Ez(i,j) )/dx
            memory_dEz_dx(i,j) = b_x(i) * memory_dEz_dx(i,j) + a_x(i) * value_dEz_dx
            value_dEz_dx = value_dEz_dx/ K_x(i) + memory_dEz_dx(i,j)

            ! Now update the Magnetic field
            Hy(i,j) = daHy*Hy(i,j) + dbHy*( value_dEz_dx + value_dEx_dz )

            enddo  
        enddo

        !--------------------------------------------------------
        ! compute electric field and update memory variables for C-PML
        !--------------------------------------------------------
        
        ! Compute the differences in the y-direction
        do j = 2,nz-1
            do i = 1,nx-1
            ! Update the Ex field
            value_dHy_dz = ( Hy(i,j) - Hy(i,j-1) )/dz ! this is nz-1 length vector
            memory_dHy_dz(i,j) = b_z_half(j) * memory_dHy_dz(i,j) + a_z_half(j) * value_dHy_dz
            value_dHy_dz = value_dHy_dz/K_z_half(j) + memory_dHy_dz(i,j)

            Ex(i,j) = (( caEx(i,j) + caEx(i,j-1) )/2) * Ex(i,j) + &
                (( cbEx(i,j) + cbEx(i,j-1) )/2 ) * value_dHy_dz
            enddo
        enddo

        do j = 1,nz-1
            do i = 2,nx-1
            ! Update the Ez field
            value_dHy_dx = ( Hy(i,j) - Hy(i-1,j) )/dx
            memory_dHy_dx(i,j) = b_x_half(i) * memory_dHy_dx(i,j) + a_x_half(i) * value_dHy_dx
            value_dHy_dx = value_dHy_dx/K_x_half(i) + memory_dHy_dx(i,j)
            
            Ez(i,j) = (( caEz(i,j) + caEz(i-1,j) )/2) * Ez(i,j) + &
                (( cbEz(i,j) + cbEz(i-1,j) )/2) * value_dHy_dx 
            enddo
        enddo


        !----------------------------------------------------------------------------

        Ex(isource,jsource) = Ex(isource,jsource) + srcx(it) * DT / eps11(isource,jsource)
        Ez(isource,jsource) = Ez(isource,jsource) + srcz(it) * DT / eps33(isource,jsource) 
        
        ! Dirichlet conditions (rigid boundaries) on the edges or at the bottom of the PML layers
        Ex(1,:) = 0.d0
        Ex(nx-1,:) = 0.d0
        Ex(:,1) = 0.d0
        Ex(:,nz) = 0.d0

        Ez(1,:) = 0.d0
        Ez(nx,:) = 0.d0
        Ez(:,1) = 0.d0
        Ez(:,nz-1) = 0.d0

        Hy(1,:) = 0.d0
        Hy(nx-1,:) = 0.d0
        Hy(:,1) = 0.d0
        Hy(:,nz-1) = 0.d0

        ! print maximum of norm of velocity
        velocnorm = maxval(abs(sqrt(Ex**2 + Ez**2)))
        if (velocnorm > STABILITY_THRESHOLD) stop 'code became unstable and blew up'

        call write_image2c(Ex, nx-1, nz, src, it, 'Ex', SINGLE)
        call write_image2c(Ez, nx, nz-1, src, it, 'Ez', SINGLE)

        enddo   ! end of time loop


    end subroutine electromag2c
    
end module cpmlfdtd