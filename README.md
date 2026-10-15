# Small Shulker fragments for 3D printing

These models match the **small Shulker simulation task**
(`stack_sawtooth_shulker_small`), which uses 27 mm voxels.
The earlier 240 mm full-size exports have been replaced with the small-task
models. Download the files currently on `main` for the dimensions below.

## Actual size

| Feature | Millimeters | Centimeters |
|---|---|---|
| One voxel / nominal raised-post width | 27 mm | 2.7 cm |
| Each fragment, X × Y × Z | 81 × 81 × 54 mm | 8.1 × 8.1 × 5.4 cm |
| Assembled cube | 81 × 81 × 81 mm | 8.1 × 8.1 × 8.1 cm |

**81 mm is 8.1 cm, not 8 mm.** Import STL coordinates as **millimeters at
100% scale**. STL files do not store units or colors.

The small simulation's grasp code selects a 27 mm central-post grasp for
blue when it is the base, or an 81 mm full-width grasp for other cases.
Its command accounts for the simulation's 2 mm collider clearance, using
25 mm or 79 mm before its additional squeeze adjustment. This explains why
the width being grasped can differ from the fragment's overall width.
Physical grasp performance with printed parts has not been tested.

## Models

| File | Fragment | Geometry |
|---|---|---|
| FragmentA_nominal.stl | Blue: base and five raised posts | Exact nominal simulation visual shape |
| FragmentB_nominal.stl | Green: base and four raised posts | Exact nominal simulation visual shape |
| FragmentA_clearance_0p4mm.stl | Blue | Posts inset for printing |
| FragmentB_clearance_0p4mm.stl | Green | Posts inset for printing |

Both versions have the same **81 × 81 × 54 mm** overall dimensions.

### Nominal versus clearance

The nominal files preserve 27 mm posts and zero mating clearance. Each has
four nonmanifold edges where diagonal posts touch along an edge, which may
require slicer repair. They are exact reference exports.

For printing, use the clearance files. Each raised post is inset **0.2 mm
on each X/Y side**, reducing its width from **27 mm to 26.6 mm**. Opposing
neighboring posts therefore have a **0.4 mm lateral mating gap**. The base,
post heights, and overall bounding dimensions are unchanged.

The 0.4 mm printing gap is separate from the simulation's 2 mm collider
clearance. Neither STL variant reproduces the simulation collision cubes;
the nominal version follows the visible voxel geometry.

## Printing and assembly

Both files have their full 81 × 81 mm base on Z=0, with posts upward.
Fragment B is rotated 180 degrees around X relative to its simulation
orientation. Flip one part for assembly so the posts face the other base.

Slice using your printer and material profile. No G-code is included.
Fit depends on printer and material accuracy; the files have not been
checked in a slicer or physically printed.

## Verification

`verify_stl.py` reloads the binary STL files and checks dimensions, positive
volume, winding, connectivity, and edge incidence. Results are recorded in
`validation.json`.

Both clearance meshes have one connected component, consistent winding,
and zero nonmanifold edges. Nominal meshes retain the four edge contacts
described above.

## Source and regeneration

Source repository on the originating workstation:
`/local_data/yz11445/projects/Assembly_Sim`

- `tasks/stack_sawtooth_shulker_small/geometry.py`: voxel assignments.
- `tasks/stack_sawtooth_shulker_small/config.py`: `DEFAULT_UNIT_SIZE = 0.027` meters.
- `tasks/stack_sawtooth_shulker_small/assets.py`: procedural simulation geometry.
- `tasks/stack_sawtooth_shulker_small/scripted.py`: grasp selection and width commands.

Regeneration requires that source repository at the path configured in
`export_fragments.py`. Validation only requires the STL files alongside the
validation script. Both scripts use Python 3 with no extra packages or GPUs:

```bash
python3 export_fragments.py
python3 verify_stl.py
```
