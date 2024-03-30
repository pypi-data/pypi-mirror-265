#!/usr/bin/env python

import os


def run_example_1(log='Ex1.log'):
    # Example 1: create supercell and slab
    Note = "\nExample 1 shows how to create a supercell of diamond-Si and build slabs"

    print (Note)
    os.chdir('example1')
    # To create a convention cell, use the command
    cmd = "pysc --task=redefine --sc1=-1,1,1 --sc2=1,-1,1 --sc3=1,1,-1 > {} 2>&1".format(log)
    os.system(cmd)

    # You can check the generated POSCAR_redefine file 
    # To create a slab structure, run
    cmd = "pysc --task=slab --hkl=111 --thickness=3 --vacuum=20 >> {} 2>&1".format(log)
    os.system(cmd)

    # To query the bond length between two atoms
    cmd_1 = "pysc --task=bond --atom_index=0,1 --poscar=POSCAR_slab >> {} 2>&1".format(log)
    cmd_2 = "pysc --task=crystal_info --poscar=POSCAR_slab >> {} 2>&1".format(log)
    os.system(cmd_1)
    os.system(cmd_2)

    # To write structure information for QE pw.x (under testing)
    cmd = "v2qe > {}".format(log)
    os.system(cmd)
    os.chdir('..')


def run_example_2(log='Ex2.log'):
    Note = "\nExample 2 demonstrates how to build nanotubes with specified chiral number"
    print (Note)
    os.chdir('example2')
    cmd = "pysc --task=tube --chiral_num=4,6 > {}".format(log)
    os.system(cmd)
    os.chdir('..')


def run_example_3(log='Ex3.log'):
    Note = "\nExample 3 demonstrate how to redefine the lattice by a transformation matrix"
    print (Note)
    os.chdir('example3')
    cmd = "pysc --task=redefine --cell_orientation=1 --sc1=10,0,0 --sc2=0,6,0 --sc3=0,0,1 > {}".format(log)
    os.system(cmd)
    # Then run the command to create the dislocated structure
    cmd = "pysc --task=screw_dislocation --burgers_vector=0,0,1 --poscar=POSCAR_redefine --screw_idir=2 --display_structure=F >> {}".format(log)
    os.system(cmd)
    os.chdir('..')


def run_example_4(log='Ex4.log'):
    Note = "\nExample 4 demonstrates how to build a bending sheet from a flat one"
    print (Note)
    os.chdir('example4')
    cmd = "pysc --task=bending --nn=8 --idir_per=1 --idir_bend=2 > {}".format(log)
    os.system(cmd)
    cmd = "pysc --task=cmp --poscar1=POSCAR_flat --poscar2=POSCAR_bending >> {}".format(log)
    os.system(cmd)
    os.chdir('..')


def run_example_5(log='Ex5.log'):
    Note = "\nExample 5 demonstrate how to build a superlattice based on two two-dimensional materials"
    print (Note)
    os.chdir('example5')
    cmd = "make_superlatt --tolerance=0.1 --maxarea=100 > {}".format(log)
    os.system(cmd)
    os.chdir('..')


def run_example_6(log='Ex6.log'):
    Note = "\nExample 6 demonstrates how to run v2qe to convert POSCAR into a QE input (pwscf)"
    print (Note)
    os.chdir('example6')
    cmd = "v2qe > {}".format(log)
    os.system(cmd)
    os.chdir('..')
 

def run_example_7(log='Ex7.log'):
    Note = "\nExample 7 demonstrates usage of interpolating structures"
    print (Note)



 
if __name__=='__main__':
    run_example_1()
    run_example_2()
    run_example_3()
    run_example_4()
    run_example_5()
    run_example_6()
    run_example_7()
