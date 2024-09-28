#
# author: Nadeem Elahi
# nadeem.elahi@gmail.com
# nad@3deem.com
# license: gpl v3
# 

#
# Automated Rotated Geometry Generation
#

import bpy
from math import radians


def fullReset() :
	#https://blenderartists.org/t/deleting-all-from-scene/1296469
	bpy.ops.object.select_all(action='SELECT')
	bpy.ops.object.delete(use_global=False)

	bpy.ops.outliner.orphans_purge()
	bpy.ops.outliner.orphans_purge()
	bpy.ops.outliner.orphans_purge()


	
def addLamp( name , watts , radius , 
		xloc , yloc , zloc ) :
	#https://docs.blender.org/api/master/bpy.types.Object.html

	lamp_name = name
	light_data = bpy.data.lights.new( 
			name = lamp_name ,
			type = 'POINT'
			)
	light_object = bpy.data.objects.new(
			name = lamp_name ,
			object_data = light_data
			)
	light_object.location = ( xloc , yloc , zloc )

	bpy.context.scene.collection.objects.link ( light_object )
	bpy.data.lights[ lamp_name ].energy = watts # 10 W default
	bpy.data.lights[ lamp_name ].shadow_soft_size = radius 



def addCam( name , 
		xloc , yloc , zloc ,
		xangle , yangle , zangle ) :

	camera_data = bpy.data.cameras.new( name = camera_name )

	camera_object = bpy.data.objects.new( camera_name , camera_data )
	camera_object.rotation_euler = ( xangle , yangle , zangle )
	camera_object.location = ( xloc , yloc , zloc )

	bpy.context.scene.collection.objects.link( camera_object )
		
	bpy.context.view_layer.objects.active = camera_object



def addNurbsPath ( name ,
		radius , depth , resolution ,
		fillCaps ,
		xloc , yloc , zloc ,
		xangle , yangle , zangle ,
		xscale , yscale , zscale ) :

	bpy.ops.curve.primitive_nurbs_path_add(
			radius = radius ,
			location = ( xloc , yloc , zloc ) , 
			rotation = ( xangle , yangle , zangle ) ,
			scale = ( xscale , yscale , zscale )
			)

	bpy.context.object.name = name

	bpy.data.objects[ name ].data.bevel_depth = depth
	bpy.data.objects[ name ].data.bevel_resolution = resolution 
	if ( fillCaps ) :
		bpy.data.objects[ name ].data.use_fill_caps = True

	


def extrudeNurbsPath ( xloc , yloc , zloc ) :
	bpy.ops.curve.extrude_move(
			CURVE_OT_extrude={"mode":'TRANSLATION'}, 
			TRANSFORM_OT_translate={
				"value":(xloc, yloc, zloc) 
				}
			)


fullReset()


# add lamp
lamp_name = "lamp1" # front right
addLamp( lamp_name , 100 , 1.0 , # 100 watts , shadow_soft_size / radius 1.0
		1.0 , -1.0 , 1.0 )


lamp_name = "lamp2" # front left up higher 
addLamp( lamp_name , 100 , 5.0 , # 100 watts , shadow_soft_size / radius 1.0
		-2.0 , -2.0 , 2.0 )


lamp_name = "lamp3" # back center
addLamp( lamp_name , 100 , 5.0 , # 100 watts , shadow_soft_size / radius 1.0
		0.0 , 2.0 , 2.0 )



# add camera 
camera_name = "camera1"
addCam( camera_name , 
	0.0 , -5.0 , 2.0 , # xyz loc
	radians( 67 ) , 0 , 0 ) # angles


depth = 0.1 

xloc = 0.0
yloc = 0.0
zloc = 0.0

# nurbs path coil
nurbs_path_name = "nurbs1"
addNurbsPath ( nurbs_path_name ,
		1.0 , depth , 4 , # radius , depth , resolution
		1 , # fill caps/end points
		xloc , yloc , zloc ,
		0.0 , 0.0 , 0.0 , 
		1.0 , 1.0 , 1.0 
		)

# 5 verts to start
# remove all but the center vert 
# there are 5 total by default
# delete first two and last two

bpy.ops.object.select_all( action='DESELECT' )
bpy.data.objects[ nurbs_path_name ].select_set( True )

bpy.ops.object.mode_set( mode='EDIT' )
bpy.ops.curve.select_all(action='DESELECT')

bpy.ops.curve.de_select_last()
bpy.ops.curve.dissolve_verts()

#twice
bpy.ops.curve.de_select_last()
bpy.ops.curve.dissolve_verts()

bpy.ops.curve.de_select_first()
bpy.ops.curve.dissolve_verts()

bpy.ops.curve.de_select_first()
bpy.ops.curve.dissolve_verts()

# just center vert remains
bpy.ops.curve.de_select_last()
