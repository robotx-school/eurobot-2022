from solid import *
from solid.utils import *

SEGMENTS = 200
f = 4

#-- camera
front_camera = 0
for i in [[0, 0, 0], [86, 0, 0], [0, 0, 17], [86, 0, 17]]: front_camera += translate(i)(rotate([90, 0, 0])(cylinder(5, 4)))
front_camera = hull()(front_camera)
front_camera_extrude = 0
for i in [[0, 0, 0], [86, 0, 0], [0, 17, 0], [86, 17, 0]]: front_camera_extrude += translate([5, 5, -1])(translate(i)(cylinder(5, f+2)))
front_camera_extrude = hull()(front_camera_extrude)
camera = translate([5, f, 5])(front_camera) + translate([(96-57)/2, 4, (27-21)/2])(cube([57, 16, 21]))
for i in [27/2, 96-27/2]: camera += translate([i, 9+4, 27/2])(rotate([90, 0, 0])(cylinder(4, 9)))
camera = color('grey')(camera)

#-- bottom
hole = cube([f+1, 20, f+2])
hole_w_1 = cube([f+1, 21, f+2])
big_hole = cube([40, f+1, f+2])
bottom = cube([200, 200, f]) - translate([-1, -1, -1])(hole_w_1) - translate([200-f, -1, -1])(hole_w_1)
for i in range(40, 200, 40): bottom -= translate([-1, i, -1])(hole) + translate([200-f, i, -1])(hole)
for i in [40, 120]: bottom -= translate([i, 200-f, -1])(big_hole)
bottom -= translate([100, 100, -1])(cylinder(h=f+2, d=10))

#-- front part
bolt_ext = translate([0, -1, -1])(cube([3, 13+1, f+2])) + translate([-(5.5-3)/2, 13/2-2.5/2, -1])(cube([5.5, 2.5, f+2]))
fr_part_h = 50-f
front_part = cube([200-f*2, fr_part_h, f]) - translate([(200-f*2-96)/2, (fr_part_h-27)/2, 0])(front_camera_extrude)
h = 42
front_part -= forward(h)(rotate([0, 0, -90])(bolt_ext))
front_part -= translate([200-f*2, h-3, 0])(rotate([0, 0, 90])(bolt_ext))
h = 0

#-- side
lean_offset = 3
side = translate([0, 50-fr_part_h, 0])(linear_extrude(f)(arc(rad=fr_part_h, start_degrees=90, end_degrees=135+lean_offset))) + cube([200, 50, f]) - rotate(-90)(translate([-f, 180, -1])(hole_w_1))
side -= translate([0, f, -1])(linear_extrude(f+2)(arc(rad=fr_part_h-f, start_degrees=90+lean_offset, end_degrees=135+lean_offset+1)))
side += translate([0, f, 0])(linear_extrude(f)(arc(rad=fr_part_h-f-3, start_degrees=90+lean_offset, end_degrees=135+lean_offset)))
side += forward(f)()(rotate([0, 0, 45+lean_offset])(left(f)(cube([4, fr_part_h, f])) + linear_extrude(f)(arc(rad=f, start_degrees=180, end_degrees=225))))
for i in [lean_offset, 45+lean_offset]: side -= translate([0, f, -1])(rotate([0, 0, i])(forward(fr_part_h-1.5-f)(cylinder(h=f+2, d=3))))
for i in range(20, 180, 40): side -= rotate(-90)(translate([-f, i, -1])(hole))
side -= translate([200-f, 15+f/2, -1])(cube([f+1, 20, f+2]))

#-- back_part
back_part = translate([f, f, 0])(cube([200-f*2, 50-f, f]))
for i in [0, 200-f]: back_part += translate([i, 15+f/2, 0])(cube([f, 20, f]))
for i in [40, 120]: back_part += translate([i, 0, 0])(cube([40, f, f]))

#-- front part with camera
deg = 45
front_part_w_camera = up(f)(rotate([90+deg, 0, 0])(right(f)(front_part))) + up(f)(rotate([deg])(translate([(200-96)/2, -f, (fr_part_h-27)/2])(camera)))
deg = 0

#-- model
model = bottom
model += rotate([90, 0, 90])(side) + right(200-f)(rotate([90, 0, 90])(side))
model += front_part_w_camera
model += translate([0, 200, 0])(rotate([90, 0, 0])(back_part))

scad_render_to_file(model, 'model.scad', file_header=f'$fn = {SEGMENTS};')

#-- result
result = bottom
for i in range(1, 3): result += translate([200+52*i, 35.3, 0])(rotate([0, 0, 90])(side))
result += translate([0, 202, 0])(front_part)
result += translate([0, 202+48, 0])(back_part)
result = projection()(result)

scad_render_to_file(result, 'result.scad', file_header=f'$fn = {SEGMENTS};')