#!/bin/bash
# Script to create a mesh and an open foam case folder for the analysis of a foil

CASE_NAME=$1
GMSH_OUT_FILE=${CASE_NAME}_mesh #without the .msh ending!
python3 gmsh_foil_run.py --foil-number-string 4812 \
  --angle-of-attack 0 \
  --output-mesh-file-name $GMSH_OUT_FILE

mkdir $CASE_NAME
echo "dbg"
echo $CASE_NAME
mkdir ${CASE_NAME}/0
echo ${CASE_NAME}/0
mkdir ${CASE_NAME}/constant
mkdir ${CASE_NAME}/system
cp ${GMSH_OUT_FILE}.msh ${CASE_NAME}/${GMSH_OUT_FILE}.msh

cp $FOAM_TUTORIALS/incompressible/simpleFoam/airFoil2D/0/* ${CASE_NAME}/0
cp $FOAM_TUTORIALS/incompressible/simpleFoam/airFoil2D/constant/* ${CASE_NAME}/constant
cp $FOAM_TUTORIALS/incompressible/simpleFoam/airFoil2D/system/* ${CASE_NAME}/system



