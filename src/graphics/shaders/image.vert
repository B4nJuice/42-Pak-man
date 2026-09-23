#version 330

in vec2 in_position;
in vec2 in_texcoord;

uniform vec2 screen_size;

out vec2 texture_coordinate;

void main() {
    vec2 ndc = in_position / screen_size * 2.0 - 1.0;

    gl_Position = vec4(ndc.x, -ndc.y, 0.0, 1.0);

    texture_coordinate = in_texcoord;
}
