#version 450 core

layout (location=0) in vec3 vertexPos;
layout (location=1) in int vertexTilesetOffset;
layout (location=2) in vec4 color_tint;

out VertexData {
    int tilesetOffset;
    vec4 colorTintIn;
} vs_out;

void main()
{
    gl_Position = vec4(vertexPos, 1.0);
    vs_out.tilesetOffset = vertexTilesetOffset;
    vs_out.colorTintIn = color_tint;
}