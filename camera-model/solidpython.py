from solid import *
from solid.utils import *

camera = cube([96, 4, 27]) + translate([(96-57)/2, 4, (27-21)/2])(cube([57, 16, 21])) + rotate()(cylinder(4, 9))

result = camera

scad_render_to_file(result, 'result.scad')