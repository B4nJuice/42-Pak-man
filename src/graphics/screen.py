import pygame
from pygame import Surface

from .gpu_renderer import GPURenderer
from .mesh import Mesh


class MeshLayer:
    def __init__(self) -> None:
        self.meshes: list[Mesh] = []


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

        if hasattr(mesh, "get_layer"):
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

    def release(self) -> None:
        for layer in (self.static_mesh_layer, self.dynamic_mesh_layer):
            for mesh in layer.meshes:
                texture = getattr(mesh, "texture", None)
                if texture is not None:
                    texture.release()
                    mesh.texture = None
        self.gpu_renderer.release()
