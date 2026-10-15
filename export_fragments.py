"""Export task voxel geometry to millimeter STL, without simulator dependencies."""
import importlib.util
import json
import struct
from collections import Counter
from pathlib import Path

ROOT = Path('/local_data/yz11445/projects/Assembly_Sim')
OUT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('geometry', ROOT/'tasks/stack_sawtooth_shulker_small/geometry.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

def mesh(boxes):
    axes = [sorted({b[k][a] for b in boxes for k in (0, 1)}) for a in range(3)]
    occupied = set()
    for i in range(len(axes[0])-1):
        for j in range(len(axes[1])-1):
            for k in range(len(axes[2])-1):
                q = (i,j,k)
                p = [(axes[a][q[a]]+axes[a][q[a]+1])/2 for a in range(3)]
                if any(all(lo[a] < p[a] < hi[a] for a in range(3)) for lo,hi in boxes):
                    occupied.add(q)
    triangles = []
    # Cyclic axes give outward winding on positive faces.
    for q in sorted(occupied):
        for a in range(3):
            u,v = (a+1)%3,(a+2)%3
            for sign in (-1,1):
                neighbor = list(q); neighbor[a] += sign
                if tuple(neighbor) in occupied:
                    continue
                quad = []
                for du,dv in ((0,0),(1,0),(1,1),(0,1)):
                    idx = list(q); idx[a] += int(sign==1); idx[u] += du; idx[v] += dv
                    quad.append(tuple(axes[t][idx[t]] for t in range(3)))
                if sign < 0:
                    quad.reverse()
                triangles.extend(((quad[0],quad[1],quad[2]),(quad[0],quad[2],quad[3])))
    return triangles

def export(name, cells, inset):
    # B is inverted so both parts have their full slab flat on the print bed.
    if name == 'FragmentB':
        cells = tuple((x, 2-y, 2-z) for x,y,z in cells)
    boxes = []
    for x,y,z in cells:
        d = inset if z == 1 else 0.0
        boxes.append(((x*27+d,y*27+d,z*27),((x+1)*27-d,(y+1)*27-d,(z+1)*27)))
    tris = mesh(boxes)
    filename = f'{name}_{"nominal" if inset == 0 else "clearance_0p4mm"}.stl'
    with (OUT/filename).open('wb') as f:
        f.write(b'Shulker small; units millimeters'.ljust(80,b'\0'))
        f.write(struct.pack('<I',len(tris)))
        for p,q,r in tris:
            u = [q[a]-p[a] for a in range(3)]; v = [r[a]-p[a] for a in range(3)]
            n = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
            length = sum(t*t for t in n)**.5
            f.write(struct.pack('<12fH',*(t/length for t in n),*p,*q,*r,0))
    return filename

files = []
for name,cells in [('FragmentA',g.FRAGMENT_A_CELLS),('FragmentB',g.FRAGMENT_B_CELLS)]:
    for inset in (0.0,0.2):
        files.append(export(name,cells,inset))
print('\n'.join(files))
