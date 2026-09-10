from collections.abc import Iterable
from functools import singledispatchmethod

import moderngl
import numpy as np

from .color import OperationEnum
from .mesh import Mesh
from .meshes.line import Line
from .meshes.plane import Plane
from .meshes.polygon import Polygon


_VERTEX_SHADER = """
#version 330

in vec2 in_position;
uniform vec2 screen_size;

void main() {
    vec2 ndc = in_position / screen_size * 2.0 - 1.0;
    gl_Position = vec4(ndc.x, -ndc.y, 0.0, 1.0);
}
"""

_MESH_FRAGMENT_SHADER = """
#version 330

uniform sampler2D previous_frame;
uniform vec4 mesh_color;
uniform int operation;

out vec4 fragment_color;

void main() {
    vec4 background = texelFetch(
        previous_frame,
        ivec2(gl_FragCoord.xy),
        0
    );
    vec3 color = mesh_color.rgb;

    if (background.a > 0.0) {
        if (operation == 1) {
            color = min(background.rgb + mesh_color.rgb, 1.0);
        } else if (operation == 2) {
            color = max(background.rgb - mesh_color.rgb, 0.0);
        } else if (operation == 3) {
            color = background.rgb * mesh_color.rgb;
        } else if (operation == 4) {
            color = vec3(
                mesh_color.r == 0.0 ? 1.0 : background.r / mesh_color.r,
                mesh_color.g == 0.0 ? 1.0 : background.g / mesh_color.g,
                mesh_color.b == 0.0 ? 1.0 : background.b / mesh_color.b
            );
        } else if (operation == 5) {
            color = min(background.rgb, mesh_color.rgb);
        } else if (operation == 6) {
            color = max(background.rgb, mesh_color.rgb);
        } else if (operation == 7) {
            color = (background.rgb + mesh_color.rgb) * 0.5;
        } else if (operation == 8) {
            color = 1.0 - (1.0 - background.rgb) * (1.0 - mesh_color.rgb);
        } else if (operation == 9) {
            color = abs(background.rgb - mesh_color.rgb);
        } else if (operation == 10) {
            color = 1.0 - mesh_color.rgb;
        } else if (operation == 11) {
            color = mix(background.rgb, mesh_color.rgb, mesh_color.a);
        }
    }

    fragment_color = vec4(color, 1.0);
}
"""

_COPY_FRAGMENT_SHADER = """
#version 330

uniform sampler2D source_texture;
out vec4 fragment_color;

void main() {
    fragment_color = texelFetch(
        source_texture,
        ivec2(gl_FragCoord.xy),
        0
    );
}
"""

_BLIT_VERTEX_SHADER = """
#version 330

in vec2 in_position;
out vec2 texture_coordinate;

void main() {
    texture_coordinate = vec2(in_position.x, 1.0 - in_position.y);
    vec2 ndc = in_position * 2.0 - 1.0;
    gl_Position = vec4(ndc.x, -ndc.y, 0.0, 1.0);
}
"""

_BLIT_FRAGMENT_SHADER = """
#version 330

uniform sampler2D source_texture;
in vec2 texture_coordinate;
out vec4 fragment_color;

void main() {
    fragment_color = texture(source_texture, texture_coordinate);
}
"""

_OPERATION_IDS = {
    OperationEnum.SET: 0,
    OperationEnum.ADD: 1,
    OperationEnum.SUBTRACT: 2,
    OperationEnum.MULTIPLY: 3,
    OperationEnum.DIVIDE: 4,
    OperationEnum.MINIMUM: 5,
    OperationEnum.MAXIMUM: 6,
    OperationEnum.AVERAGE: 7,
    OperationEnum.SCREEN: 8,
    OperationEnum.DIFFERENCE: 9,
    OperationEnum.INVERT: 10,
    OperationEnum.ALPHA: 11,
}


class GPURenderer:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.context = moderngl.create_context()

        self.mesh_program = self.context.program(
            vertex_shader=_VERTEX_SHADER,
            fragment_shader=_MESH_FRAGMENT_SHADER,
        )
        self.copy_program = self.context.program(
            vertex_shader=_BLIT_VERTEX_SHADER,
            fragment_shader=_COPY_FRAGMENT_SHADER,
        )
        self.blit_program = self.context.program(
            vertex_shader=_BLIT_VERTEX_SHADER,
            fragment_shader=_BLIT_FRAGMENT_SHADER,
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
            vertices, _ = self._thick_segment_vertices(
                start.x,
                start.y,
                end.x,
                end.y,
                polygon.thickness,
            )
            first, second, third, fourth = vertices.reshape(4, 2)
            segments.extend((first, second, third, third, second, fourth))

        return np.asarray(segments, dtype="f4").reshape(-1), moderngl.TRIANGLES

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

    def _draw_mesh(self, mesh: Mesh, source: moderngl.Texture, target: moderngl.Framebuffer) -> None:
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
            mesh.color.r / 255.0,
            mesh.color.g / 255.0,
            mesh.color.b / 255.0,
            mesh.color.a / 255.0,
        )
        self.mesh_program["operation"].value = _OPERATION_IDS[mesh.operation]
        source.use(0)
        target.use()
        vao.render(mode=mode)
        vertex_buffer.release()
        vao.release()

    def render(self, static_meshes: Iterable[Mesh], dynamic_meshes: Iterable[Mesh]) -> None:
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
