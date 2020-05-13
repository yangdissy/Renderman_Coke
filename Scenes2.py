#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import prman
import sys
import sys,os.path,subprocess
import argparse
sys.path.append('Common')
sys.path.append('Shaders')
#sys.path.insert(0, 'Common')
#sys.path.insert(0, 'Shaders')
from Camera import *
from Obj import *
import ProcessCommandLine as cl
ri = prman.Ri() # create an instance of the RenderMan interface

def Cube(width=1.0,height=1.0,depth=1.0) :	
	w=width/2.0
	h=height/2.0
	d=depth/2.0
	#ri = prman.Ri()
	#ri.ArchiveRecord(ri.COMMENT,"Cube Generated by Cube Function")
	ri.ArchiveRecord(ri.COMMENT, 'Cube Generated by Cube Function')
	#rear
	face=[-w,-h,d,-w,h,d,w,-h,d,w,h,d]								
	ri.Patch("bilinear",{'P':face})
	#front
	face=[-w,-h,-d,-w,h,-d,w,-h,-d,w,h,-d]								
	ri.Patch("bilinear",{'P':face})
	#left
	face=[-w,-h,-d,-w,h,-d,-w,-h,d,-w,h,d]									
	ri.Patch("bilinear",{'P':face})
	#right
	face=[w,-h,-d,w,h,-d,w,-h,d,w,h,d]								
	ri.Patch("bilinear",{'P':face})
	#bottom
	face=[w,-h,d,w,-h,-d,-w,-h,d,-w,-h,-d]								
	ri.Patch("bilinear",{'P':face})
	#top
	face=[w,h,d,w,h,-d,-w,h,d,-w,h,-d]								
	ri.Patch("bilinear",{'P':face})
	ri.ArchiveRecord(ri.COMMENT, '--End of Cube Function--')

def Coke():
	ri.ArchiveRecord(ri.COMMENT, 'Coke Generated by Coke Function')

	#---------------------global scale------------
	ri.TransformBegin()
	ri.Scale( 0.1, 0.1, 0.1) 
	#----------------------body strat----------------
	ri.TransformBegin()
	ri.Rotate(90,1,0,0)
	#---------------------material start-------------------------------
	ri.AttributeBegin()
	# ri.Pattern('check','check', {'float repeatU' : [10],
	# 'float repeatV' : [10],
	# 'color baseColour' : [1.0,1.0,1.0],
	# 'color checkColour' : [0.5,0.5,0.5] })
	# ri.Bxdf('PxrSurface', 'plastic',
	# {
	# 	'reference color diffuseColor' : ['check:resultRGB'],
	# 	'int diffuseDoubleSided' : [1]

	# })
	ri.Pattern('PxrTexture', 'Cokebody',{ 'string filename' : 'Coke_Body_BaseColor.tx'})
	ri.Pattern('PxrTexture', 'Coke_smudges',{ 'string filename' : 'Coke_smudges.tx'})
	ri.Pattern('PxrTexture', 'Coke_Dust2',{ 'string filename' : 'Coke_Dust2.tx'})
	ri.Pattern('PxrMix','mix_baseColor',
	{
	'reference color color1' : ['Cokebody:resultRGB'], 
	'reference color color2' : ['Coke_smudges:resultRGB'], 
	'float mix' : [0.12], 
	})
	ri.Bxdf( 'PxrDisney','bxdf', { 
                        'reference color baseColor' : ['mix_baseColor:resultRGB'],
						"float metallic" : [0.8],
                        "float roughness" : [0.1],
                        "float specular" : [0.5], 
                        })
	ri.Cylinder(0.5,-0.75,0.75,360)
	ri.AttributeEnd() 
	#---------------------material end-------------------------------
	ri.TransformEnd()
	#-----------------------body end-----------------------

	#------top-----------
	ri.TransformBegin()
	ri.Translate(0,0.9,0)
	ri.Rotate(90,1,0,0)
	#---------------------red silver material start-------------------------------
	ri.AttributeBegin()
	ri.Pattern('PxrTexture', 'Cokebody_top',{ 'string filename' : 'Coke_Body_BaseColor_top.tx'})
	ri.Pattern('PxrTexture', 'Coke_Dust2',{ 'string filename' : 'Coke_Dust2.tx'})
	ri.Pattern('PxrMix','mix_baseColor',
	{
	'reference color color1' : ['Cokebody_top:resultRGB'],  
	'reference color color2' : ['Coke_Dust2:resultRGB'], 
	'float mix' : [0.12], 
	})
	ri.Bxdf( 'PxrDisney','bxdf', { 
                        'reference color baseColor' : ['mix_baseColor:resultRGB'],
						"float metallic" : [0.8],
                        "float roughness" : [0.1],
                        "float specular" : [0.5] 
                        })
	
	#ri.Paraboloid(0.5,1,0.5,360)
	ri.Hyperboloid([0.5,0,0.15],[0.4,0,0],360)
	ri.AttributeEnd()
	#---------------------red silver material end-------------------------------
	ri.Scale(1,1,2)
	#---------------------silver material start-------------------------------
	ri.AttributeBegin()
	ri.Pattern('Linescratch','Linescratch', 
	{
		'float angle':[90.0],
		})
	ri.Pattern('PxrMix','mix_baseColor',
	{
	'color color1' : [1.0,1.0,1.0], 
	'color color2' : [0.2,0.2,0.2], 
	'reference float mix' : ['Linescratch:resultStripes'], 
	})
	ri.Bxdf( 'PxrDisney','bxdf', { 
                        'reference color baseColor' : ['mix_baseColor:resultRGB'],
						"float metallic" : [0.8],
                        "float roughness" : [0.5],
                        "float specular" : [0.4] 
                        }) 
	ri.Torus(0.39,0.015,0.1,360,360)
	ri.TransformBegin()
	ri.Scale( 0.18, 0.18, 0.18)
	ri.Rotate(-90,1,0,0) 
	ri.Rotate(-90,0,1,0)
	ri.Translate(0,0,-0.5)
	obj=Obj("ObjFiles\PullRing.obj")
	obj.Polygon(ri)
	ri.TransformEnd()
	ri.AttributeEnd()
	#---------------------silver material end-------------------------------
	ri.Translate(0,0,0.005)
	ri.AttributeBegin()
	ri.Pattern('Linescratch','Linescratch', 
	{
		'float angle':[0.0],
		})
	ri.Pattern('PxrMix','mix_baseColor',
	{
	'color color1' : [1.0,1.0,1.0], 
	'color color2' : [0.2,0.2,0.2], 
	'reference float mix' : ['Linescratch:resultStripes'], 
	})
	ri.Pattern('PxrNormalMap', 'Coke_NormalMap',
	{ 'string filename' : 'Coke_Top_Normal_Polar.tx',
	'int invertT' : [0]})
	ri.Bxdf( 'PxrDisney','bxdf', { 
                        'reference color baseColor' : [ 'mix_baseColor:resultRGB'],
						"float metallic" : [0.8],
                        "float roughness" : [0.5],
                        "float specular" : [0.4] ,
						"reference normal bumpNormal": ['Coke_NormalMap:resultN']
                        }) 	
	ri.Disk(0,0.4,360)
	ri.AttributeEnd()
	ri.TransformEnd()
	#-----------------------------top--------------------------------------

	#---------------------------bottom------------------------------------
	ri.TransformBegin()
	#---------------------silver material start-------------------------------
	ri.AttributeBegin()
	ri.Bxdf( 'PxrDisney','bxdf', { 
                        'color baseColor' : [ 1.0,1.0,1.0],
						"float metallic" : [0.8],
                        "float roughness" : [0.5],
                        "float specular" : [0.4] 
                        }) 
	ri.Translate(0,-0.85,0)
	ri.Rotate(90,1,0,0)
	ri.Rotate(180,1,0,0)
	ri.Hyperboloid([0.5,0,0.1],[0.35,0,0],360)
	ri.Translate(0,0,0.01)
	ri.Torus(0.35,0.015,0.1,360,360)
	ri.Scale(1,1,0.35) 
	ri.Sphere(0.35,0,1,360)
	ri.AttributeEnd()
	#---------------------silver material end-------------------------------
	ri.TransformEnd()
	#---------------------bottom geometry end------------------------------

	ri.TransformEnd()
	#-----------------------globalscale-------------------------------

	ri.ArchiveRecord(ri.COMMENT, '--End of Coke Function--')

def main(filename,shadingrate=10,pixelvar=0.1,
		 fov=48.0,width=1024,height=720,
		 integrator='PxrPathTracer',integratorParams={}
		):

	print ('shading rate {} pivel variance {} using {} {}'.format(shadingrate,pixelvar,integrator,integratorParams))
	
	ri.Begin(filename)	

	# FILENAME DISPLAY Type Output format
	ri.Display('screen.exr', 'it', 'rgba')
	ri.Format(1920,1080,1)


	#ri.Hider('raytrace' ,{'int incremental' :[1]})
	#ri.Integrator('PxrPathTracer','integrator')
	#ri.ShadingRate(shadingrate)
	#ri.PixelVariance (pixelvar)

	ri.Hider('raytrace' ,{'int incremental' :[1],'int maxsamples' : [1024]})
	ri.ShadingRate(shadingrate)
	ri.PixelVariance (pixelvar)
	ri.Integrator (integrator ,'integrator',integratorParams)
	ri.Option( 'statistics', {'filename'  : [ 'stats.txt' ] } )
	ri.Option( 'statistics', {'endofframe' : [ 1 ] })
	#set searchpath
	ri.Option('searchpath', {'string texture':'Textures\:@'})
	ri.Option('searchpath', {'string shader' :'Shaders\:@'})
	#ri.Option('searchpath', {'string archive':'ObjFiles\:@'})


	#ri.Projection(ri.PERSPECTIVE,{ri.FOV:fov})
	ri.Projection('PxrCamera',{
                ri.FOV:fov,
                'float fStop' : [16.0],
                'float focalLength' : [0.12],
                'float focalDistance' : [0.35],
                #'color transverse' : [1,1.0005, 1.001], 
                'float natural' : [0.5],
  	})
	#---------frountCamera-------------------------
	#cam=Camera(Vec4(0,0,1.5),Vec4(0,0,0),Vec4(0,1,0))
	#cam.slide(0.0,0.1,0.0)
	#---------perCamera-------------------------
	cam=Camera(Vec4(-0.3,0,1.05),Vec4(0,0,0),Vec4(0,1,0))# pre
	#cam=Camera(Vec4(0,0.1,2),Vec4(0,0,0),Vec4(0,1,0))# pre
	cam.slide(0.22,0.2,0.3)
	
	
	cam.place(ri)

	#------------------------------screen strat------------------------------------
	ri.WorldBegin()


	#######################################################################
	# start lighting
	#######################################################################
	#Environment Light
	ri.TransformBegin()
	ri.AttributeBegin()
	ri.Declare('domeLight' ,'string')
	ri.Rotate(-90,1,0,0)
	ri.Rotate(0,0,0,1)
	ri.Light( 'PxrDomeLight', 'domeLight', { 
			  'string lightColorMap'  : 'veranda_1k.tx'
	})
	ri.AttributeEnd()
	ri.TransformEnd()
	#######################################################################
	# end lighting
	#######################################################################
  
	#######################################################################
	# start geomertry
	#######################################################################
	#--------------------------first Coke-------------------------------
	ri.TransformBegin()
	ri.Translate(0,0.135,1)
	ri.Rotate(-95,0,1,0)
	Coke()
	ri.TransformEnd()
	#--------------------------first Coke-------------------------------
	#--------------------------second Coke-------------------------------
	ri.TransformBegin()
	ri.Translate(0,0.1,0.9)
	ri.Rotate(90,0,0,1)
	ri.Rotate(25,1,0,0)
	ri.Translate(0.0,0.02,0.0)
	Coke()
	ri.TransformEnd()
	#--------------------------second Coke-------------------------------

	#--------------------------create table--------------------------------
	ri.TransformBegin()
	ri.Translate(0,0,1)
	ri.Rotate(0,0,1,0)
	ri.AttributeBegin()
	#######################################################################
	#---------------------------test shader--------------------------------
	
	# ri.Pattern('check','check', {'float repeatU' : [10],
	# 'float repeatV' : [10],
	# 'color baseColour' : [1.0,1.0,1.0],
	# 'color checkColour' : [0.5,0.5,0.5] })
	# ri.Bxdf('PxrSurface', 'plastic',
	# {
	# 	'reference color diffuseColor' : ['check:resultRGB'],
	# 	'int diffuseDoubleSided' : [1]

	# })
	########################################################################	
	ri.Pattern('PxrTexture', 'diffuseColor',
	{ 'string filename' : 'brown_planks_03_diff_1k.tx'})
	ri.Pattern('PxrNormalMap', 'NormalMap',
	{ 'string filename' : 'brown_planks_03_Nor_1k.tx'})
	ri.Pattern('PxrBump', 'displaceMap',
	{ 'string filename' : 'brown_planks_03_Disp_1k.tx'})

	ri.Attribute ('trace' ,{'int displacements' : [ 1 ]})
	ri.Attribute ('displacementbound', 
	#{'float sphere' : [0.1], 'string coordinatesystem' : ['shader']})
	{'float sphere' : [0.2]})
	ri.Pattern('PxrDispTransform','DispTransform',
    {
      'reference vector dispVector' : ['displaceMap:resultN'],
	  #'reference float dispScalar' : ['displaceMap:resultR'],
      'uniform float dispDepth' : [1.0],
      'uniform float dispHeight' : [1.0],
      'uniform int dispType' : [2],  
      'uniform int vectorSpace' : [3], 
      'uniform int dispRemapMode' : [1], 
      'uniform float dispCenter' : [0]
    })
	ri.Displace('PxrDisplace','myDisp' ,
    {   
      'reference vector dispVector' : ['DispTransform:resultXYZ'], 
      'uniform float dispAmount' : [0.001],
      'int enabled' : [1]
    })

	ri.Bxdf( 'PxrDisney','bxdf', 
		{ 
		'reference color baseColor' : ['diffuseColor:resultRGB'],
		#'reference color baseColor' : ['DispTransform:resultXYZ'],
		"float metallic" : [0.1],
		"float roughness" : [0.9],
		"float specular" : [0.1],
		"reference normal bumpNormal": ['NormalMap:resultN']
		})

	Cube(1.5,0.1,1.0)
	ri.AttributeEnd()
	ri.TransformEnd()
	#--------------------------end table--------------------------------
	#######################################################################
	# end geomertry
	#######################################################################
	


	ri.WorldEnd()
	#------------------------------screen end------------------------------------
	ri.End()

# def checkAndCompileShader(shader) :
# 	path = sys.path.append
# 	print(path+".osl")
# 	print(os.path.isfile(shader+'.osl'))
# 	print(os.stat(shader+'.osl').st_mtime - os.stat(shader+'.oso').st_mtime > 0)
	# if os.path.isfile(shader+'.oso') != True  or os.stat(shader+'.osl').st_mtime - os.stat(shader+'.oso').st_mtime > 0 :
	# 	print ('compiling shader %s' %(shader))
	# 	try :
	# 		subprocess.call(['oslc', path+".osl"])
	# 	except subprocess.CalledProcessError :
	# 		sys.exit('shader compilation failed')
def checkAndCompileShader(shader) :
	path = os.path.join(os.pardir, 'shaders')
	print(path)
	if os.path.isfile(os.path.join(path, shader+'.oso')) != True  or os.stat(os.path.join(path, shader+'.osl')).st_mtime - os.stat(os.path.join(path, shader+'.oso')).st_mtime > 0 :
		print( 'compiling shader {0}'.format(shader))
		try:
			subprocess.check_call(['oslc', os.path.join(path,shader+'.osl')], cwd=path)
		except subprocess.CalledProcessError :
			sys.exit('shader compilation failed')


if __name__ == '__main__':
	#checkAndCompileShader('uvshader')
	#checkAndCompileShader('Linescratch')
	cl.ProcessCommandLine('Scenes.rib')

	main(cl.filename,
		cl.args.shadingrate,
		cl.args.pixelvar,
		cl.args.fov,
		cl.args.width,
		cl.args.height,
		cl.integrator,
		cl.integratorParams)