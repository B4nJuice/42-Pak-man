#version 330

in vec2 in_position;
out vec2 texture_coordinate;

void main() {
    texture_coordinate = vec2(in_position.x, 1.0 - in_position.y);
    vec2 ndc = in_position * 2.0 - 1.0;
    gl_Position = vec4(ndc.x, -ndc.y, 0.0, 1.0);
}
