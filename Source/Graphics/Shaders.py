from PyQt5.QtCore import QObject
from PyQt5.QtGui import QOpenGLShader, QOpenGLShaderProgram

## singleton shader class 
class Shaders(QObject):

	__instance = None

	def __new__(cls):
		if Shaders.__instance is None:
			Shaders.__instance = QObject.__new__(cls)
			Shaders.__instance.initialize()
		return Shaders.__instance


	def initialize(self):
		"""Create shader programs"""

		## create background shader program
		self.__instance._backgroundShader = QOpenGLShaderProgram()
		self.__instance._backgroundShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeColorNoTransformVertexShader())
		self.__instance._backgroundShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.simpleFragmentShader())
		self.__instance._backgroundShader.link()

		## create uniform material shader with no lighting 
		self.__instance._wireframeMaterialShader = QOpenGLShaderProgram()
		self.__instance._wireframeMaterialShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.wireframeMaterialVertexShader())
		self.__instance._wireframeMaterialShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.simpleFragmentShader())
		self.__instance._wireframeMaterialShader.link()

		## create uniform material shader with no lighting 
		self.__instance._uniformMaterialShader = QOpenGLShaderProgram()
		self.__instance._uniformMaterialShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.uniformMaterialVertexShader())
		self.__instance._uniformMaterialShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.simpleFragmentShader())
		self.__instance._uniformMaterialShader.link()

		## create uniform material with no lighting calculations
		self.__instance._attributeColorShader = QOpenGLShaderProgram()
		self.__instance._attributeColorShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeColorTransformVertexShader())
		self.__instance._attributeColorShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.simpleFragmentShader())
		self.__instance._attributeColorShader.link()

		## create Phong mesh shader
		self.__instance._uniformMaterialPhongShader = QOpenGLShaderProgram()
		self.__instance._uniformMaterialPhongShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.uniformMaterialPhongVertexShader())
		self.__instance._uniformMaterialPhongShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.uniformMaterialPhongFragmentShader())
		self.__instance._uniformMaterialPhongShader.link()

		## create color-based Phong mesh shader
		#AQUI1
		self.__instance._attributeColorPhongShader = QOpenGLShaderProgram()
		self.__instance._attributeColorPhongShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeMaterialPhongVertexShader())
		self.__instance._attributeColorPhongShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.attributeMaterialPhongFragmentShader())
		self.__instance._attributeColorPhongShader.link()

		## create Phong mesh shader
		self.__instance._uniformMaterialPhongFlatShader = QOpenGLShaderProgram()
		self.__instance._uniformMaterialPhongFlatShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.uniformMaterialPhongVertexFlatShader())
		self.__instance._uniformMaterialPhongFlatShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.uniformMaterialPhongFragmentFlatShader())
		self.__instance._uniformMaterialPhongFlatShader.link()

		## create color-based Phong mesh shader
		self.__instance._attributeColorPhongFlatShader = QOpenGLShaderProgram()
		self.__instance._attributeColorPhongFlatShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeMaterialPhongVertexFlatShader())
		self.__instance._attributeColorPhongFlatShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.attributeMaterialPhongFragmentFlatShader())
		self.__instance._attributeColorPhongFlatShader.link()

		## create simple textured-based mesh shader
		self.__instance._texturedShader = QOpenGLShaderProgram()
		self.__instance._texturedShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.texturedVertexShader())
		self.__instance._texturedShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.texturedFragmentShader())
		self.__instance._texturedShader.link()	

		## create simple textured-based mesh flat shader
		self.__instance._texturedFlatShader = QOpenGLShaderProgram()
		self.__instance._texturedFlatShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.texturedVertexFlatShader())
		self.__instance._texturedFlatShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.texturedFragmentFlatShader())
		self.__instance._texturedFlatShader.link()	

		self.__instance._normalVisShader = QOpenGLShaderProgram()
		self.__instance._normalVisShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.normalVisVertexShader())
		self.__instance._normalVisShader.addShaderFromSourceCode(QOpenGLShader.Geometry, Shaders.normalVisGeometryShader())
		self.__instance._normalVisShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.normalVisFragmentShader())
		self.__instance._normalVisShader.link()

		self.__instance._attributeColorPhongTessellationShader = QOpenGLShaderProgram()
		self.__instance._attributeColorPhongTessellationShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeColorTSLVertexShader())
		self.__instance._attributeColorPhongTessellationShader.addShaderFromSourceCode(QOpenGLShader.TessellationControl, Shaders.attributeColorTCS())
		self.__instance._attributeColorPhongTessellationShader.addShaderFromSourceCode(QOpenGLShader.TessellationEvaluation, Shaders.attributeMaterialPhongTES())
		self.__instance._attributeColorPhongTessellationShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.attributeMaterialPhongFragmentShader())
		self.__instance._attributeColorPhongTessellationShader.link()

		## create color-based Phong mesh shader
		self.__instance._attributeColorPhongFlatTessellationShader = QOpenGLShaderProgram()
		self.__instance._attributeColorPhongFlatTessellationShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeColorTSLVertexShader())
		self.__instance._attributeColorPhongFlatTessellationShader.addShaderFromSourceCode(QOpenGLShader.TessellationControl, Shaders.attributeColorTCS())
		self.__instance._attributeColorPhongFlatTessellationShader.addShaderFromSourceCode(QOpenGLShader.TessellationEvaluation, Shaders.attributeMaterialPhongFlatTES())
		self.__instance._attributeColorPhongFlatTessellationShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.attributeMaterialPhongFragmentFlatShader())
		self.__instance._attributeColorPhongFlatTessellationShader.link()

		## create uniform material with no lighting calculations
		self.__instance._attributeColorTessellationShader = QOpenGLShaderProgram()
		self.__instance._attributeColorTessellationShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeColorTSLVertexShader())
		self.__instance._attributeColorTessellationShader.addShaderFromSourceCode(QOpenGLShader.TessellationControl, Shaders.attributeColorTCS())
		self.__instance._attributeColorTessellationShader.addShaderFromSourceCode(QOpenGLShader.TessellationEvaluation, Shaders.attributeColorTransformTES())
		self.__instance._attributeColorTessellationShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.simpleFragmentShader())
		self.__instance._attributeColorTessellationShader.link()

		## create uniform material shader with no lighting tessellation 
		self.__instance._uniformMaterialPhongTessellationShader = QOpenGLShaderProgram()
		self.__instance._uniformMaterialPhongTessellationShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.uniformMaterialTSLVertexShader())
		self.__instance._uniformMaterialPhongTessellationShader.addShaderFromSourceCode(QOpenGLShader.TessellationControl, Shaders.uniformMaterialTCS())
		self.__instance._uniformMaterialPhongTessellationShader.addShaderFromSourceCode(QOpenGLShader.TessellationEvaluation, Shaders.uniformMaterialPhongTES())
		self.__instance._uniformMaterialPhongTessellationShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.uniformMaterialPhongFragmentShader())
		self.__instance._uniformMaterialPhongTessellationShader.link()

		## create Phong mesh shader
		self.__instance._uniformMaterialPhongFlatTessellationShader = QOpenGLShaderProgram()
		self.__instance._uniformMaterialPhongFlatTessellationShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.uniformMaterialTSLVertexShader())
		self.__instance._uniformMaterialPhongFlatTessellationShader.addShaderFromSourceCode(QOpenGLShader.TessellationControl, Shaders.uniformMaterialTCS())
		self.__instance._uniformMaterialPhongFlatTessellationShader.addShaderFromSourceCode(QOpenGLShader.TessellationEvaluation, Shaders.uniformMaterialPhongFlatTES())
		self.__instance._uniformMaterialPhongFlatTessellationShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.uniformMaterialPhongFragmentFlatShader())
		self.__instance._uniformMaterialPhongFlatTessellationShader.link()

		## create uniform material shader with no lighting 
		self.__instance._uniformMaterialTessellationShader = QOpenGLShaderProgram()
		self.__instance._uniformMaterialTessellationShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.uniformMaterialTSLVertexShader())
		self.__instance._uniformMaterialTessellationShader.addShaderFromSourceCode(QOpenGLShader.TessellationControl, Shaders.uniformMaterialTCS())
		self.__instance._uniformMaterialTessellationShader.addShaderFromSourceCode(QOpenGLShader.TessellationEvaluation, Shaders.uniformMaterialTES())
		self.__instance._uniformMaterialTessellationShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.simpleFragmentShader())
		self.__instance._uniformMaterialTessellationShader.link()

	@classmethod
	def attributeColorTSLVertexShader(cls):
		vertexShaderSource = """
		#version 400
		layout(location = 0) in vec3 position;
		layout(location = 2) in vec3 color;

		out vec3 colorCS;
		out vec3 positionCS; 

		void main()
		{
		    positionCS = position;
		    colorCS = color;
		}
		"""
		return vertexShaderSource

	@classmethod
	def attributeColorTCS(cls):
		return """
		#version 400 core
		layout(vertices = 3) out;
		
		in vec3 positionCS[];
		in vec3 colorCS[];

		uniform int innerSubdivisionLevel;
		uniform int outerSubdivisionLevel;

		out vec3 positionES[];
		out vec3 colorES[];

		void main()
		{
			positionES[gl_InvocationID] = positionCS[gl_InvocationID];
			colorES[gl_InvocationID] = colorCS[gl_InvocationID] ;
			gl_TessLevelInner[0] = innerSubdivisionLevel;
			gl_TessLevelOuter[0] = outerSubdivisionLevel;
			gl_TessLevelOuter[1] = outerSubdivisionLevel;
			gl_TessLevelOuter[2] = outerSubdivisionLevel;
		}
		"""

	@classmethod
	def attributeColorTransformTES(cls):
		return """
		#version 400 core
		layout(triangles, equal_spacing, ccw) in;

		const float PI = 3.14159265;

		in vec3 positionES[];
		in vec3 colorES[];

		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform float radius;

		smooth out vec4 vertexColor;


		void main()
		{
			vec3 p0 = gl_TessCoord.x * positionES[0];
			vec3 p1 = gl_TessCoord.y * positionES[1];
			vec3 p2 = gl_TessCoord.z * positionES[2];

			vec3 p = normalize(p0 + p1 + p2) * radius;
			vec3 normal = p / radius;

			float u = 0.5 + (atan(p.z, p.x)) / (2*PI);
			float v = 0.5 + - asin(p.y)/PI;


			gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(p, 1);


			vec3 c0 = gl_TessCoord.x * colorES[0];
			vec3 c1 = gl_TessCoord.y * colorES[1];
			vec3 c2 = gl_TessCoord.z * colorES[2];

			vertexColor = vec4(c0 + c1 + c2, 1.0);
		}
		"""

	@classmethod
	def attributeMaterialPhongTES(cls):
		return """
		#version 400 core
		layout(triangles, equal_spacing, ccw) in;

		const float PI = 3.14159265;

		in vec3 positionES[];
		in vec3 colorES[];

		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform mat3 normalMatrix;
		uniform vec4 lightPosition;
		uniform vec3 lightAttenuation;
		uniform float radius;

		smooth out vec3 vertexColor;

		smooth out vec4 vertexNormal;
		smooth out vec4 vertexPosition;
		smooth out vec3 lightDirection;
		smooth out float attenuation;

		void main()
		{
			vec3 p0 = gl_TessCoord.x * positionES[0];
			vec3 p1 = gl_TessCoord.y * positionES[1];
			vec3 p2 = gl_TessCoord.z * positionES[2];

			vec3 p = normalize(p0 + p1 + p2) * radius;
			vec3 normal = p / radius;

			float u = 0.5 + (atan(p.z, p.x)) / (2*PI);
			float v = 0.5 + - asin(p.y)/PI;

			vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
			vertexPosition = vec4(p, 1);

			if (lightPosition.w == 0.0) {
				lightDirection = normalize(lightPosition.xyz);
				attenuation = 1.0;
			} else {
		    	lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
		    	float distance = length(lightPosition.xyz - vertexPosition.xyz);
		    	attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
		    }

			gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(p, 1);


			vec3 c0 = gl_TessCoord.x * colorES[0];
			vec3 c1 = gl_TessCoord.y * colorES[1];
			vec3 c2 = gl_TessCoord.z * colorES[2];

			vertexColor = c0 + c1 + c2;
		}
		"""

	@classmethod
	def attributeMaterialPhongFlatTES(cls):
		return """
		#version 400 core
		layout(triangles, equal_spacing, ccw) in;

		const float PI = 3.14159265;

		in vec3 positionES[];
		in vec3 colorES[];

		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform mat3 normalMatrix;
		uniform vec4 lightPosition;
		uniform vec3 lightAttenuation;
		uniform float radius;

		smooth out vec3 vertexColor;

		flat out vec4 vertexNormal;
		smooth out vec4 vertexPosition;
		smooth out vec3 lightDirection;
		smooth out float attenuation;

		void main()
		{
			vec3 p0 = gl_TessCoord.x * positionES[0];
			vec3 p1 = gl_TessCoord.y * positionES[1];
			vec3 p2 = gl_TessCoord.z * positionES[2];

			vec3 v = normalize(p0 + p1 + p2) * radius;
			vec3 normal = v / radius;

			float s = 0.5 + (atan(v.z, v.x)) / (2*PI);
			float t = 0.5 + - asin(v.y)/PI;

			vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);

			vertexPosition = vec4(v, 1);

			if (lightPosition.w == 0.0) {
				lightDirection = normalize(lightPosition.xyz);
				attenuation = 1.0;
			} else {
		    	lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
		    	float distance = length(lightPosition.xyz - vertexPosition.xyz);
		    	attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
		    }

			gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(v, 1);


			vec3 c0 = gl_TessCoord.x * colorES[0];
			vec3 c1 = gl_TessCoord.y * colorES[1];
			vec3 c2 = gl_TessCoord.z * colorES[2];

			vertexColor = c0 + c1 + c2;
		}
		"""

#sem cor
	@classmethod
	def uniformMaterialTSLVertexShader(cls):
		vertexShaderSource = """
		#version 400
		layout(location = 0) in vec3 position;

		out vec3 positionCS; 

		void main()
		{
		    positionCS = position;
		}
		"""
		return vertexShaderSource

	@classmethod
	def uniformMaterialTCS(cls):
		return """
		#version 400 core
		layout(vertices = 3) out;
		
		in vec3 positionCS[];

		uniform int innerSubdivisionLevel;
		uniform int outerSubdivisionLevel;

		out vec3 positionES[];

		void main()
		{
			positionES[gl_InvocationID] = positionCS[gl_InvocationID];
			gl_TessLevelInner[0] = innerSubdivisionLevel;
			gl_TessLevelOuter[0] = outerSubdivisionLevel;
			gl_TessLevelOuter[1] = outerSubdivisionLevel;
			gl_TessLevelOuter[2] = outerSubdivisionLevel;
		}
		"""

	@classmethod
	def uniformMaterialTES(cls):
		return """
		#version 400 core
		layout(triangles, equal_spacing, ccw) in;

		const float PI = 3.14159265;

		struct Material {
			vec3 emission;
			vec3 ambient;
			vec3 diffuse;
			vec3 specular;    
			float shininess;
		}; 

		in vec3 positionES[];
		in vec3 colorES[];

		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform float radius;
		uniform Material material;

		smooth out vec4 vertexColor;

		void main()
		{
			vec3 p0 = gl_TessCoord.x * positionES[0];
			vec3 p1 = gl_TessCoord.y * positionES[1];
			vec3 p2 = gl_TessCoord.z * positionES[2];

			vec3 v = normalize(p0 + p1 + p2) * radius;
			vec3 normal = v / radius;

			float s = 0.5 + (atan(v.z, v.x)) / (2*PI);
			float t = 0.5 + - asin(v.y)/PI;
			
			gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(v, 1);
			vertexColor = vec4(material.diffuse, 1.0);

		}
		"""

	@classmethod
	def uniformMaterialPhongTES(cls):
		return """
		#version 400 core
		layout(triangles, equal_spacing, ccw) in;

		const float PI = 3.14159265;

		in vec3 positionES[];
		in vec3 colorES[];

		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform mat3 normalMatrix;
		uniform vec4 lightPosition;
		uniform vec3 lightAttenuation;
		uniform float radius;


		smooth out vec4 vertexNormal;
		smooth out vec4 vertexPosition;
		smooth out vec3 lightDirection;
		smooth out float attenuation;

		void main()
		{
			vec3 p0 = gl_TessCoord.x * positionES[0];
			vec3 p1 = gl_TessCoord.y * positionES[1];
			vec3 p2 = gl_TessCoord.z * positionES[2];

			vec3 v = normalize(p0 + p1 + p2) * radius;
			vec3 normal = v / radius;
			vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);

			float s = 0.5 + (atan(v.z, v.x)) / (2*PI);
			float t = 0.5 + - asin(v.y)/PI;

			vertexPosition = vec4(v, 1);

			if (lightPosition.w == 0.0) {
				lightDirection = normalize(lightPosition.xyz);
				attenuation = 1.0;
			} else {
		    	lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
		    	float distance = length(lightPosition.xyz - vertexPosition.xyz);
		    	attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
		    }

			gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(v, 1);

		}
		"""

	@classmethod
	def uniformMaterialPhongFlatTES(cls):
		return """
		#version 400 core
		layout(triangles, equal_spacing, ccw) in;

		const float PI = 3.14159265;

		in vec3 positionES[];
		in vec3 colorES[];

		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform mat3 normalMatrix;
		uniform vec4 lightPosition;
		uniform vec3 lightAttenuation;
		uniform float radius;


		flat out vec4 vertexNormal;
		smooth out vec4 vertexPosition;
		smooth out vec3 lightDirection;
		smooth out float attenuation;

		void main()
		{
			vec3 p0 = gl_TessCoord.x * positionES[0];
			vec3 p1 = gl_TessCoord.y * positionES[1];
			vec3 p2 = gl_TessCoord.z * positionES[2];

			vec3 v = normalize(p0 + p1 + p2) * radius;
			vec3 normal = v / radius;
			vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);

			float s = 0.5 + (atan(v.z, v.x)) / (2*PI);
			float t = 0.5 + - asin(v.y)/PI;

			vertexPosition = vec4(v, 1);

			if (lightPosition.w == 0.0) {
				lightDirection = normalize(lightPosition.xyz);
				attenuation = 1.0;
			} else {
		    	lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
		    	float distance = length(lightPosition.xyz - vertexPosition.xyz);
		    	attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
		    }

			gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(v, 1);

		}
		"""

	
#no tessellation
	@classmethod
	def uniformMaterialPhongVertexFlatShader(cls):
		vertexShaderSource = """
		#version 400
		layout(location = 0) in vec3 position;
		layout(location = 1) in vec3 normal;
		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform mat3 normalMatrix;
		uniform vec4 lightPosition;
		uniform vec3 lightAttenuation;

		flat out vec4 vertexNormal;
		smooth out vec4 vertexPosition;
		smooth out vec3 lightDirection;
		smooth out float attenuation;

		void main()
		{
		    vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
		    vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
		    if (lightPosition.w == 0.0) {
				lightDirection = normalize(lightPosition.xyz);
				attenuation = 1.0;
			} else {
		    	lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
		    	float distance = length(lightPosition.xyz - vertexPosition.xyz);
		    	attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
		    }
		    gl_Position = projectionMatrix * vertexPosition;
		}
		"""
		return vertexShaderSource


	@classmethod
	def uniformMaterialPhongFragmentFlatShader(cls):
		fragmentShaderSource = """
		#version 400
		struct Material {
			vec3 emission;
			vec3 ambient;
			vec3 diffuse;
			vec3 specular;    
			float shininess;
		}; 

		struct Light {
			vec3 ambient;
			vec3 diffuse;
			vec3 specular;
		};

		flat in vec4 vertexNormal;
		smooth in vec4 vertexPosition;
		smooth in vec3 lightDirection;
		smooth in float attenuation;

		uniform Material material;
		uniform Light light;

		out vec4 fragColor;

		void main()
		{
			// ambient term
			vec3 ambient = material.ambient * light.ambient;

			// diffuse term
			vec3 N = normalize(vertexNormal.xyz);
			vec3 L = normalize(lightDirection);
			vec3 diffuse = light.diffuse * material.diffuse * max(dot(N, L), 0.0);

			// specular term
			vec3 E = normalize(-vertexPosition.xyz);
	 		vec3 R = normalize(-reflect(L, N)); 
			vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

			// final intensity
			vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
			fragColor = vec4(intensity, 1.0);
		}
		"""
		return fragmentShaderSource


	@classmethod
	def attributeMaterialPhongVertexFlatShader(cls):
		vertexShaderSource = """
		#version 400
		layout(location = 0) in vec3 position;
		layout(location = 1) in vec3 normal;
		layout(location = 2) in vec3 color;
		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform mat3 normalMatrix;
		uniform vec4 lightPosition;
		uniform vec3 lightAttenuation;

		flat out vec4 vertexNormal;
		smooth out vec4 vertexPosition;
		smooth out vec3 lightDirection;
		smooth out float attenuation;
		smooth out vec3 vertexColor;

		void main()
		{
		    vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
		    vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
		    if (lightPosition.w == 0.0) {
				lightDirection = normalize(lightPosition.xyz);
				attenuation = 1.0;
			} else {
		    	lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
		    	float distance = length(lightPosition.xyz - vertexPosition.xyz);
		    	attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
		    }
		    vertexColor = color;
		    gl_Position = projectionMatrix * vertexPosition;
		}
		"""
		return vertexShaderSource


	@classmethod
	def attributeMaterialPhongFragmentFlatShader(cls):
		fragmentShaderSource = """
		#version 400
		struct Material {
			vec3 emission;
			vec3 ambient;
			vec3 diffuse;
			vec3 specular;    
			float shininess;
		}; 

		struct Light {
			vec3 ambient;
			vec3 diffuse;
			vec3 specular;
		};

		flat in vec4 vertexNormal;
		smooth in vec4 vertexPosition;
		smooth in vec3 lightDirection;
		smooth in float attenuation;
		smooth in vec3 vertexColor;

		uniform Material material;
		uniform Light light;

		out vec4 fragColor;

		void main()
		{
			// ambient term
			vec3 ambient = material.ambient * light.ambient;

			// diffuse term
			vec3 N = normalize(vertexNormal.xyz);
			vec3 L = normalize(lightDirection);
			vec3 diffuse = light.diffuse * vertexColor * max(dot(N, L), 0.0);

			// specular term
			vec3 E = normalize(-vertexPosition.xyz);
	 		vec3 R = normalize(-reflect(L, N)); 
			vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

			// final intensity
			vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
			fragColor = vec4(intensity, 1.0);
		}
		"""
		return fragmentShaderSource
		

	@classmethod
	def uniformMaterialPhongVertexShader(cls):
		vertexShaderSource = """
		#version 400
		layout(location = 0) in vec3 position;
		layout(location = 1) in vec3 normal;
		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform mat3 normalMatrix;
		uniform vec4 lightPosition;
		uniform vec3 lightAttenuation;

		smooth out vec4 vertexNormal;
		smooth out vec4 vertexPosition;
		smooth out vec3 lightDirection;
		smooth out float attenuation;

		void main()
		{
		    vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
		    vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
		    if (lightPosition.w == 0.0) {
				lightDirection = normalize(lightPosition.xyz);
				attenuation = 1.0;
			} else {
		    	lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
		    	float distance = length(lightPosition.xyz - vertexPosition.xyz);
		    	attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
		    }
		    gl_Position = projectionMatrix * vertexPosition;
		}
		"""
		return vertexShaderSource


	@classmethod
	def uniformMaterialPhongFragmentShader(cls):
		fragmentShaderSource = """
		#version 400
		struct Material {
			vec3 emission;
			vec3 ambient;
			vec3 diffuse;
			vec3 specular;    
			float shininess;
		}; 

		struct Light {
			vec3 ambient;
			vec3 diffuse;
			vec3 specular;
		};

		smooth in vec4 vertexNormal;
		smooth in vec4 vertexPosition;
		smooth in vec3 lightDirection;
		smooth in float attenuation;

		uniform Material material;
		uniform Light light;

		out vec4 fragColor;

		void main()
		{
			// ambient term
			vec3 ambient = material.ambient * light.ambient;

			// diffuse term
			vec3 N = normalize(vertexNormal.xyz);
			vec3 L = normalize(lightDirection);
			vec3 diffuse = light.diffuse * material.diffuse * max(dot(N, L), 0.0);

			// specular term
			vec3 E = normalize(-vertexPosition.xyz);
	 		vec3 R = normalize(-reflect(L, N)); 
			vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

			// final intensity
			vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
			fragColor = vec4(intensity, 1.0);
		}
		"""
		return fragmentShaderSource


	@classmethod
	def attributeMaterialPhongVertexShader(cls):
		vertexShaderSource = """
		#version 400
		layout(location = 0) in vec3 position;
		layout(location = 1) in vec3 normal;
		layout(location = 2) in vec3 color;
		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform mat3 normalMatrix;
		uniform vec4 lightPosition;
		uniform vec3 lightAttenuation;

		smooth out vec4 vertexNormal;
		smooth out vec4 vertexPosition;
		smooth out vec3 lightDirection;
		smooth out float attenuation;
		smooth out vec3 vertexColor;

		void main()
		{
		    vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
		    vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
		    if (lightPosition.w == 0.0) {
				lightDirection = normalize(lightPosition.xyz);
				attenuation = 1.0;
			} else {
		    	lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
		    	float distance = length(lightPosition.xyz - vertexPosition.xyz);
		    	attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
		    }
		    vertexColor = color;
		    gl_Position = projectionMatrix * vertexPosition;
		}
		"""
		return vertexShaderSource


	@classmethod
	def attributeMaterialPhongFragmentShader(cls):
		fragmentShaderSource = """
		#version 400
		struct Material {
			vec3 emission;
			vec3 ambient;
			vec3 diffuse;
			vec3 specular;    
			float shininess;
		}; 

		struct Light {
			vec3 ambient;
			vec3 diffuse;
			vec3 specular;
		};

		smooth in vec4 vertexNormal;
		smooth in vec4 vertexPosition;
		smooth in vec3 lightDirection;
		smooth in float attenuation;
		smooth in vec3 vertexColor;

		uniform Material material;
		uniform Light light;

		out vec4 fragColor;

		void main()
		{
			// ambient term
			vec3 ambient = material.ambient * light.ambient;

			// diffuse term
			vec3 N = normalize(vertexNormal.xyz);
			vec3 L = normalize(lightDirection);
			vec3 diffuse = light.diffuse * vertexColor * max(dot(N, L), 0.0);

			// specular term
			vec3 E = normalize(-vertexPosition.xyz);
	 		vec3 R = normalize(-reflect(L, N)); 
			vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

			// final intensity
			vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
			fragColor = vec4(intensity, 1.0);
		}
		"""
		return fragmentShaderSource


	@classmethod
	def attributeColorNoTransformVertexShader(cls):
		vertexShaderSource = """
		#version 400
		layout(location = 0) in vec3 position;
		layout(location = 2) in vec3 color;
		smooth out vec4 vertexColor;

		void main()
		{
			gl_Position = vec4(position, 1.0);
			vertexColor = vec4(color, 1.0);
		}
		"""
		return vertexShaderSource


	@classmethod
	def uniformMaterialVertexShader(cls):
		vertexShaderSource = """
		#version 400
		
		struct Material {
			vec3 emission;
			vec3 ambient;
			vec3 diffuse;
			vec3 specular;    
			float shininess;
		}; 

		layout(location = 0) in vec3 position;
		
		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform Material material;

		smooth out vec4 vertexColor;

		void main()
		{
		    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
		    vertexColor = vec4(material.diffuse, 1.0);
		}
		"""
		return vertexShaderSource


	@classmethod
	def texturedVertexShader(cls):
		vertexShaderSource = """
		#version 400
		layout(location = 0) in vec3 position;
		layout(location = 1) in vec3 normal;
		layout(location = 2) in vec3 color;
		layout(location = 3) in vec2 texcoord;
		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform mat3 normalMatrix;
		uniform vec4 lightPosition;
		uniform vec3 lightAttenuation;

		smooth out vec4 vertexNormal;
		smooth out vec4 vertexPosition;
		smooth out vec3 lightDirection;
		smooth out float attenuation;
		smooth out vec2 textureCoord;

		void main()
		{
		    vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
		    vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
		    if (lightPosition.w == 0.0) {
				lightDirection = normalize(lightPosition.xyz);
				attenuation = 1.0;
			} else {
		    	lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
		    	float distance = length(lightPosition.xyz - vertexPosition.xyz);
		    	attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
		    }
		    textureCoord = texcoord;
		    gl_Position = projectionMatrix * vertexPosition;
		}
		"""
		return vertexShaderSource


	@classmethod
	def texturedVertexFlatShader(cls):
		vertexShaderSource = """
		#version 400
		layout(location = 0) in vec3 position;
		layout(location = 1) in vec3 normal;
		layout(location = 2) in vec3 color;
		layout(location = 3) in vec2 texcoord;
		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform mat3 normalMatrix;
		uniform vec4 lightPosition;
		uniform vec3 lightAttenuation;

		flat out vec4 vertexNormal;
		smooth out vec4 vertexPosition;
		smooth out vec3 lightDirection;
		smooth out float attenuation;
		smooth out vec2 textureCoord;

		void main()
		{
		    vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
		    vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
		    if (lightPosition.w == 0.0) {
				lightDirection = normalize(lightPosition.xyz);
				attenuation = 1.0;
			} else {
		    	lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
		    	float distance = length(lightPosition.xyz - vertexPosition.xyz);
		    	attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
		    }
		    textureCoord = texcoord;
		    gl_Position = projectionMatrix * vertexPosition;
		}
		"""
		return vertexShaderSource


	@classmethod
	def wireframeMaterialVertexShader(cls):
		vertexShaderSource = """
		#version 400
		
		struct Material {
			vec3 emission;
			vec3 ambient;
			vec3 diffuse;
			vec3 specular;    
			float shininess;
		}; 

		layout(location = 0) in vec3 position;
		
		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform Material wireframe_material;

		smooth out vec4 vertexColor;

		void main()
		{
		    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
		    vertexColor = vec4(wireframe_material.diffuse, 1.0);
		}
		"""
		return vertexShaderSource


	@classmethod
	def attributeColorTransformVertexShader(cls):
		vertexShaderSource = """
		#version 400
		layout(location = 0) in vec3 position;
		layout(location = 2) in vec3 color;
		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		smooth out vec4 vertexColor;

		void main()
		{
		    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
		    vertexColor = vec4(color, 1.0);
		}
		"""
		return vertexShaderSource


	@classmethod
	def simpleFragmentShader(cls):
		fragmentShaderSource = """
		#version 400
		smooth in vec4 vertexColor;
		out vec4 fragColor;

		void main()
		{
			fragColor = vertexColor;
		}
		"""
		return fragmentShaderSource


	@classmethod
	def texturedFragmentShader(cls):
		fragmentShaderSource = """
		#version 400
		struct Material {
			vec3 emission;
			vec3 ambient;
			vec3 diffuse;
			vec3 specular;    
			float shininess;
		}; 

		struct Light {
			vec3 ambient;
			vec3 diffuse;
			vec3 specular;
		};

		smooth in vec4 vertexNormal;
		smooth in vec4 vertexPosition;
		smooth in vec3 lightDirection;
		smooth in float attenuation;
		smooth in vec2 textureCoord;

		uniform float selected;
		uniform sampler2D texObject;
		uniform Material material;
		uniform Light light;

		out vec4 fragColor;

		void main()
		{
			// ambient term
			vec3 ambient = material.ambient * light.ambient;

			// diffuse term
			vec3 N = normalize(vertexNormal.xyz);
			vec3 L = normalize(lightDirection);
			vec3 diffuse = light.diffuse * material.diffuse * max(dot(N, L), 0.0);

			// specular term
			vec3 E = normalize(-vertexPosition.xyz);
	 		vec3 R = normalize(-reflect(L, N)); 
			vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

			// final intensity
			vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
			vec4 tex = texture(texObject, textureCoord.st);
			fragColor = (1.0 - tex.a) * vec4(intensity, 1.0) + tex.a * vec4(selected * tex.rgb, 1.0);
		}
		"""
		return fragmentShaderSource


	@classmethod
	def texturedFragmentFlatShader(cls):
		fragmentShaderSource = """
		#version 400
		struct Material {
			vec3 emission;
			vec3 ambient;
			vec3 diffuse;
			vec3 specular;    
			float shininess;
		}; 

		struct Light {
			vec3 ambient;
			vec3 diffuse;
			vec3 specular;
		};

		flat in vec4 vertexNormal;
		smooth in vec4 vertexPosition;
		smooth in vec3 lightDirection;
		smooth in float attenuation;
		smooth in vec2 textureCoord;

		uniform float selected;
		uniform sampler2D texObject;
		uniform Material material;
		uniform Light light;

		out vec4 fragColor;

		void main()
		{
			// ambient term
			vec3 ambient = material.ambient * light.ambient;

			// diffuse term
			vec3 N = normalize(vertexNormal.xyz);
			vec3 L = normalize(lightDirection);
			vec3 diffuse = light.diffuse * material.diffuse * max(dot(N, L), 0.0);

			// specular term
			vec3 E = normalize(-vertexPosition.xyz);
	 		vec3 R = normalize(-reflect(L, N)); 
			vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

			// final intensity
			vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
			vec4 tex = texture(texObject, textureCoord.st);
			fragColor = (1.0 - tex.a) * vec4(intensity, 1.0) + tex.a * vec4(selected * tex.rgb, 1.0);
		}
		"""
		return fragmentShaderSource

	@classmethod
	def normalVisVertexShader(cls):
		return """
		#version 400
		layout(location = 0) in vec3 position;
		layout(location = 1) in vec3 normal;
		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform mat3 normalMatrix;

		out vec3 vertexNormal;
		out vec3 vertexPosition;

		void main() 
		{
			gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
			vertexPosition = position;
			vertexNormal = normal;
		}
		"""

	# @classmethod
	# def normalVisGeometryShader(cls):
	# 	return """
	# 	#version 400 core
	# 	layout (triangles) in;
	# 	layout (line_strip, max_vertices = 6) out;

	# 	uniform mat4 modelMatrix;
	# 	uniform mat4 viewMatrix;
	# 	uniform mat4 projectionMatrix;
	# 	uniform mat3 normalMatrix;

	# 	in vec3 vertexNormal[];
	# 	in vec3 vertexPosition[];

	# 	const float MAGNITUDE = 0.4;

	# 	void GenerateLine(int index)
	# 	{
	# 	    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition[index], 1.0);
	# 	    EmitVertex();
	# 	    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition[index] 
	# 	    	+ vertexNormal[index] * MAGNITUDE, 1.0);
	# 	    EmitVertex();
	# 	    EndPrimitive();
	# 	}

	# 	void main()
	# 	{
	# 	    GenerateLine(0); // first vertex normal
	# 	    GenerateLine(1); // second vertex normal
	# 	    GenerateLine(2); // third vertex normal
	# 	}  
	# 	"""

	@classmethod
	def normalVisGeometryShader(cls):
		return """
		#version 400
		layout(triangles) in;
		layout(line_strip, max_vertices = 4) out;

		in vec3 vertexNormal[];
		in vec3 vertexPosition[];

		const float a = 0.33;
		const float b = 0.33;
		const float c = 0.33;

		const float MAGNITUDE = 0.4;

		uniform mat4 modelMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 projectionMatrix;
		uniform mat3 normalMatrix;

		void main()
		{
			vec3 p0 = a*vertexPosition[0];
			vec3 p1 = b*vertexPosition[1];
			vec3 p2 = c*vertexPosition[2];
			vec3 p = p0 + p1 + p2;

			vec3 n0 = a * normalize(vertexNormal[0]);
			vec3 n1 = b * normalize(vertexNormal[1]);
			vec3 n2 = c * normalize(vertexNormal[2]);
			vec3 n = n0 + n1 + n2;

			gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(p, 1.0);
			EmitVertex();
			gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(p+n*MAGNITUDE, 1.0);
			EmitVertex();
			EndPrimitive();
		}"""

	@classmethod
	def normalVisFragmentShader(cls):
		return """
		#version 400
		out vec4 fragColor;
		void main() {
			fragColor = vec4(1.0, 1.0, 0.0, 1.0);
		}"""

	def backgroundShader(self):
		return self.__instance._backgroundShader

	def uniformMaterialShader(self):
		return self.__instance._uniformMaterialShader

	def wireframeMaterialShader(self):
		return self.__instance._wireframeMaterialShader

	def attributeColorShader(self):
		return self.__instance._attributeColorShader
		
	def uniformMaterialPhongShader(self):
		return self.__instance._uniformMaterialPhongShader

	def attributeColorPhongShader(self):
		return self.__instance._attributeColorPhongShader

	def uniformMaterialPhongFlatShader(self):
		return self.__instance._uniformMaterialPhongFlatShader

	def attributeColorPhongFlatShader(self):
		return self.__instance._attributeColorPhongFlatShader
		
	def texturedShader(self):
		return self.__instance._texturedShader

	def texturedFlatShader(self):
		return self.__instance._texturedFlatShader

	def normalVisShader(self):
		return self.__instance._normalVisShader

	def attributeColorPhongTessellationShader(self):
		return self.__instance._attributeColorPhongTessellationShader

	def uniformMaterialPhongTessellationShader(self):
		return self.__instance._uniformMaterialPhongTessellationShader

	def attributeColorPhongFlatTessellationShader(self):
		return self.__instance._attributeColorPhongFlatTessellationShader

	def attributeColorTessellationShader(self):
		return self.__instance._attributeColorTessellationShader

	def uniformMaterialPhongFlatTessellationShader(self):
		return self.__instance._uniformMaterialPhongFlatTessellationShader
	
	def uniformMaterialTessellationShader(self):
		return self.__instance._uniformMaterialTessellationShader
