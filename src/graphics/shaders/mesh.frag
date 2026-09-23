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
