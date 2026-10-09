import pygame
from pygame import Surface
from moderngl import Context

from ..ui.interface import Interface
from .gpu_renderer import GPURenderer
from .mesh import Mesh
from .mesh_layer import MeshLayer
from .super_mesh import SuperMesh


class Screen:
    width: int
    height: int
    gpu_renderer: GPURenderer
    moderngl_context: Context
    static_mesh_layer: MeshLayer
    dynamic_mesh_layer: MeshLayer

    def __init__(
                self,
                width: int,
                height: int,
                pygame_screen: Surface
            ) -> None:
        if not pygame_screen.get_flags() & pygame.OPENGL:
            raise ValueError("Screen requires a pygame OpenGL display")

        self.width = width
        self.height = height
        self.gpu_renderer = GPURenderer(width, height)
        self.moderngl_context = self.gpu_renderer.context
        self.static_mesh_layer = MeshLayer()
        self.dynamic_mesh_layer = MeshLayer()

    def add_layer(
                self,
                layer: MeshLayer
            ) -> None:
        self.dynamic_mesh_layer.meshes.append(layer)

    def add_mesh(self, mesh: Mesh | Interface) -> None:
        if isinstance(mesh, Interface | SuperMesh):
            self.add_layer(mesh.get_layer())
            return

        layer = (
            self.dynamic_mesh_layer
            if mesh.is_dynamic()
            else self.static_mesh_layer
        )
        layer.meshes.append(mesh)

    def refresh(self) -> None:
        self.gpu_renderer.render(
            self.static_mesh_layer.meshes,
            self.dynamic_mesh_layer.meshes
        )
