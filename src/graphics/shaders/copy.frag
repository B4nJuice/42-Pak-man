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
