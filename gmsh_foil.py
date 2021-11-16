from airfoils import Airfoil
import numpy as np
import gmsh

class GMSHFoil:
    def __init__(self, foil_name = '4812', mesh_name = 'NACA_4812'):
        """
        A thin wrapper class that creates a 2D airfoil mesh and sets
        names for the surfaces of the boundaries.
        """
        self.foil_name = foil_name
        self.foil = Airfoil.NACA4(self.foil_name)
        self.mesh_name = mesh_name 
        self.gmsh = gmsh
        
    def create_2d_unstructured_foil_mesh(self,
                                         npoints_disc_foil = 150,
                                         npoints_boundary = 20, 
                                         h_f = 0.001,
                                         h_0 = 0.01,
                                         L_x = 10,
                                         L_y = None, 
                                         phi_angle = 0.):
        """
        Create the 2D unstructured mesh for simulating the airfoil.
        
        Arguments:
          npoints_disc_foil : (150) number of points for each of the surfaces of the airfoil
          npoints_boundary  : (10) the number of points for the discretization of the outer boundary.
          h_f               : (0.001) h-refinement size for the points of the foil
          h_0               : (0.01)  h-refinement size for the points of the outer boundary
          L_x, L_y          : the length of the outer boundary.
          phi_angle         : "angle of attack" (just rotating the foil) in radians
          
        """
        
        _gmsh = self.gmsh
        _gmsh.initialize()
        _gmsh.model.add(self.mesh_name)

        if L_y is None:
            L_y = L_x

        # For the boundary:
        lines_top    = np.array( [ (x,y) for x, y in zip(np.linspace(-L_x/2, L_x/2, npoints_boundary) , [L_y/2]*npoints_boundary )])
        lines_bottom = np.flip(lines_top,0) - [0,L_y]

        lines_right  = np.array( [ (x,y) for x, y in zip([L_x/2]*npoints_boundary , np.linspace(L_y/2, -L_y/2, npoints_boundary) )])
        lines_left   = np.flip(lines_right,0) - [L_x, 0]
        
        #I'm doing some book-keeping to create the boundary groups easier:
        
        all_lines_list = [lines_left, lines_top, lines_right, lines_bottom]
        _blc           = np.array([l.shape[0] for l in all_lines_list])
        all_lines      = np.vstack(all_lines_list)

        # for the foil-hole:
        x_points = np.linspace(0,1,npoints_disc_foil)
        x_points_reversed = list(reversed(x_points))
        foil_points_x = np.array([*x_points, *x_points_reversed])
        foil_points_y = np.array([*self.foil.y_lower(x_points), *self.foil.y_upper(x_points_reversed)])
        foil_p = [(x,y) for x,y in zip(foil_points_x, foil_points_y)]
        
        c = np.cos(phi_angle)
        s = np.sin(phi_angle)
        R = np.array([[c,-s],[s,c]])
        foil_p = np.array(foil_p) @ R
        
        gmsh_airf_points = [_gmsh.model.geo.addPoint(x,y,0,h_f, k) for k, (x,y) in enumerate(foil_p)]
        n_airf_points = len(gmsh_airf_points)

        points_outer_xy = all_lines

        gmsh_outer_points  = [_gmsh.model.geo.addPoint(px, py,0., k+n_airf_points+1) for k, (px, py) in enumerate(points_outer_xy)]

        foil_curve = [];
        start_end_lines_foil = [];
        
        for k in range(n_airf_points):
            k_start, k_end = k, k + 1
            if k_end > max(gmsh_airf_points):
                k_end = min(gmsh_airf_points)

            gmsh.model.geo.addLine(k_start, k_end, k)
            start_end_lines_foil.append((k_start, k_end))
            foil_curve.append(k)
        
        n_lines_foil = n_airf_points+1
        bound_curve = [];
        start_end_lines_boundary = [];
        
        # Adding the external lines:
        for k in gmsh_outer_points:

            k_start, k_end = k , k +1

            if k_end>max(gmsh_outer_points):
                k_end = min(gmsh_outer_points)

            _gmsh.model.geo.addLine(k_start, k_end, k + n_lines_foil)
            start_end_lines_boundary.append((k_start, k_end))
            bound_curve.append(k + n_lines_foil)


        #Creating a square unstructured mesh with a 
        # foil-shaped hole:
        _gmsh.model.geo.addCurveLoop(bound_curve,1)
        _gmsh.model.geo.addCurveLoop(foil_curve,2)
        _gmsh.model.geo.addPlaneSurface([1,2], 0)
        
        
        _blcs = np.cumsum(_blc)
        
        # Definition of physical groups:
        foil_surf_group       = _gmsh.model.addPhysicalGroup(1,[*foil_curve],123)
        left_boundary_group   = _gmsh.model.addPhysicalGroup(1,bound_curve[0:_blcs[0]],1)
        top_boundary_group    = _gmsh.model.addPhysicalGroup(1,bound_curve[_blcs[0]:_blcs[1]],2)
        right_boundary_group  = _gmsh.model.addPhysicalGroup(1,bound_curve[_blcs[1]:_blcs[2]],3)
        bottom_boundary_group = _gmsh.model.addPhysicalGroup(1,bound_curve[_blcs[2]:],4)
        
        _gmsh.model.setPhysicalName(1, foil_surf_group, 'foil_surf')
        _gmsh.model.setPhysicalName(1, left_boundary_group,'left_boundary' )
        _gmsh.model.setPhysicalName(1, right_boundary_group, 'right_boundary')
        _gmsh.model.setPhysicalName(1, top_boundary_group, 'top_boundary')
        _gmsh.model.setPhysicalName(1, bottom_boundary_group, 'bottom_boundary')
        
        _gmsh.model.geo.synchronize()
        _gmsh.model.mesh.generate(2)
        
        _gmsh.write("%s.msh"%self.mesh_name)
        
    def view(self):
        self.gmsh.fltk.run()
