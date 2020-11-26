#version 130
out vec4 color;
in vec3 fCor;
void main(){

  color = vec4(fCor,1);
  
}
