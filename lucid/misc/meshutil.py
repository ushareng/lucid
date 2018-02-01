"""3D mesh manipulation utilities."""

from builtins import str
import numpy as np

def _parse_face(line):
  """Parse .obj faces line."""
  vert_tuples = []
  for chunk in line.split():
    vt = []
    for c in chunk.split('/'):
      c = int(c) if c else 0
      vt.append(c)
    while len(vt) < 3:
      vt.append(0)
    vert_tuples.append(tuple(vt))
  return vert_tuples


def load_obj(fn):
  """Load 3d mesh form .obj' file.
  
  Args:
    fn: Input file name or file-like object.
    
  Returns:
    dictionary with following keys:
      position: np.float32, (n, 3) array, vertex positions
      uv: np.float32, (n, 2) array, vertex uv coordinates
      normal: np.float32, (n, 3) array, vertex uv normals
      face: np.int32, (k*3,) traingular face indices
  """
  position = [np.zeros(3, dtype=np.float32)]
  normal = [np.zeros(3, dtype=np.float32)]
  uv = [np.zeros(2, dtype=np.float32)]

  tuple2idx = {}
  out_position, out_normal, out_uv, out_face = [], [], [], []
  
  input_file = open(fn) if isinstance(fn, str) else fn
  for line in input_file:
    line = line.strip()
    if not line or line[0] == '#':
      continue
    tag, line = line.split(' ', 1)
    if tag == 'v':
      position.append(np.fromstring(line, sep=' '))
    elif tag == 'vt':
      uv.append(np.fromstring(line, sep=' '))
    elif tag == 'vn':
      normal.append(np.fromstring(line, sep=' '))
    elif tag == 'f':
      face_idx = []
      for vt in _parse_face(line):
        if vt not in tuple2idx:
          pos_idx, uv_idx, normal_idx = vt
          out_position.append(position[pos_idx])
          out_normal.append(normal[normal_idx])
          out_uv.append(uv[uv_idx])
          tuple2idx[vt] = len(out_position)-1
        face_idx.append(tuple2idx[vt])
      # generate face triangles
      for i in range(1, len(face_idx)-1):
        for vi in [0, i, i+1]:
          out_face.append(face_idx[vi])

  return dict(
      position=np.float32(out_position),
      normal=np.float32(out_normal),
      uv=np.float32(out_uv),
      face=np.int32(out_face))