#!/usr/bin/env python

from pysupercell.pysupercell import *

def get_twin_structures(poscar1,poscar2,verbosity=1):
    import operator
    if verbosity:
        print ('Please make sure that all atoms are ordered in the same sequence!')
        print ('Structure 1 from file {}'.format(poscar1))
        print ('Structure 2 from file {}'.format(poscar2))
    assert os.path.isfile(poscar1),'cannot find {}'.format(poscar1)
    assert os.path.isfile(poscar2),'cannot find {}'.format(poscar2)
    struct_1=cryst_struct.load_poscar(poscar1)
    struct_2=cryst_struct.load_poscar(poscar2)
    assert np.prod(operator.eq(struct_1._species,struct_2._species)), 'Twin-structure error: species inconsistent!'
    assert np.prod(operator.eq(struct_1._counts,struct_2._counts)), 'Twin-structure error: No. of atoms inconsistent!'
    assert struct_1._natom==struct_2._natom,'Twin-structure error numbers of atoms inconsistent'
    return struct_1, struct_2


def sort_structs_atoms(poscar1,poscar2,ncell=1,boundary_condition=[1,1,0]):
    def bond_length(pos1,pos2,cell,cell_idx=True,ncell=1,boundary_condition=[1,1,1]):
        Rvecs = gen_Rvecs(ncell,boundary_condition)
        dists = np.linalg.norm( np.dot(pos1 - pos2 + Rvecs, cell), axis=-1)
        bond = np.min(dists)
        if cell_idx: return bond,np.where(dists==bond)[0][0]
        return bond

    print ('\nSort atoms in {} accordingly to {}'.format(poscar2,poscar1))
    struct_1, struct_2 = get_twin_structures(poscar1,poscar2)
    pos_to_sort = copy.deepcopy(struct_2._pos) 
    sort_idx = np.zeros(struct_2._natom,int)
    sort_iR = np.zeros(struct_2._natom,int)
    for iat in range(struct_2._natom):
        current_bond=100
        for jat in range(struct_1._natom):
            bond,iR = bond_length(struct_1._pos[jat], struct_2._pos[iat] ,struct_2._cell, 
            boundary_condition = boundary_condition)
            if bond < current_bond: 
                current_bond = bond
                sort_idx[iat]=jat
                sort_iR[iat] = iR
    Rvecs = gen_Rvecs(ncell,boundary_condition=[1,1,0])
    struct_2._pos = pos_to_sort[sort_idx] 
    struct_2._pos -= Rvecs[sort_iR]
    struct_2._pos_cart = np.dot(struct_2._pos, struct_2._cell)
    filposcar = '{}_sorted'.format(poscar2)
    struct_2.write_poscar_head(filename=filposcar)
    struct_2.write_poscar_atoms(filename=filposcar,mode='a')
    print ('Done. Please check the structures in {} and {} carefully'.format(poscar1,filposcar))
    return struct_1,struct_2
 


def compare_structs(poscar1,poscar2):
    print ('\nComparing two crystal structures\n')
    struct_1, struct_2 = get_twin_structures(poscar1,poscar2)

    nat = struct_1._natom
    diff=np.zeros(nat)
    print ('\n{}'.format('='*60))
    print (('{:4s} '*3+'{:>8s} '*4).format('idx','st1','st2','dist (Ang)','dx','dy','dz'))
    print ('-'*60)
    Rvecs = gen_Rvecs()
    for iat in range(nat):
        images = np.dot(struct_2._pos[iat]+Rvecs,struct_2._cell)
        norms = np.linalg.norm(struct_1._pos_cart[iat]-images,axis=1)
        diff[iat]=np.min(norms)
        idx = np.where(norms==np.min(norms))[0][0]
        print (' {:<4d} {:4s} {:4s} '.format(iat+1,struct_1._symbols[iat],struct_2._symbols[iat]),end=' ')
        print (('{:8.4f} '*4).format(diff[iat],*tuple(struct_1._pos_cart[iat] - images[idx])))
    print ('{0}'.format('='*60))
    print ('{0:14s}'.format('Total dist : ')+'   {:8.4f}'.format(np.sum(diff)))
    print ('{0:14s}'.format('Max   dist : ')+'   {:8.4f}\n'.format(np.max(diff)))
    return diff


def interpolate_structs(poscar1,poscar2,nimages=5,n_extrapolate=0,outdir='interpolated_images',f_archive='XDATCAR',sort_atoms=True):
    import shutil
    if sort_atoms:
        struct_1, struct_2 = sort_structs_atoms(poscar1,poscar2)
        poscar2 = '{}_sorted'.format(poscar2)
    print ('\nInterpolating images between two crystal structures')
    struct_1, struct_2 = get_twin_structures(poscar1,poscar2)
    if os.path.isdir(outdir): shutil.rmtree(outdir)
    assert nimages>=1, 'Number of images should not be less than 1!'
    diff_cell = (struct_2._cell - struct_1._cell)/(nimages+1)
    diff_pos_cart  = (struct_2._pos_cart - struct_1._pos_cart)/(nimages+1)
    os.mkdir(outdir)
    st_images = []

    st_arch = copy.deepcopy(struct_1)
    st_arch._system = 'All images'
    st_arch.write_poscar_head(filename=f_archive)
    with open(f_archive,'a') as fw: 
        fw.write(' '.join(['{:4s}'.format(item) for item in st_arch._species])+'\n')
        fw.write(' '.join(['{:4d}'.format(item) for item in st_arch._counts])+'\n')
 
    if n_extrapolate==0:
        for im in range(nimages+2):
            st_im = copy.deepcopy(struct_1)
            st_im._system = 'Image {}'.format(im)
            st_im._cell += diff_cell*(im)
            st_im._pos_cart += diff_pos_cart*(im)
            st_im._pos = np.dot(st_im._pos_cart, np.linalg.inv(st_im._cell))
            filpos = '{}/POSCAR_im_{}'.format(outdir,im)
            st_im.write_poscar_head(filename=filpos)
            st_im.write_poscar_atoms(filename=filpos,mode='a')
            st_images.append(st_im)
            with open(f_archive,'a') as fw: 
                fw.write('Direct configuration = {}\n'.format(im))
                for pos in st_im._pos: fw.write(('{:22.15f} '*3+'\n').format(*tuple(pos)))

    else:
        nimages_tot = n_extrapolate*2 + nimages + 2
        print ('{} extrapolated images included as required'.format(2*n_extrapolate))
        for imm in range(nimages_tot):
            im = imm - n_extrapolate
            st_im = copy.deepcopy(struct_1)
            st_im._system = 'Image {}'.format(im)
            st_im._cell += diff_cell*(im)
            st_im._pos_cart += diff_pos_cart*(im)
            st_im._pos = np.dot(st_im._pos_cart, np.linalg.inv(st_im._cell))
            filpos = '{}/POSCAR_im_{}'.format(outdir,im)
            st_im.write_poscar_head(filename=filpos)
            st_im.write_poscar_atoms(filename=filpos,mode='a')
            st_images.append(st_im)
            with open(f_archive,'a') as fw: 
                fw.write('Direct configuration = {}\n'.format(im))
                for pos in st_im._pos: fw.write(('{:22.15f} '*3+'\n').format(*tuple(pos)))
 
    print ('\n{} images written to {}'.format(len(st_images),outdir))
    print ('You can also check the XDATCAR file for an archive of images')
    return st_images



