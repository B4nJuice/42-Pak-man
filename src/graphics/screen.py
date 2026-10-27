import pygame
from moderngl import Context
from pygame import Surface
from pygame.event import Event
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.ui.interface import Interface

from .clickable import Clickable
from .meshes.plane import Plane
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
    clickables: list[Clickable]
    _hovered_clickables: set[Clickable]
    _last_mouse_position: tuple[int, int] | None
    background: Plane

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
        self.clickables = []
        self._hovered_clickables = set()
        self._last_mouse_position = None

    def add_layer(
                self,
                layer: MeshLayer
            ) -> None:
        self.dynamic_mesh_layer.meshes.append(layer)
        self.search_for_clickable(layer)

    def search_for_clickable(self, layer: MeshLayer) -> None:
        for mesh in layer.meshes:
            if hasattr(mesh, "get_layer"):
                self.search_for_clickable(mesh.get_layer())
                continue
            if (
                isinstance(mesh, Clickable)
                and (mesh._on_click or mesh._on_hover)
            ):
                self.clickables.append(mesh)

    def click(self, _: Event, __: int) -> None:
        x, y = pygame.mouse.get_pos()
        for c in self.clickables:
            c.click(x, y)

    def hover(self, _: Event, __: int) -> None:
        position = pygame.mouse.get_pos()
        if position == self._last_mouse_position:
            return
        self._last_mouse_position = position
        x, y = position
        hovered_clickables = set()
        for c in self.clickables:
            if c._on_hover and c.contains(x, y):
                hovered_clickables.add(c)

        for c in hovered_clickables - self._hovered_clickables:
            c.hover(x, y)
        self._hovered_clickables = hovered_clickables

    def add_mesh(self, mesh: 'Mesh | Interface') -> None:
        from src.ui.interface import Interface

        if isinstance(mesh, Interface | SuperMesh):
            self.add_layer(mesh.get_layer())
            return

        if (
            isinstance(mesh, Clickable)
            and (mesh._on_click or mesh._on_hover)
        ):
            self.clickables.append(mesh)

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
