#version 330

uniform sampler2D source_texture;
uniform vec2 logical_size;
uniform vec2 window_size;
uniform int scaling_mode;
in vec2 texture_coordinate;
out vec4 fragment_color;

void main() {
    vec2 screen_coordinate = vec2(
        gl_FragCoord.x / window_size.x,
        gl_FragCoord.y / window_size.y
    );
    vec2 logical_aspect = logical_size / logical_size.x;
    vec2 window_aspect = window_size / window_size.x;
    vec2 content_size = vec2(1.0);

    if (scaling_mode == 1) {
        content_size = vec2(
            min(window_aspect.x / logical_aspect.x,
                window_aspect.y / logical_aspect.y)
        ) * logical_aspect / window_aspect;
    } else if (scaling_mode == 2) {
        content_size = vec2(
            max(window_aspect.x / logical_aspect.x,
                window_aspect.y / logical_aspect.y)
        ) * logical_aspect / window_aspect;
    }

    vec2 content_coordinate = (
        screen_coordinate - (vec2(1.0) - content_size) / 2.0
    ) / content_size;
    if (scaling_mode == 1
        && (content_coordinate.x < 0.0 || content_coordinate.x > 1.0
            || content_coordinate.y < 0.0 || content_coordinate.y > 1.0)) {
        fragment_color = vec4(0.0, 0.0, 0.0, 1.0);
        return;
    }

    fragment_color = texture(source_texture, content_coordinate);
}
