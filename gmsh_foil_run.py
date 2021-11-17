from gmsh_foil import GMSHFoil
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--foil-number-string', '-f', help="the foil number", type= str, default = '4812')
parser.add_argument('--angle-of-attack', '-a', help="angle of attack in radians", type= float, default= 0.)
parser.add_argument('--output-mesh-file-name', '-o',help='the file name of the mesh output (without the .msh suffix)', type = str, default = 'mesh_out')
parser.add_argument('--view','-v',help='view the mesh after creating it',type=bool)

def _gf_mesh_run(foil_number_string, angle_of_attack, output_mesh_file, view):
    g = GMSHFoil(foil_name = foil_number_string, mesh_name=output_mesh_file)
    g.create_2d_unstructured_foil_mesh()
    if view:
        g.view()


if __name__ == '__main__':
    args = parser.parse_args()

    if len(sys.argv):
        parser.print_help()
        return 0
    
    _gf_mesh_run(args.foil_number_string,
            args.angle_of_attack, 
            args.output_mesh_file_name, 
            args.view)
