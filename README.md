# `GMSHFoil`
A simple class to create a 2D mesh for an airfoil in GMSH using python.

## Requirements

```
pip install airfoils
pip install gmsh==4.8.0
pip install numpy
```

## Usage

Script to create a mesh with a NACA airfoil and a particular angle of attack:

```
python3 gmsh_foil_run.py --foil-number-string 4812 \
  --angle-of-attack 0.\
  --output-mesh-file-name 'NACA_4812'\
  --view 0

```

## Results:
![Alt text](figs/gmsh_foil1.png)

