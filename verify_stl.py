import json
import struct
from collections import Counter, defaultdict
from pathlib import Path

out = Path(__file__).resolve().parent
results = {}
for path in sorted(out.glob('*.stl')):
    data = path.read_bytes()
    count, = struct.unpack_from('<I', data, 80)
    assert len(data) == 84+50*count
    edges = Counter(); directed = Counter(); verts = set(); volume = 0
    adjacency = defaultdict(set)
    for i in range(count):
        record = struct.unpack_from('<12fH',data,84+50*i)
        a,b,c = [tuple(record[k:k+3]) for k in (3,6,9)]
        verts.update((a,b,c))
        volume += (a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
        for p,q in ((a,b),(b,c),(c,a)):
            edges[tuple(sorted((p,q)))] += 1
            directed[(p,q)] += 1
            adjacency[p].add(q); adjacency[q].add(p)
    pending = set(verts); components = 0
    while pending:
        components += 1; stack = [pending.pop()]
        while stack:
            for v in adjacency[stack.pop()] & pending:
                pending.remove(v); stack.append(v)
    bounds = [[min(v[a] for v in verts),max(v[a] for v in verts)] for a in range(3)]
    bad = sum(n != 2 for n in edges.values())
    consistent = all(directed[(p,q)]==directed[(q,p)] for p,q in edges)
    result = dict(triangles=count,dimensions_mm=[round(hi-lo,5) for lo,hi in bounds],nonmanifold_edges=bad,consistent_winding=consistent,connected_components=components,volume_mm3=round(volume,3))
    assert result['dimensions_mm'] == [240,240,160]
    assert volume > 0 and consistent and components == 1
    if 'clearance' in path.name:
        assert bad == 0
        posts = 5 if 'FragmentA' in path.name else 4
        assert abs(volume - (240*240*80+posts*79.6**2*80)) < 2.0
    results[path.name] = result
(out/'validation.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
