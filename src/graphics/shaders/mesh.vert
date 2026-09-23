#version 330

in vec2 in_position;
uniform vec2 screen_size;

void main() {
    vec2 ndc = in_position / screen_size * 2.0 - 1.0;
    gl_Position = vec4(ndc.x, -ndc.y, 0.0, 1.0);
}
