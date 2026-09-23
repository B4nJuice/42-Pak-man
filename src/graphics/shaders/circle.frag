#version 330

uniform vec4 color;
uniform vec2 center;
uniform float radius;
uniform float thickness;
uniform bool filled;
uniform int height;

out vec4 frag_color;

void main() {
    vec2 pos = gl_FragCoord.xy;

    pos.y = height - pos.y;

    float distance = length(pos - center) + thickness;

    if (filled) {
        if (distance > radius) {
            discard;
        }
    } else {
        float border_distance = abs(distance - radius);

        if (border_distance > thickness / 2.0) {
            discard;
        }
    }

    frag_color = color;
}
