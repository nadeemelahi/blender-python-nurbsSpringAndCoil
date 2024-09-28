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
from math import sin
from math import cos

depth = 0.1 
zlocInc = 0.001
angleInc = 10



def fullReset() :
	#https://blenderartists.org/t/deleting-all-from-scene/1296469
	bpy.ops.object.select_all(action='SELECT')
	bpy.ops.object.delete(use_global=False)

	bpy.ops.outliner.orphans_purge()
	bpy.ops.outliner.orphans_purge()
	bpy.ops.outliner.orphans_purge()



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

# single verts setup above


# winding

zloc = zlocInc
angle = angleInc

windingCnt = 5
lim = windingCnt * 360 / angle 

idx = 1
while idx < lim :
    #print ( 'idx' , idx )

    xloc = sin ( radians ( angle ) ) 
    yloc = cos ( radians ( angle ) )
    
    extrudeNurbsPath ( xloc , yloc , zloc )

    angle += angleInc
    zloc += zlocInc
    print ( 'zloc' , zloc )
    idx += 1


# back to object mode
bpy.ops.object.mode_set( mode='OBJECT' )
