#version 330

uniform sampler2D source_texture;
in vec2 texture_coordinate;
out vec4 fragment_color;

void main() {
    fragment_color = texture(source_texture, texture_coordinate);
}
