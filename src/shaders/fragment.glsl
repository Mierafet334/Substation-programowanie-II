#version 450 core

in GS_OUT {
    vec2 texCoord;
    vec4 colorTint;
} fs_in;

out vec4 color;

uniform sampler2D imageTexture;

void main()
{
    color = texture(imageTexture, fs_in.texCoord) + fs_in.colorTint;
}