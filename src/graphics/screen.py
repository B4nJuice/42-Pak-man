import pygame
from pygame import Surface

from .gpu_renderer import GPURenderer
from .mesh import Mesh
from .mesh_layer import MeshLayer
from .super_mesh import SuperMesh


class Screen:
    def __init__(
                self,
                width: int,
                height: int,
                pygame_screen: Surface
            ) -> None:
        if not pygame_screen.get_flags() & pygame.OPENGL:
            raise ValueError("Screen requires a pygame OpenGL display")

        self.width: int = width
        self.height: int = height
        self.gpu_renderer: GPURenderer = GPURenderer(width, height)
        self.static_mesh_layer: MeshLayer = MeshLayer()
        self.dynamic_mesh_layer: MeshLayer = MeshLayer()

    def add_layer(
                self,
                layer: MeshLayer
            ) -> None:
        for mesh in layer.meshes:
            self.add_mesh(mesh)

    def add_mesh(self, mesh: Mesh) -> None:
        if isinstance(mesh, SuperMesh):
            self.add_layer(mesh.get_layer())
            return

        layer = (
            self.dynamic_mesh_layer
            if mesh.is_dynamic
            else self.static_mesh_layer
        )
        layer.meshes.append(mesh)

    def refresh(self) -> None:
        self.gpu_renderer.render(
            self.static_mesh_layer.meshes,
            self.dynamic_mesh_layer.meshes
        )
