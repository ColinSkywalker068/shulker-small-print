# Shulker fragments at original simulation size

These full-size models replace the earlier 81 mm small-task exports.
The repository retains its original name, `shulker-small-print`.

Source: tasks/stack_sawtooth_shulker/geometry.py and config.py in
/local_data/yz11445/projects/Assembly_Sim.
DEFAULT_UNIT_SIZE = 0.08 meters = 80 mm.

Each fragment measures 240 x 240 x 160 mm. Together they form a
240 x 240 x 240 mm cube. Import STL as millimeters at 100% scale.
Both parts have their full base flat on Z=0. Fragment B is inverted
relative to its simulation pose; flip one part for assembly.

- FragmentA_nominal.stl and FragmentB_nominal.stl reproduce the nominal
  simulation visual geometry. Zero fit clearance; each retains four
  nonmanifold edges at diagonal post contacts. A slicer may need to repair
  these exact reference meshes.
- FragmentA_clearance_0p4mm.stl and FragmentB_clearance_0p4mm.stl inset
  each raised post by 0.2 mm on every X/Y side, creating a 0.4 mm lateral
  gap between neighboring mating posts. This uses the same absolute gap
  as the small print version, not a scaled-up gap. Base and heights remain
  unchanged. Both clearance meshes passed edge, winding, connectivity,
  dimensions, and volume checks with zero nonmanifold edges.

The printing clearance is independent of the simulation's 2 mm collider
clearance. Nominal STL files follow the visible 80 mm voxels, not the smaller
simulation collision cubes.

No slicer or physical fit tests have been performed. No G-code is included.
Build volume must accommodate 240 x 240 x 160 mm per fragment.

Regenerate using Python 3 (no additional packages):

```bash
python3 export_fragments.py
python3 verify_stl.py
```

The exporter reads the source geometry from the repository path above.
Validation reads the STL artifacts and writes validation.json.
