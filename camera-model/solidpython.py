from solid import *
from solid.utils import *

SEGMENTS = 50
f = 4

for i in []: front_camera = rotate([90, 0, 0])(cylinder(5, 4))

camera = cube([96, 4, 27]) + translate([(96-57)/2, 4, (27-21)/2])(cube([57, 16, 21]))
for i in [27/2, 96-27/2]: camera += translate([i, 9+4, 27/2])(rotate([90, 0, 0])(cylinder(4, 9)))

bottom = cube([200, 200, f])

# result = translate([100-96/2, 0, f])(camera) + bottom
result = front_camera

scad_render_to_file(result, 'result.scad', file_header=f'$fn = {SEGMENTS};')