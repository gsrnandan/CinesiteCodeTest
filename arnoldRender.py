import os

import PyQt4
import arnold


class ArnoldRender(object):
	""" Arnold Render class to create a render a sphere

	"""
	def __init__(self, sceneName, color, imageType=None, path=None):


		self._sceneName = sceneName
		self._imageType = imageType or "jpg"
		self._path = path or os.getcwd()
		# self._logFile = sceneName + "." + 'log'
		self._color = color

	@property
	def image(self):
		imageName = "%s.%s" % (self._sceneName, self._imageType)
		return os.path.join(self._path, imageName)

	@property
	def log(self):
		logName = "%s.log" % self._sceneName
		return os.path.join(self._path, logName)

	def renderGeo(self):
		""" This method calls the arnold functions to setup and scene and render the image
		"""

		arnold.AiBegin()

		arnold.AiMsgSetLogFileName(self.log)
		arnold.AiMsgSetConsoleFlags(arnold.AI_LOG_ALL)
  
   		# create a sphere geometric primitive
		sph = arnold.AiNode("sphere")
		arnold.AiNodeSetStr(sph, "name", "mysphere")
		arnold.AiNodeSetVec(sph, "center", 0.0, 4.0, 0.0)
		arnold.AiNodeSetFlt(sph, "radius", 5.0)
  
   		# create a red standard shader
		shader1 = arnold.AiNode("standard")
		arnold.AiNodeSetStr(shader1, "name", "myshader1")
		arnold.AiNodeSetRGB(shader1, "Kd_color", self._color[0], self._color[1], self._color[2])
		arnold.AiNodeSetFlt(shader1, "Ks", 0.05)
  
		# assign the shaders to the geometric objects
		arnold.AiNodeSetPtr(sph, "shader", shader1)
  
 		# create a perspective camera
		camera = arnold.AiNode("persp_camera")
		arnold.AiNodeSetStr(camera, "name", "mycamera")
		arnold.AiNodeSetVec(camera, "position", 0.0, 10.0, 35.0)
		arnold.AiNodeSetVec(camera, "look_at", 0.0, 3.0, 0.0)
		arnold.AiNodeSetFlt(camera, "fov", 45.0)
  
   		# create a point light source
		light = arnold.AiNode("point_light")
		arnold.AiNodeSetStr(light, "name", "pointLight_A")
		arnold.AiNodeSetVec(light, "position", 0.0, 30.0, 0.0)
		arnold.AiNodeSetFlt(light, "intensity", 10.0) 
		arnold.AiNodeSetFlt(light, "radius", 4.0) 
  
   		# create a point light source
		light = arnold.AiNode("point_light")
		arnold.AiNodeSetStr(light, "name", "pointLight_B")
		arnold.AiNodeSetVec(light, "position", 0.0, -30.0, 0.0)
		arnold.AiNodeSetFlt(light, "intensity", 10.0) 
		arnold.AiNodeSetFlt(light, "radius", 4.0) 

		# create a point light source
		light = arnold.AiNode("point_light")
		arnold.AiNodeSetStr(light, "name", "pointLight_C")
		arnold.AiNodeSetVec(light, "position", 0.0, 4.0, 20.0)
		arnold.AiNodeSetFlt(light, "intensity", 5.0)
		arnold.AiNodeSetFlt(light, "radius", 15.0) 


 		# get the global options node and set some options
		options = arnold.AiUniverseGetOptions()
		arnold.AiNodeSetInt(options, "AA_samples", 8)
		arnold.AiNodeSetInt(options, "xres", 480)
		arnold.AiNodeSetInt(options, "yres", 360)
		arnold.AiNodeSetInt(options, "GI_diffuse_depth", 4)
		arnold.AiNodeSetPtr(options, "camera", camera)
  
 		 # create an output driver node
		driver = arnold.AiNode("driver_jpeg")
		arnold.AiNodeSetStr(driver, "name", "mydriver")
		arnold.AiNodeSetStr(driver, "filepath", os.path.dirname(self.image))
		arnold.AiNodeSetStr(driver, "filename", os.path.basename(self.image))
		arnold.AiNodeSetFlt(driver, "gamma", 2.2)
  
   		# create a gaussian filter node
		filter = arnold.AiNode("gaussian_filter")
		arnold.AiNodeSetStr(filter, "name", "myfilter")
  
   		# assign the driver and filter to the main (beauty) AOV,
   		# which is called "RGBA" and is of type RGBA
		outputs_array = arnold.AiArrayAllocate(1, 1, arnold.AI_TYPE_STRING)
		arnold.AiArraySetStr(outputs_array, 0, "RGBA RGBA myfilter mydriver")
		arnold.AiNodeSetArray(options, "outputs", outputs_array)
  
   		# finally, render the image!
		arnold.AiRender(arnold.AI_RENDER_MODE_CAMERA)
    
   		# // Arnold session shutdown
		arnold.AiEnd()

	def setColor(self,color):
		""" Sets the color for the object that is being rendered.

			Args:

				color(tuple): The r,g,b values of the color that is to be set
		"""
		self._color = color

