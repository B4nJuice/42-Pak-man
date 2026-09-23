from functools import lru_cache, singledispatchmethod
from collections.abc import Iterable
from importlib.resources import files
import numpy as np
import moderngl

from src.graphics import OperationEnum, Mesh
from src.graphics.meshes import Line, Plane, Polygon, ImageTexture, Circle


@lru_cache(maxsize=None)
def _load_shader(name: str) -> str:
    return (files("src.graphics.shaders") / name).read_text()


class GPURenderer:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.context = moderngl.create_context()

        self.mesh_program = self.context.program(
            vertex_shader=_load_shader("mesh.vert"),
            fragment_shader=_load_shader("mesh.frag"),
        )
        self.copy_program = self.context.program(
            vertex_shader=_load_shader("copy.vert"),
            fragment_shader=_load_shader("copy.frag"),
        )
        self.blit_program = self.context.program(
            vertex_shader=_load_shader("copy.vert"),
            fragment_shader=_load_shader("blit.frag"),
        )
        self.image_program = self.context.program(
            vertex_shader=_load_shader("image.vert"),
            fragment_shader=_load_shader("image.frag"),
        )
        self.circle_program = self.context.program(
            vertex_shader=_load_shader("circle.vert"),
            fragment_shader=_load_shader("circle.frag"),
        )

        self.copy_quad = self._create_copy_quad()
        self.screen_quad = self._create_screen_quad()
        self.textures = [
            self.context.texture((width, height), 4),
            self.context.texture((width, height), 4),
        ]
        for texture in self.textures:
            texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.framebuffers = [
            self.context.framebuffer(color_attachments=texture)
            for texture in self.textures
        ]

    def _create_screen_quad(self) -> moderngl.VertexArray:
        vertices = np.array(
            [0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0],
            dtype="f4",
        )
        buffer = self.context.buffer(vertices.tobytes())
        return self.context.simple_vertex_array(
            self.blit_program,
            buffer,
            "in_position",
        )

    def _create_copy_quad(self) -> moderngl.VertexArray:
        vertices = np.array(
            [0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0],
            dtype="f4",
        )
        buffer = self.context.buffer(vertices.tobytes())
        return self.context.simple_vertex_array(
            self.copy_program,
            buffer,
            "in_position",
        )

    @singledispatchmethod
    def _vertices(self, mesh: Mesh) -> tuple[np.ndarray, int]:
        raise TypeError(f"Unsupported mesh type: {type(mesh).__name__}")

    @_vertices.register
    def _(self, plane: Plane) -> tuple[np.ndarray, int]:
        first, second = plane.positions
        vertices = np.array(
            [
                first.x, first.y,
                second.x, first.y,
                first.x, second.y,
                second.x, second.y,
            ],
            dtype="f4",
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
            return np.empty(0, dtype="f4"), moderngl.TRIANGLES

        positions = polygon.positions + [polygon.positions[0]]
        segments = []
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

        return np.asarray(segments, dtype="f4").reshape(-1), moderngl.TRIANGLES

    @_vertices.register
    def _(self, image: ImageTexture) -> tuple[np.ndarray, int]:
        x, y = image.position.x, image.position.y

        left: float = x - image.width / 2
        right: float = x + image.width / 2
        top: float = y - image.height / 2
        bottom: float = y + image.height / 2

        vertices = np.array([
            left,  top,    0, 0,
            right, top,    1, 0,
            left,  bottom, 0, 1,
            right, bottom, 1, 1,
        ], dtype="f4")

        if image.texture is None:
            image.texture = self.context.texture(
                image.image.size,
                4,
                image.image.tobytes(),
            )

        return vertices, moderngl.TRIANGLE_STRIP

    @_vertices.register
    def _(self, circle: Circle) -> tuple[np.ndarray, int]:
        x, y = circle.position.x, circle.position.y
        radius = circle.radius
        vertices = np.array(
            [
                x - radius, y - radius,
                x + radius, y - radius,
                x - radius, y + radius,
                x + radius, y + radius,
            ],
            dtype="f4",
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
            dtype="f4",
        )

        return vertices, moderngl.TRIANGLE_STRIP

    @singledispatchmethod
    def _draw_mesh(
                self,
                mesh: Mesh,
                source: moderngl.Texture,
                target: moderngl.Framebuffer
            ) -> None:
        raise TypeError(f"Unsupported mesh type: {type(mesh).__name__}")

    @_draw_mesh.register
    def _(
                self,
                mesh: Mesh,
                source: moderngl.Texture,
                target: moderngl.Framebuffer
            ) -> None:
        if mesh.hidden or mesh.color.is_default:
            return

        vertices, mode = self._vertices(mesh)
        vertex_buffer = self.context.buffer(vertices.tobytes())

        vao = self.context.simple_vertex_array(
            self.mesh_program,
            vertex_buffer,
            "in_position",
        )
        self.mesh_program["screen_size"].value = (self.width, self.height)
        self.mesh_program["mesh_color"].value = (
            mesh.color.r / 255,
            mesh.color.g / 255,
            mesh.color.b / 255,
            mesh.color.a / 255,
        )
        self.mesh_program["operation"].value = mesh.operation.value
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
        if mesh.hidden or mesh.color.is_default:
            return

        vertices, mode = self._vertices(mesh)
        vertex_buffer = self.context.buffer(vertices.tobytes())
        vao = self.context.simple_vertex_array(
            self.circle_program,
            vertex_buffer,
            "in_position",
        )
        self.circle_program["height"].value = self.height
        self.circle_program["screen_size"].value = (self.width, self.height)
        self.circle_program["color"].value = (
            mesh.color.r / 255,
            mesh.color.g / 255,
            mesh.color.b / 255,
            mesh.color.a / 255,
        )
        self.circle_program["center"].value = (
            mesh.position.x,
            mesh.position.y,
        )
        self.circle_program["radius"].value = mesh.radius
        self.circle_program["thickness"].value = mesh.thickness
        self.circle_program["filled"].value = mesh.filled
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
        vertices, mode = self._vertices(mesh)
        vertex_buffer = self.context.buffer(vertices.tobytes())
        vao = self.context.vertex_array(
            self.image_program,
            [
                (
                    vertex_buffer,
                    "2f 2f",
                    "in_position",
                    "in_texcoord",
                ),
            ],
        )
        mesh.texture.use(1)
        self.image_program["image_texture"].value = 1
        self.image_program["operation"].value = mesh.operation.value
        self.image_program["screen_size"].value = (self.width, self.height)
        target.use()
        vao.render(mode=mode)
        vertex_buffer.release()
        vao.release()

    def render(
                self,
                static_meshes: Iterable[Mesh],
                dynamic_meshes: Iterable[Mesh]
            ) -> None:
        source_index = 0
        target_index = 1
        self.framebuffers[source_index].clear(0.0, 0.0, 0.0, 0.0)

        for mesh in [*static_meshes, *dynamic_meshes]:
            source = self.textures[source_index]
            target = self.framebuffers[target_index]
            target.use()
            source.use(0)
            self.copy_program["source_texture"].value = 0
            self.copy_quad.render(mode=moderngl.TRIANGLE_STRIP)
            self._draw_mesh(mesh, source, target)
            source_index, target_index = target_index, source_index

        self.context.screen.use()
        self.textures[source_index].use(0)
        self.blit_program["source_texture"].value = 0
        self.screen_quad.render(mode=moderngl.TRIANGLE_STRIP)
        self.context.finish()

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
