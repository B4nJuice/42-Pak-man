#version 330

uniform sampler2D image_texture;
uniform sampler2D previous_frame;
uniform int operation;

in vec2 texture_coordinate;

out vec4 fragment_color;

void main() {
    vec4 texture_color = texture(image_texture, texture_coordinate);
    vec4 color = texture_color;

    vec4 background = texelFetch(
        previous_frame,
        ivec2(gl_FragCoord.xy),
        0
    );

    if (background.a > 0.0) {
        if (operation == 1) {
            color = min(background + texture_color, 1.0);
        } else if (operation == 2) {
            color = max(background - texture_color, 0.0);
        } else if (operation == 3) {
            color = background * texture_color;
        } else if (operation == 4) {
            color.rgb = vec3(
                texture_color.r == 0.0 ? 1.0 : background.r / texture_color.r,
                texture_color.g == 0.0 ? 1.0 : background.g / texture_color.g,
                texture_color.b == 0.0 ? 1.0 : background.b / texture_color.b
            );
        } else if (operation == 5) {
            color = min(background, texture_color);
        } else if (operation == 6) {
            color = max(background, texture_color);
        } else if (operation == 7) {
            color = (background + texture_color) * 0.5;
        } else if (operation == 8) {
            color = 1.0 - (1.0 - background) * (1.0 - texture_color);
        } else if (operation == 9) {
            color = abs(background - texture_color);
        } else if (operation == 10) {
            color = 1.0 - texture_color;
        } else if (operation == 11) {
            color = mix(background, texture_color, texture_color.a);
        }
    }

    if (color.a <= 0.0) {
        discard;
    }

    fragment_color = color;
}
