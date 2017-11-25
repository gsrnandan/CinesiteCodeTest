import PyQt4
import arnold


class ArnoldRender(object):
	""" Arnold Render class to create a render a sphere

	"""
	def __init__(self,sceneName,color):

		self._sceneName = sceneName + "." + 'jpg'
		self._logFile = sceneName + "." + 'log'
		self._color = color

	def renderGeo(self):

		arnold.AiBegin();

		arnold.AiMsgSetLogFileName(self._logFile);
		arnold.AiMsgSetConsoleFlags(arnold.AI_LOG_ALL);
  
		# create a sphere geometric primitive
		sph = arnold.AiNode("sphere");
		arnold.AiNodeSetStr(sph, "name", "mysphere")
		arnold.AiNodeSetVec(sph, "center", 0.0, 4.0, 0.0);
		arnold.AiNodeSetFlt(sph, "radius", 4.0);
  
		# create a red standard shader
		shader1 = arnold.AiNode("standard");
		arnold.AiNodeSetStr(shader1, "name", "myshader1");
		arnold.AiNodeSetRGB(shader1, "Kd_color", self._color[0], self._color[1], self._color[2]);
		arnold.AiNodeSetFlt(shader1, "Ks", 0.05);
  
		# assign the shaders to the geometric objects
		arnold.AiNodeSetPtr(sph, "shader", shader1);
  

		# create a polymesh, with UV coordinates
		mesh = arnold.AiNode("polymesh");
		arnold.AiNodeSetStr(mesh, "name", "mymesh");
		nsides_array = arnold.AiArray(1, 1, arnold.AI_TYPE_UINT, 4);
		arnold.AiNodeSetArray(mesh, "nsides", nsides_array);
		vlist_array = arnold.AiArray(12, 1, arnold.AI_TYPE_FLOAT, -10.0, 0.0, 10.0, 10.0, 0.0, 10.0, -10.0, 0.0, -10.0, 10.0, 0.0, -10.0);
		arnold.AiNodeSetArray(mesh, "vlist", vlist_array);
		vidxs_array = arnold.AiArray(4, 1, arnold.AI_TYPE_UINT, 0, 1, 3, 2);
		arnold.AiNodeSetArray(mesh, "vidxs", vidxs_array);
		uvlist_array = arnold.AiArray(8, 1, arnold.AI_TYPE_FLOAT, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0);
		arnold.AiNodeSetArray(mesh, "uvlist", uvlist_array);
		uvidxs_array = arnold.AiArray(4, 1, arnold.AI_TYPE_UINT, 0, 1, 2, 3);
		arnold.AiNodeSetArray(mesh, "uvidxs", uvidxs_array);

		# create a textured standard shader
		shader2 = arnold.AiNode("standard");
	   	arnold.AiNodeSetStr(shader2, "name", "myshader2");
		arnold.AiNodeSetRGB(shader2, "Kd_color", 1.0, 0.0, 0.0);
	  
	   # create an image shader for texture mapping
		image = arnold.AiNode("image");
		arnold.AiNodeSetStr(image, "name", "myimage");
		arnold.AiNodeSetStr(image, "filename", "scene1.jpg");
		arnold.AiNodeSetFlt(image, "sscale", 4.0);
		arnold.AiNodeSetFlt(image, "tscale", 4.0);
		# link the output of the image shader to the color input of the standard shader
		arnold.AiNodeLink(image, "Kd_color", shader2);


		# create a perspective camera
		camera = arnold.AiNode("persp_camera");
		arnold.AiNodeSetStr(camera, "name", "mycamera");
		# position the camera (alternatively you can set 'matrix')
		arnold.AiNodeSetVec(camera, "position", 0.0, 10.0, 35.0);
		arnold.AiNodeSetVec(camera, "look_at", 0.0, 3.0, 0.0);
		arnold.AiNodeSetFlt(camera, "fov", 45.0);
  
		# create a point light source
		light = arnold.AiNode("point_light");
		arnold.AiNodeSetStr(light, "name", "mylight");
		# // position the light (alternatively use 'matrix')
		arnold.AiNodeSetVec(light, "position", 15.0, 30.0, 15.0);
		arnold.AiNodeSetFlt(light, "intensity", 4500.0); # alternatively, use 'exposure'
		arnold.AiNodeSetFlt(light, "radius", 4.0); # for soft shadows
  
		# // get the global options node and set some options
		options = arnold.AiUniverseGetOptions();
		arnold.AiNodeSetInt(options, "AA_samples", 8);
		arnold.AiNodeSetInt(options, "xres", 480);
		arnold.AiNodeSetInt(options, "yres", 360);
		arnold.AiNodeSetInt(options, "GI_diffuse_depth", 4);
		# // set the active camera (optional, since there is only one camera)
		arnold.AiNodeSetPtr(options, "camera", camera);
  
		 # create an output driver node
		driver = arnold.AiNode("driver_jpeg");
		arnold.AiNodeSetStr(driver, "name", "mydriver");
		arnold.AiNodeSetStr(driver, "filename", self._sceneName);
		arnold.AiNodeSetFlt(driver, "gamma", 2.2);
  
		# create a gaussian filter node
		filter = arnold.AiNode("gaussian_filter");
		arnold.AiNodeSetStr(filter, "name", "myfilter");
  
		# assign the driver and filter to the main (beauty) AOV,
		# which is called "RGBA" and is of type RGBA
		outputs_array = arnold.AiArrayAllocate(1, 1, arnold.AI_TYPE_STRING);
		arnold.AiArraySetStr(outputs_array, 0, "RGBA RGBA myfilter mydriver");
		arnold.AiNodeSetArray(options, "outputs", outputs_array);
  
		# finally, render the image!
		arnold.AiRender(arnold.AI_RENDER_MODE_CAMERA);
	
		# // Arnold session shutdown
		arnold.AiEnd();

	def setColor(self,color):
		self._color = color