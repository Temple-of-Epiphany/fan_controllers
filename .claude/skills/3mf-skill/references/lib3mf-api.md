# lib3mf Python API Quick Reference

Official docs: https://github.com/3MFConsortium/lib3mf
Python bindings install: `pip install lib3mf`

---

## Initialization

```python
import lib3mf

wrapper = lib3mf.Wrapper()         # load the native library
model   = wrapper.CreateModel()    # new empty model
```

---

## Reading a 3MF

```python
reader = model.QueryReader("3mf")
reader.SetStrictModeActive(False)  # warn, don't abort on errors
reader.ReadFromFile("input.3mf")

# Check warnings
for i in range(reader.GetWarningCount()):
    code, msg = reader.GetWarning(i)
    print(f"Warning {code}: {msg}")
```

---

## Writing a 3MF

```python
writer = model.QueryWriter("3mf")
writer.WriteToFile("output.3mf")
writer.WriteToBuffer()             # returns bytes (for streaming/HTTP)
```

---

## Metadata

```python
meta = model.GetMetaDataGroup()

# Add
meta.AddMetaData(
    namespace,      # "" for standard names
    name,           # "Title", "Author", "Description", "Date", etc.
    value,          # string
    type_,          # "xs:string" (default), "xs:boolean", "xs:integer"
    must_preserve   # bool
)

# Read
count = meta.GetMetaDataCount()
m = meta.GetMetaData(index)
m.GetName()   # → str
m.GetValue()  # → str
m.SetValue(new_value)

# Remove
meta.RemoveMetaData(index)
```

Standard metadata names (no namespace):
`Title`, `Designer`, `Description`, `Copyright`, `LicenseTerms`, `Rating`,
`CreationDate`, `ModificationDate`, `Application`

---

## Mesh Objects

```python
# Create
obj = model.AddMeshObject()
obj.SetName("PartName")
obj.SetType(lib3mf.ObjectType.Model)   # Model | Support | SolidSupport | Other

# Add geometry
obj.AddVertex(lib3mf.Position(x, y, z))
obj.AddTriangle(lib3mf.Triangle(v1_idx, v2_idx, v3_idx))

# Read geometry
vertices  = obj.GetVertices()    # list of lib3mf.Position
triangles = obj.GetTriangles()   # list of lib3mf.Triangle

# Counts
obj.GetVertexCount()
obj.GetTriangleCount()

# Validate
obj.IsValid()                    # True if manifold and watertight
```

Access vertex/triangle data:
```python
v = vertices[i]
x, y, z = v.m_Coordinates[0], v.m_Coordinates[1], v.m_Coordinates[2]

t = triangles[i]
i0, i1, i2 = t.m_Indices[0], t.m_Indices[1], t.m_Indices[2]
```

---

## Build Items

```python
# Place an object on the build plate
transform = wrapper.GetIdentityTransform()   # no rotation, origin position

# Translate to (x, y, z):
transform.m_Field[0][3] = x_offset
transform.m_Field[1][3] = y_offset
transform.m_Field[2][3] = z_offset

build_item = model.AddBuildItem(mesh_obj, transform)
build_item.GetObjectID()   # → int (the object's resource ID)

# Iterate build items
it = model.GetBuildItems()
while it.MoveNext():
    item = it.GetCurrent()
    print(item.GetObjectID())
```

---

## Color Groups

```python
cg = model.AddColorGroup()
cg_id = cg.GetResourceID()

# Add colors (RGBA 0–255 as lib3mf.Color)
idx = cg.AddColor(lib3mf.Color(r=220, g=50, b=50, a=255))

# Apply to entire object
obj.SetObjectLevelProperty(cg_id, idx)

# Apply per-triangle
# (pass property IDs for each triangle when adding)
```

---

## Component Objects (assemblies)

```python
comp_obj = model.AddComponentsObject()
comp_obj.SetName("Assembly")

# Add component references (with per-component transforms)
comp_obj.AddComponent(mesh_obj1, wrapper.GetIdentityTransform())
comp_obj.AddComponent(mesh_obj2, some_transform)

model.AddBuildItem(comp_obj, wrapper.GetIdentityTransform())
```

---

## Iterating Model Objects

```python
# All mesh objects
it = model.GetMeshObjects()
while it.MoveNext():
    obj = it.GetCurrentMeshObject()

# All resources (meshes + components + color groups, etc.)
it = model.GetResources()
while it.MoveNext():
    res = it.GetCurrent()
    print(type(res), res.GetResourceID())
```

---

## Transform Matrix Format

`lib3mf.Transform` is a 4×3 row-major matrix. The last column is the translation:

```
m_Field[0][0]  m_Field[0][1]  m_Field[0][2]  m_Field[0][3]  ← tx
m_Field[1][0]  m_Field[1][1]  m_Field[1][2]  m_Field[1][3]  ← ty
m_Field[2][0]  m_Field[2][1]  m_Field[2][2]  m_Field[2][3]  ← tz
```

Identity + translate to (50, 30, 0):
```python
t = wrapper.GetIdentityTransform()
t.m_Field[0][3] = 50.0
t.m_Field[1][3] = 30.0
```

Rotate 90° around Z then translate:
```python
import math
t = wrapper.GetIdentityTransform()
angle = math.radians(90)
t.m_Field[0][0] =  math.cos(angle)
t.m_Field[0][1] = -math.sin(angle)
t.m_Field[1][0] =  math.sin(angle)
t.m_Field[1][1] =  math.cos(angle)
t.m_Field[0][3] = 80.0   # move right after rotation
```
