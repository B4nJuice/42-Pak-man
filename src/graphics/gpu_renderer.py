from collections.abc import Iterable, Iterator
from functools import cache, singledispatchmethod
from importlib.resources import files
from typing import cast

import moderngl
import numpy as np

from src.core.displayable import Displayable
from src.graphics.color import OperationEnum
from src.graphics.mesh import Mesh
from src.graphics.mesh_layer import LayerProtocol, MeshLayer
from src.graphics.meshes import (
    Character,
    Circle,
    ImageTexture,
    Line,
    Plane,
    Polygon,
)


def get_uniform(
    program: moderngl.Program,
    name: str,
) -> moderngl.Uniform:
    return cast(moderngl.Uniform, program[name])


@cache
def _load_shader(name: str) -> str:
    return (files('src.graphics.shaders') / name).read_text()


class GPURenderer:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.context = moderngl.create_context()

        self.mesh_program = self.context.program(
            vertex_shader=_load_shader('mesh.vert'),
            fragment_shader=_load_shader('mesh.frag'),
        )
        self.copy_program = self.context.program(
            vertex_shader=_load_shader('copy.vert'),
            fragment_shader=_load_shader('copy.frag'),
        )
        self.blit_program = self.context.program(
            vertex_shader=_load_shader('copy.vert'),
            fragment_shader=_load_shader('blit.frag'),
        )
        self.image_program = self.context.program(
            vertex_shader=_load_shader('image.vert'),
            fragment_shader=_load_shader('image.frag'),
        )
        self.circle_program = self.context.program(
            vertex_shader=_load_shader('circle.vert'),
            fragment_shader=_load_shader('circle.frag'),
        )
        get_uniform(self.mesh_program, 'previous_frame').value = 0
        get_uniform(self.image_program, 'previous_frame').value = 0

        self.copy_quad = self._create_copy_quad()
        self.screen_quad = self._create_screen_quad()
        self.textures = [
            self.context.texture((width, height), 4),
            self.context.texture((width, height), 4),
        ]
        self.framebuffers = [
            self.context.framebuffer(color_attachments=texture)
            for texture in self.textures
        ]

    def _create_screen_quad(self) -> moderngl.VertexArray:
        vertices = np.array(
            [0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0],
            dtype='f4',
        )
        buffer = self.context.buffer(vertices.tobytes())
        return self.context.simple_vertex_array(
            self.blit_program,
            buffer,
            'in_position',
        )

    def _create_copy_quad(self) -> moderngl.VertexArray:
        vertices = np.array(
            [0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0],
            dtype='f4',
        )
        buffer = self.context.buffer(vertices.tobytes())
        return self.context.simple_vertex_array(
            self.copy_program,
            buffer,
            'in_position',
        )

    @singledispatchmethod
    def _vertices(self, mesh: Mesh) -> tuple[np.ndarray, int]:
        raise TypeError(f'Unsupported mesh type: {type(mesh).__name__}')

    @_vertices.register
    def _(self, plane: Plane) -> tuple[np.ndarray, int]:
        first, second = plane.get_positions()
        vertices = np.array(
            [
                first.x, first.y,
                second.x, first.y,
                first.x, second.y,
                second.x, second.y,
            ],
            dtype='f4',
        )
        return vertices, moderngl.TRIANGLE_STRIP

    @_vertices.register
    def _(self, line: Line) -> tuple[np.ndarray, int]:
        return self._thick_segment_vertices(
            line.start_position.x,
            line.start_position.y,
            line.end_position.x,
            line.end_position.y,
            line.thickness,
        )

    @_vertices.register
    def _(self, polygon: Polygon) -> tuple[np.ndarray, int]:
        if len(polygon.positions) < 2:
            return np.empty(0, dtype='f4'), moderngl.TRIANGLES

        positions = polygon.positions + [polygon.positions[0]]
        segments: list[np.ndarray] = []
        for start, end in zip(positions, positions[1:]):
            start_x, start_y = start.x, start.y
            end_x, end_y = end.x, end.y

            if polygon.smooth_end:
                delta_x = end_x - start_x
                delta_y = end_y - start_y
                length = (delta_x * delta_x + delta_y * delta_y) ** 0.5

                if length > 0:
                    extension = polygon.thickness / (2 * length)
                    start_x -= delta_x * extension
                    start_y -= delta_y * extension
                    end_x += delta_x * extension
                    end_y += delta_y * extension

            vertices, _ = self._thick_segment_vertices(
                start_x,
                start_y,
                end_x,
                end_y,
                polygon.thickness,
            )
            first, second, third, fourth = vertices.reshape(4, 2)
            segments.extend((first, second, third, third, second, fourth))

        return np.asarray(segments, dtype='f4').reshape(-1), moderngl.TRIANGLES

    @_vertices.register
    def _(self, image: ImageTexture) -> tuple[np.ndarray, int]:
        x, y = image.get_position().x, image.get_position().y

        image_width: int = image.get_width()
        image_height: int = image.get_height()

        left: float = x - image_width / 2
        right: float = x + image_width / 2
        top: float = y - image_height / 2
        bottom: float = y + image_height / 2

        vertices = np.array([
            left,  top,    0, 0,
            right, top,    1, 0,
            left,  bottom, 0, 1,
            right, bottom, 1, 1,
        ], dtype='f4')

        if image.texture is None:
            image.texture = self.context.texture(
                image.image.size,
                4,
                image.image.tobytes()
            )
            image.texture.filter = (moderngl.NEAREST, moderngl.NEAREST)

        return vertices, moderngl.TRIANGLE_STRIP

    @_vertices.register
    def _(self, entity: Displayable) -> tuple[np.ndarray, int]:

        pos = entity.get_position_on_screen()

        x, y = pos.x, pos.y

        image_width: int = entity.get_width()
        image_height: int = entity.get_height()

        left: float = x - image_width / 2
        right: float = x + image_width / 2
        top: float = y - image_height / 2
        bottom: float = y + image_height / 2

        vertices = np.array([
            left,  top,    0, 0,
            right, top,    1, 0,
            left,  bottom, 0, 1,
            right, bottom, 1, 1,
        ], dtype='f4')

        return vertices, moderngl.TRIANGLE_STRIP

    @_vertices.register
    def _(self, character: Character) -> tuple[np.ndarray, int]:
        x, y = character.position.x, character.position.y
        width = character.infos['width'] * character.scale
        height = character.infos['height'] * character.scale

        vertices = np.array([
            x, y, 0, 0,
            x + width, y, 1, 0,
            x, y + height, 0, 1,
            x + width, y + height, 1, 1,
        ], dtype='f4')

        return vertices, moderngl.TRIANGLE_STRIP

    @_vertices.register
    def _(self, circle: Circle) -> tuple[np.ndarray, int]:
        x, y = circle.get_position().x, circle.get_position().y
        radius = circle.radius
        vertices = np.array(
            [
                x - radius, y - radius,
                x + radius, y - radius,
                x - radius, y + radius,
                x + radius, y + radius,
            ],
            dtype='f4',
        )
        return vertices, moderngl.TRIANGLE_STRIP

    @staticmethod
    def _thick_segment_vertices(
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        thickness: int,
    ) -> tuple[np.ndarray, int]:
        dx = end_x - start_x
        dy = end_y - start_y
        length = max((dx * dx + dy * dy) ** 0.5, 1.0)
        radius = max(thickness, 1) * 0.5
        offset_x = -dy / length * radius
        offset_y = dx / length * radius
        vertices = np.array(
            [
                start_x - offset_x, start_y - offset_y,
                start_x + offset_x, start_y + offset_y,
                end_x - offset_x, end_y - offset_y,
                end_x + offset_x, end_y + offset_y,
            ],
            dtype='f4',
        )

        return vertices, moderngl.TRIANGLE_STRIP

    @singledispatchmethod
    def _draw_mesh(
                self,
                mesh: Mesh,
                source: moderngl.Texture,
                target: moderngl.Framebuffer
            ) -> None:
        raise TypeError(f'Unsupported mesh type: {type(mesh).__name__}')

    @_draw_mesh.register
    def _(
                 self,
                 entity: Displayable,
                 source: moderngl.Texture,
                 target: moderngl.Framebuffer
             ) -> None:
        if entity.is_hidden():
            return

        vertices, mode = self._vertices(entity)
        vertex_buffer = self.context.buffer(vertices.tobytes())
        vao = self.context.vertex_array(
            self.image_program,
            [
                (
                    vertex_buffer,
                    '2f 2f',
                    'in_position',
                    'in_texcoord',
                ),
            ],
        )
        entity.get_texture().texture.use(1)
        get_uniform(self.image_program, 'image_texture').value = 1
        get_uniform(
            self.image_program, 'operation'
        ).value = OperationEnum.SET.value
        get_uniform(self.image_program, 'use_tint').value = False
        get_uniform(
            self.image_program, 'screen_size'
        ).value = (self.width, self.height)
        target.use()
        vao.render(mode=mode)
        vertex_buffer.release()
        vao.release()

    @_draw_mesh.register
    def _(
                self,
                mesh: Mesh,
                source: moderngl.Texture,
                target: moderngl.Framebuffer
            ) -> None:
        if mesh.is_hidden():
            return

        vertices, mode = self._vertices(mesh)
        vertex_buffer = self.context.buffer(vertices.tobytes())

        vao = self.context.simple_vertex_array(
            self.mesh_program,
            vertex_buffer,
            'in_position',
        )
        get_uniform(
            self.mesh_program, 'screen_size'
        ).value = (self.width, self.height)
        get_uniform(self.mesh_program, 'mesh_color').value = (
            mesh.get_color().r / 255,
            mesh.get_color().g / 255,
            mesh.get_color().b / 255,
            mesh.get_color().a / 255,
        )
        get_uniform(
            self.mesh_program, 'operation'
        ).value = mesh.get_operation().value
        source.use(0)
        target.use()

        vao.render(mode=mode)
        vertex_buffer.release()
        vao.release()

    @_draw_mesh.register
    def _(
                self,
                mesh: Circle,
                source: moderngl.Texture,
                target: moderngl.Framebuffer
            ) -> None:
        if mesh.is_hidden():
            return

        vertices, mode = self._vertices(mesh)
        vertex_buffer = self.context.buffer(vertices.tobytes())
        vao = self.context.simple_vertex_array(
            self.circle_program,
            vertex_buffer,
            'in_position',
        )
        get_uniform(self.circle_program, 'height').value = self.height
        get_uniform(
            self.circle_program, 'screen_size'
        ).value = (self.width, self.height)
        get_uniform(self.circle_program, 'color').value = (
            mesh.get_color().r / 255,
            mesh.get_color().g / 255,
            mesh.get_color().b / 255,
            mesh.get_color().a / 255,
        )
        get_uniform(self.circle_program, 'center').value = (
            mesh.position.x,
            mesh.position.y,
        )
        get_uniform(self.circle_program, 'radius').value = mesh.radius
        get_uniform(self.circle_program, 'thickness').value = mesh.thickness
        get_uniform(self.circle_program, 'filled').value = mesh.filled
        target.use()
        vao.render(mode=mode)
        vertex_buffer.release()
        vao.release()

    @_draw_mesh.register
    def _(
                self,
                mesh: ImageTexture,
                source: moderngl.Texture,
                target: moderngl.Framebuffer
            ) -> None:
        if mesh.is_hidden():
            return

        vertices, mode = self._vertices(mesh)
        vertex_buffer = self.context.buffer(vertices.tobytes())
        vao = self.context.vertex_array(
            self.image_program,
            [
                (
                    vertex_buffer,
                    '2f 2f',
                    'in_position',
                    'in_texcoord',
                ),
            ],
        )
        mesh.texture.use(1)
        source.use(0)
        get_uniform(self.image_program, 'previous_frame').value = 0
        get_uniform(self.image_program, 'image_texture').value = 1
        get_uniform(
            self.image_program, 'operation'
        ).value = mesh.get_operation().value
        get_uniform(self.image_program, 'use_tint').value = False
        get_uniform(
            self.image_program, 'screen_size'
        ).value = (self.width, self.height)
        target.use()
        vao.render(mode=mode)
        vertex_buffer.release()
        vao.release()

    @_draw_mesh.register
    def _(
                self,
                mesh: Character,
                source: moderngl.Texture,
                target: moderngl.Framebuffer
            ) -> None:
        if mesh.is_hidden():
            return

        vertices, mode = self._vertices(mesh)
        vertex_buffer = self.context.buffer(vertices.tobytes())
        vao = self.context.vertex_array(
            self.image_program,
            [
                (
                    vertex_buffer,
                    '2f 2f',
                    'in_position',
                    'in_texcoord',
                ),
            ],
        )
        mesh.infos['texture'].use(1)
        get_uniform(self.image_program, 'image_texture').value = 1
        get_uniform(
            self.image_program, 'operation'
        ).value = mesh.get_operation().value
        get_uniform(self.image_program, 'use_tint').value = True
        get_uniform(self.image_program, 'tint').value = (
            mesh.get_color().r / 255,
            mesh.get_color().g / 255,
            mesh.get_color().b / 255,
            mesh.get_color().a / 255,
        )
        get_uniform(
            self.image_program, 'screen_size'
        ).value = (self.width, self.height)
        target.use()
        vao.render(mode=mode)
        vertex_buffer.release()
        vao.release()

    @_draw_mesh.register
    def _(
                self,
                layer: MeshLayer,
                source: moderngl.Texture,
                target: moderngl.Framebuffer
            ) -> None:
        for mesh in layer.meshes:
            if hasattr(mesh, "get_layer"):
                mesh = mesh.get_layer()
            self._draw_mesh(mesh, source, target)

    def render(
                self,
                static_meshes: Iterable[Mesh | LayerProtocol | Displayable],
                dynamic_meshes: Iterable[Mesh | LayerProtocol | Displayable]
            ) -> None:
        self.source_index = 0
        self.target_index = 1
        self.framebuffers[self.source_index].clear(0.0, 0.0, 0.0, 0.0)

        for mesh in self._iter_meshes([*static_meshes, *dynamic_meshes]):
            source = self.textures[self.source_index]
            target = self.framebuffers[self.target_index]
            target.use()
            source.use(0)
            get_uniform(self.copy_program, 'source_texture').value = 0
            self.copy_quad.render(mode=moderngl.TRIANGLE_STRIP)
            self._draw_mesh(mesh, source, target)
            self.source_index, self.target_index = (
                self.target_index, self.source_index
            )

        self.context.screen.use()
        self.textures[self.source_index].use(0)
        get_uniform(self.blit_program, 'source_texture').value = 0
        self.screen_quad.render(mode=moderngl.TRIANGLE_STRIP)

    def release(self) -> None:
        for framebuffer in self.framebuffers:
            framebuffer.release()
        for texture in self.textures:
            texture.release()
        self.copy_quad.release()
        self.screen_quad.release()
        self.mesh_program.release()
        self.copy_program.release()
        self.blit_program.release()
        self.image_program.release()
        self.circle_program.release()

    def _iter_meshes(
        self,
        meshes: Iterable[Mesh | LayerProtocol | Displayable],
    ) -> Iterator[Mesh | LayerProtocol | Displayable]:
        for mesh in meshes:
            if mesh.is_hidden():
                continue
            if isinstance(mesh, MeshLayer):
                yield from self._iter_meshes(mesh.meshes)
            else:
                if hasattr(mesh, "get_layer"):
                    mesh = mesh.get_layer()
                    yield from self._iter_meshes([mesh])
                else:
                    yield mesh
