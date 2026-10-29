from typing import TYPE_CHECKING

import pygame
from moderngl import Context
from pygame import Surface
from pygame.event import Event

if TYPE_CHECKING:
    from src.ui.interface import Interface

from .clickable import Clickable
from .gpu_renderer import GPURenderer
from .mesh import Mesh
from .mesh_layer import LayerProtocol, MeshLayer
from .meshes.plane import Plane
from .super_mesh import SuperMesh


class Screen:
    width: int
    height: int
    gpu_renderer: GPURenderer
    moderngl_context: Context
    layer: MeshLayer
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
        self.layer = MeshLayer()
        self.clickables = []
        self._hovered_clickables = set()
        self._last_mouse_position = None

    def add_layer(
                self,
                layer: MeshLayer
            ) -> None:
        self.layer.meshes.append(layer)
        self.search_for_clickable(layer, [layer])

    def search_for_clickable(
                self,
                layer: MeshLayer,
                parents: list[LayerProtocol] | None = None
            ) -> None:
        if parents is None:
            parents = []

        for mesh in layer.meshes:
            if hasattr(mesh, "get_layer"):
                self.search_for_clickable(mesh.get_layer(), parents + [mesh])
                continue
            if (
                isinstance(mesh, Clickable)
                and (mesh._on_click or mesh._on_hover)
            ):
                mesh.set_parents(parents)
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
            self.search_for_clickable(mesh.get_layer(), [mesh])
            self.layer.meshes.append(mesh)
            return

        if (
            isinstance(mesh, Clickable)
            and (mesh._on_click or mesh._on_hover)
        ):
            self.clickables.append(mesh)

        self.layer.meshes.append(mesh)

    def refresh(self) -> None:
        self.gpu_renderer.render(self.layer.meshes)
