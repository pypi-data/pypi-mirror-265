from __future__ import annotations

from enum import Enum

from pydantic import Field

from vbl_aquarium.models.unity import Color, Vector2, Vector3
from vbl_aquarium.utils.vbl_base_model import VBLBaseModel

# CustomAtlas


class CustomAtlasModel(VBLBaseModel):
    name: str
    dimensions: Vector3
    resolution: Vector3


# CustomMesh


class CustomMeshData(VBLBaseModel):
    id: str = Field(alias="ID")
    vertices: list[Vector3]
    triangles: list[int]
    normals: list[Vector3] = None


class CustomMeshModel(VBLBaseModel):
    id: str = Field(alias="ID")
    position: Vector3
    use_reference: bool
    material: str
    scale: Vector3
    color: Color


# Area


class AtlasModel(VBLBaseModel):
    name: str
    reference_coord: Vector3 = None
    areas: list[StructureModel]
    colormap: ColormapModel


class StructureModel(VBLBaseModel):
    name: str
    acronym: str
    atlas_id: int
    color: Color
    # values that come with defaults:
    visible: bool = False
    color_intensity: float = -1
    side: int = 0
    material: str = "default"


# Camera


class CameraModel(VBLBaseModel):
    class CameraMode(str, Enum):
        orthographic = "orthographic"
        perspective = "perspective"

    id: float
    type: str
    position: Vector3
    rotation: Vector3
    target: Vector3
    zoom: float
    pan: Vector2
    mode: CameraMode
    controllable: bool
    main: bool

class CameraRotationModel(VBLBaseModel):
    start_rotation: Vector3
    end_rotation: Vector3

# Individual mesh neuron


class PrimitiveMeshModel(VBLBaseModel):
    data: list[MeshModel]


class MeshModel(VBLBaseModel):
    id: str = Field(alias="ID")
    shape: str
    position: Vector3
    color: Color
    scale: Vector3
    material: str
    interactive: bool


# Particle group


class ParticleGroupModel(VBLBaseModel):
    id: str = Field(alias="ID")
    scale: Vector3
    shape: str
    material: str

    xs: list[float]
    ys: list[float]
    zs: list[float]

    colors: list[Color]


# Utilities
    
class ColormapModel(VBLBaseModel):
    name: str
    min: float
    max: float