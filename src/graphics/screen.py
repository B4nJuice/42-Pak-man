from math import floor
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
from .scaling_mode import ScalingMode
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
        window_width, window_height = pygame_screen.get_size()
        self.gpu_renderer = GPURenderer(
            width,
            height,
            window_width,
            window_height,
        )
        self.moderngl_context = self.gpu_renderer.context
        self.layer = MeshLayer()
        self.clickables = []
        self._hovered_clickables = set()
        self._last_mouse_position = None

    def resize(self, width: int, height: int) -> None:
        self.gpu_renderer.set_window_size(width, height)

    def add_layer(
                self,
                layer: MeshLayer
            ) -> None:
        self.layer.meshes.append(layer)
        self.search_for_clickable(layer, [layer])

    def get_mouse_pos(self) -> tuple[int, int]:
        return self._translate_mouse_pos(pygame.mouse.get_pos())

    def _translate_mouse_pos(
            self,
            position: tuple[int, int]
            ) -> tuple[int, int]:
        x, y = position
        window_width = self.gpu_renderer.window_width
        window_height = self.gpu_renderer.window_height
        if window_width == 0 or window_height == 0:
            return (0, 0)

        scaling_mode = self.gpu_renderer.scaling_mode
        if scaling_mode == ScalingMode.STRETCH:
            logical_x = x * self.width / window_width
            logical_y = y * self.height / window_height
        else:
            if scaling_mode == ScalingMode.FIT:
                scale = min(
                    window_width / self.width,
                    window_height / self.height
                )
            else:
                scale = max(
                    window_width / self.width,
                    window_height / self.height
                )
            content_width = self.width * scale
            content_height = self.height * scale
            logical_x = (x - (window_width - content_width) / 2) / scale
            logical_y = (y - (window_height - content_height) / 2) / scale

        return (floor(logical_x), floor(logical_y))

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
        x, y = self.get_mouse_pos()
        for c in self.clickables:
            c.click(x, y)

    def hover(self, _: Event, __: int) -> None:
        position = pygame.mouse.get_pos()
        if position == self._last_mouse_position:
            return
        self._last_mouse_position = position
        x, y = self._translate_mouse_pos(position)
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
