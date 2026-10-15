# Shulker small task: printable fragments

Source repository: /local_data/yz11445/projects/Assembly_Sim
- tasks/stack_sawtooth_shulker_small/geometry.py defines the two voxel shapes.
- tasks/stack_sawtooth_shulker_small/config.py sets DEFAULT_UNIT_SIZE = 0.027 meters.
- tasks/stack_sawtooth_shulker_small/assets.py builds the simulated USD cubes procedurally.

## Files to print

- FragmentA_clearance_0p4mm.stl: blue, solid base with five raised posts.
- FragmentB_clearance_0p4mm.stl: green, solid base with four raised posts.

Import STL coordinates as millimeters, at 100% scale. Each part measures
81 x 81 x 54 mm; assembled height is 81 mm. STL does not store colors or units.
Both files have their full 81 x 81 mm base on Z=0, posts upward. B is rotated
180 degrees around X relative to its simulation orientation. Flip one part
for assembly so its posts point toward the other part's base.

The clearance variant insets every raised post by 0.2 mm on each X/Y side,
without changing the base, post heights, or overall bounding dimensions.
This produces a nominal 0.4 mm lateral gap between opposing adjacent posts.
Fit has not been physically tested and depends on printer/material accuracy.
No G-code is included: slice with your printer and material profile.

## Exact reference files

FragmentA_nominal.stl and FragmentB_nominal.stl preserve the nominal voxel
geometry. Each has four nonmanifold edges where diagonal posts meet only
along an edge. These are reference exports; use the clearance versions
for printing.

## Validation

verify_stl.py reads the actual binary STL files, checks dimensions, positive
volume, winding, connectivity and edge incidence, and writes validation.json.
Both clearance meshes have one connected component, consistent winding,
and exactly two triangles incident to every edge (zero nonmanifold edges).
They have not been checked in a slicer or physically printed.

Regenerate with Python 3: python3 export_fragments.py
Validate with Python 3: python3 verify_stl.py
No extra Python packages or GPUs are needed.
