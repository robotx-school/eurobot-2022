// Generated by SolidPython 1.1.1 on 2021-10-12 18:25:39
$fn = 50;


union() {
	translate(v = [52.0000000000, 0, 4]) {
		union() {
			cube(size = [96, 4, 27]);
			translate(v = [19.5000000000, 4, 3.0000000000]) {
				cube(size = [57, 16, 21]);
			}
			translate(v = [13.5000000000, 13, 13.5000000000]) {
				rotate(a = [90, 0, 0]) {
					cylinder(h = 9, r = 4);
				}
			}
			translate(v = [82.5000000000, 13, 13.5000000000]) {
				rotate(a = [90, 0, 0]) {
					cylinder(h = 9, r = 4);
				}
			}
		}
	}
	cube(size = [200, 200, 4]);
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
from solid import *
from solid.utils import *

SEGMENTS = 50
f = 4

camera = cube([96, 4, 27]) + translate([(96-57)/2, 4, (27-21)/2])(cube([57, 16, 21]))
for i in [27/2, 96-27/2]:
    camera += translate([i, 9+4, 27/2])(rotate([90, 0, 0])(cylinder(4, 9)))

bottom = cube([200, 200, f])

result = translate([100-96/2, 0, f])(camera) + bottom

scad_render_to_file(result, 'result.scad', file_header=f'$fn = {SEGMENTS};') 
 
************************************************/
