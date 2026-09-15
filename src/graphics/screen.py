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

        self.width = width
        self.height = height
        self.pygame_screen = pygame_screen
        self.gpu_renderer = GPURenderer(width, height)
        self.static_mesh_layer = MeshLayer()
        self.dynamic_mesh_layer = MeshLayer()

    def add_mesh(self, mesh: Mesh) -> None:
        layer = (
            self.dynamic_mesh_layer
            if mesh.is_dynamic
            else self.static_mesh_layer
        )
        layer.meshes.append(mesh)

    def init(self) -> None:
        self.gpu_renderer.render(
            self.static_mesh_layer.meshes,
            self.dynamic_mesh_layer.meshes
        )

    def refresh_dynamic(self) -> None:
        self.gpu_renderer.render(
            self.static_mesh_layer.meshes,
            self.dynamic_mesh_layer.meshes
        )