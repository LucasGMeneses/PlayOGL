#version 130

uniform vec3 fColor;

uniform vec3 lightPos;
uniform vec3 viewPos;

uniform float ambientStrength;
uniform float difuseStregth;
uniform float specularStregth;

in vec3 normal;
in vec3 fPos;
out vec4 color;

void main(){
  vec3 lightColor = vec3(1,1,1); // cor da luz padrao
  // luz ambiente
  vec3 ambient = ambientStrength * lightColor;
  
  
  // luz difusa
  vec3 norm = normalize(normal);
  vec3 lightDir = normalize(lightPos-fPos);
  float diff = max(dot(norm,lightDir),0.0);
  vec3 difuse = diff * lightColor * difuseStregth;
  
  // luz especular

  vec3 viewDir = (viewPos - fPos);
  vec3 reflectDir = reflect(-lightDir, norm);
  float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
  vec3 specular = specularStregth * spec * lightColor;

  vec3 result = (ambient + difuse + specular) * fColor;
  color = vec4(result, 1.0);
}
