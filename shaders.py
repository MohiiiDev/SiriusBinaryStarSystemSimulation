
STAR_VERTEX_SHADER = """
#version 330

in vec3 in_position;

uniform mat4 view;
uniform mat4 projection;
uniform float star_radius;
uniform float star_screen_size_multiplier;
uniform float star_screen_size_min;
uniform float star_screen_size_max;

void main() {
    vec4 view_pos = view * vec4(in_position, 1.0);
    gl_Position = projection * view_pos;

    gl_PointSize = clamp(
        star_radius * star_screen_size_multiplier,
        star_screen_size_min,
        star_screen_size_max
    );
}
"""

STAR_FRAGMENT_SHADER = """
#version 330

uniform vec3 star_color;
uniform float glow_intensity;

out vec4 frag_color;

void main() {
    vec2 p = gl_PointCoord * 2.0 - 1.0;
    float r = length(p);

    if (r > 1.0) {
        discard;
    }

    float core = 1.0 - smoothstep(0.12, 0.38, r);
    float inner_glow = exp(-r * r * 4.0);
    float outer_glow = exp(-r * r * 1.8);

    vec3 color = star_color * (
        core * 2.5
        + inner_glow * glow_intensity
        + outer_glow * glow_intensity * 0.45
    );

    float alpha = clamp(
        core + inner_glow * 0.55 + outer_glow * 0.2,
        0.0,
        1.0
    );

    frag_color = vec4(color, alpha);
}
"""

LINE_VERTEX_SHADER = """
#version 330

in vec3 in_position;

uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = projection * view * vec4(in_position, 1.0);
}
"""

LINE_FRAGMENT_SHADER = """
#version 330

uniform vec3 line_color;
uniform float opacity;

out vec4 frag_color;

void main() {
    frag_color = vec4(line_color, opacity);
}
"""