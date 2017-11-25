import PyQt4
import arnold
import sys,os

from arnold import *
 
   # // start an Arnold session, log to both a file and the console
AiBegin();

AiMsgSetLogFileName("scene1.log");
AiMsgSetConsoleFlags(AI_LOG_ALL);
  
   # // create a sphere geometric primitive
sph = AiNode("sphere");
AiNodeSetStr(sph, "name", "mysphere")
AiNodeSetVec(sph, "center", 0.0, 4.0, 0.0);
AiNodeSetFlt(sph, "radius", 4.0);
  
   # // create a red standard shader
shader1 = AiNode("standard");
AiNodeSetStr(shader1, "name", "myshader1");
AiNodeSetRGB(shader1, "Kd_color", 1.0, 0.02, 0.02);
AiNodeSetFlt(shader1, "Ks", 0.05);
  
# // assign the shaders to the geometric objects
AiNodeSetPtr(sph, "shader", shader1);
  
 # // create a perspective camera
camera = AiNode("persp_camera");
AiNodeSetStr(camera, "name", "mycamera");
   # // position the camera (alternatively you can set 'matrix')
AiNodeSetVec(camera, "position", 0.0, 10.0, 35.0);
AiNodeSetVec(camera, "look_at", 0.0, 3.0, 0.0);
AiNodeSetFlt(camera, "fov", 45.0);
  
   # // create a point light source
light = AiNode("point_light");
AiNodeSetStr(light, "name", "mylight");
# // position the light (alternatively use 'matrix')
AiNodeSetVec(light, "position", 15.0, 30.0, 15.0);
AiNodeSetFlt(light, "intensity", 4500.0); # alternatively, use 'exposure'
AiNodeSetFlt(light, "radius", 15.0); # for soft shadows
  
 # // get the global options node and set some options
options = AiUniverseGetOptions();
AiNodeSetInt(options, "AA_samples", 8);
AiNodeSetInt(options, "xres", 480);
AiNodeSetInt(options, "yres", 360);
AiNodeSetInt(options, "GI_diffuse_depth", 4);
 # // set the active camera (optional, since there is only one camera)
AiNodeSetPtr(options, "camera", camera);
  
   # // create an output driver node
driver = AiNode("driver_jpeg");
AiNodeSetStr(driver, "name", "mydriver");
AiNodeSetStr(driver, "filename", "scene1.jpg");
AiNodeSetFlt(driver, "gamma", 2.2);
  
   # // create a gaussian filter node
filter = AiNode("gaussian_filter");
AiNodeSetStr(filter, "name", "myfilter");
  
   # // assign the driver and filter to the main (beauty) AOV,
   # // which is called "RGBA" and is of type RGBA
outputs_array = AiArrayAllocate(1, 1, AI_TYPE_STRING);
AiArraySetStr(outputs_array, 0, "RGBA RGBA myfilter mydriver");
AiNodeSetArray(options, "outputs", outputs_array);
  
   # // finally, render the image!
AiRender(AI_RENDER_MODE_CAMERA);
  
   # // ... or you can write out an .ass file instead
   # //AiASSWrite("scene1.ass", AI_NODE_ALL, FALSE);
  
   # // Arnold session shutdown
AiEnd();