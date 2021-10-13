from solid import *
from solid.utils import *

SEGMENTS = 100
f = 4

front_camera = 0
for i in [[0, 0, 0], [86, 0, 0], [0, 0, 17], [86, 0, 17]]: front_camera += translate(i)(rotate([90, 0, 0])(cylinder(5, 4)))
front_camera = hull()(front_camera)
front_camera_extrude = 0
for i in [[0, 0, 0], [86, 0, 0], [0, 17, 0], [86, 17, 0]]: front_camera_extrude += translate([5, 5, -1])(translate(i)(cylinder(5, f+2)))
front_camera_extrude = hull()(front_camera_extrude)
camera = translate([5, f, 5])(front_camera) + translate([(96-57)/2, 4, (27-21)/2])(cube([57, 16, 21]))
for i in [27/2, 96-27/2]: camera += translate([i, 9+4, 27/2])(rotate([90, 0, 0])(cylinder(4, 9)))
camera = color('orange')(camera)

hole = cube([f+1, 20, f+2])
hole_w_1 = cube([f+1, 21, f+2])
bottom = cube([200, 200, f]) - translate([-1, -1, -1])(hole_w_1) - translate([200-f, -1, -1])(hole_w_1)
for i in range(40, 200, 40): bottom -= translate([-1, i, -1])(hole) + translate([200-f, i, -1])(hole)

front_part = cube([200-f*2, 50, f]) - translate([(200-f*2-96)/2, (50-27)/2, 0])(front_camera_extrude)

side = left(2)(linear_extrude(f)(arc(rad=50, start_degrees=90, end_degrees=135)) + cube([200+2, 50, f])) - rotate(-90)(translate([-f, 180, -1])(hole_w_1))
for i in range(20, 180, 40): side -= rotate(-90)(translate([-f, i, -1])(hole))
side = color('orange')(side)

deg = 45
front_part_w_camera = up(f)(rotate([90+deg, 0, 0])(right(f)(front_part))) + up(f)(rotate([deg])(translate([(200-96)/2, -f, (50-27)/2])(camera)))

result = bottom
result += rotate([90, 0, 90])(side) + right(200-f)(rotate([90, 0, 90])(side))
result += front_part_w_camera

scad_render_to_file(result, 'result.scad', file_header=f'$fn = {SEGMENTS};')