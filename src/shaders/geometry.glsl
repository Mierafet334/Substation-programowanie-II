#version 450 core

layout (points) in;
layout (triangle_strip, max_vertices=4) out;

in VertexData {
    int tilesetOffset;
    vec4 colorTintIn;
} gs_in[];

out GS_OUT {
    vec2 texCoord;
    vec4 colorTint;
} gs_out;

const int REGION_SIZE = 16;
const int TILESET_SIZE = 8;

uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform mat4 modelMatrix;

vec2 offsetToCoords(int offset) {
    float x = mod(offset, TILESET_SIZE) / TILESET_SIZE;
    float y = floor(offset / TILESET_SIZE) / TILESET_SIZE;
    return vec2(x, y);
}

void main() {
    mat4 MVP = projectionMatrix * viewMatrix * modelMatrix;

    gl_Position = MVP * (gl_in[0].gl_Position + vec4(-0.5/REGION_SIZE, -0.5/REGION_SIZE, 0.0, 0.0));
    gs_out.texCoord = offsetToCoords(gs_in[0].tilesetOffset) + vec2(0.0/TILESET_SIZE, 1.0/TILESET_SIZE);
    gs_out.colorTint = gs_in[0].colorTintIn;
    EmitVertex();

    gl_Position = MVP * (gl_in[0].gl_Position + vec4( 0.5/REGION_SIZE, -0.5/REGION_SIZE, 0.0, 0.0));
    gs_out.texCoord = offsetToCoords(gs_in[0].tilesetOffset) + vec2(1.0/TILESET_SIZE, 1.0/TILESET_SIZE);
    gs_out.colorTint = gs_in[0].colorTintIn;
    EmitVertex();

    gl_Position = MVP * (gl_in[0].gl_Position + vec4(-0.5/REGION_SIZE, 0.5/REGION_SIZE, 0.0, 0.0));
    gs_out.texCoord = offsetToCoords(gs_in[0].tilesetOffset) + vec2(0.0/TILESET_SIZE, 0.0/TILESET_SIZE);
    gs_out.colorTint = gs_in[0].colorTintIn;
    EmitVertex();

    gl_Position = MVP * (gl_in[0].gl_Position + vec4( 0.5/REGION_SIZE, 0.5/REGION_SIZE, 0.0, 0.0));
    gs_out.texCoord = offsetToCoords(gs_in[0].tilesetOffset) + vec2(1.0/TILESET_SIZE, 0.0/TILESET_SIZE);
    gs_out.colorTint = gs_in[0].colorTintIn;
    EmitVertex();
    
    EndPrimitive();
} 