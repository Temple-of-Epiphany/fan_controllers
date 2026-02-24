# 3MF XML Schema Reference

The 3MF format is defined by the 3MF Consortium. The core spec is at:
https://github.com/3MFConsortium/spec_core

## Namespaces

| Prefix | Namespace URI | Purpose |
|--------|---------------|---------|
| (default) | `http://schemas.microsoft.com/3dmanufacturing/core/2015/02` | Core geometry |
| `p`    | `http://schemas.microsoft.com/3dmanufacturing/material/2015/02` | Materials extension |
| `s`    | `http://schemas.microsoft.com/3dmanufacturing/slice/2015/07` | Slice extension |
| `b`    | `http://schemas.microsoft.com/3dmanufacturing/beamlattice/2017/02` | Beam lattice |

---

## Minimal Valid 3dmodel.model

```xml
<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="en-US"
       xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">

  <metadata name="Title">My Model</metadata>
  <metadata name="Author">Colin Bitterfield</metadata>
  <metadata name="Description">Example minimal 3MF</metadata>
  <metadata name="Application">Custom Script 1.0</metadata>
  <metadata name="CreationDate">2025-02-21</metadata>

  <resources>
    <object id="1" type="model" name="MyPart">
      <mesh>
        <vertices>
          <vertex x="0" y="0" z="0"/>
          <vertex x="10" y="0" z="0"/>
          <vertex x="10" y="10" z="0"/>
          <vertex x="0" y="10" z="0"/>
          <vertex x="0" y="0" z="5"/>
          <vertex x="10" y="0" z="5"/>
          <vertex x="10" y="10" z="5"/>
          <vertex x="0" y="10" z="5"/>
        </vertices>
        <triangles>
          <!-- Bottom -->
          <triangle v1="0" v2="2" v3="1"/>
          <triangle v1="0" v2="3" v3="2"/>
          <!-- Top -->
          <triangle v1="4" v2="5" v3="6"/>
          <triangle v1="4" v2="6" v3="7"/>
          <!-- Sides -->
          <triangle v1="0" v2="1" v3="5"/>
          <triangle v1="0" v2="5" v3="4"/>
          <triangle v1="1" v2="2" v3="6"/>
          <triangle v1="1" v2="6" v3="5"/>
          <triangle v1="2" v2="3" v3="7"/>
          <triangle v1="2" v2="7" v3="6"/>
          <triangle v1="3" v2="0" v3="4"/>
          <triangle v1="3" v2="4" v3="7"/>
        </triangles>
      </mesh>
    </object>
  </resources>

  <build>
    <item objectid="1"/>
  </build>

</model>
```

---

## Object Types

```xml
<object id="1" type="model" ...>    <!-- renderable geometry (default) -->
<object id="2" type="support" ...>  <!-- support structure -->
<object id="3" type="solidsupport" ...>  <!-- solid support -->
<object id="4" type="other" ...>    <!-- non-printing annotation -->
```

## Transform Attribute

Build items can include an affine transform (4×3 column-major matrix):

```xml
<item objectid="1" transform="1 0 0 0 1 0 0 0 1 50 0 0"/>
```
Format: `m00 m01 m02 m10 m11 m12 m20 m21 m22 tx ty tz`
The last three values are the XYZ translation. The identity transform is:
`1 0 0 0 1 0 0 0 1 0 0 0`

---

## Materials Extension (colors)

```xml
<model xmlns:m="http://schemas.microsoft.com/3dmanufacturing/material/2015/02" ...>
  <resources>
    <!-- Color group -->
    <m:colorgroup id="10">
      <m:color color="#FF3322"/>  <!-- index 0: red -->
      <m:color color="#3366FF"/>  <!-- index 1: blue -->
    </m:colorgroup>

    <!-- Base material group (named materials) -->
    <m:basematerials id="20">
      <m:base name="PLA Red"  displaycolor="#FF3322"/>
      <m:base name="PLA Blue" displaycolor="#3366FF"/>
    </m:basematerials>

    <!-- Object using color group -->
    <object id="1" type="model" pid="10" pindex="0">
      <mesh>...</mesh>
    </object>
  </resources>
</model>
```

---

## [Content_Types].xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels"
    ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="model"
    ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
</Types>
```

## _rels/.rels

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Target="/3D/3dmodel.model" Id="rel-1"
    Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>
```

---

## Units

Valid values for the `unit` attribute on `<model>`:
`micron`, `millimeter` (default), `centimeter`, `meter`, `inch`, `foot`

---

## Winding Order

Triangles must have vertices listed **counter-clockwise** when viewed from outside
the surface (right-hand rule). Incorrect winding = inverted normals = non-manifold mesh.

```
Correct (CCW from outside):    v1 → v2 → v3
```
