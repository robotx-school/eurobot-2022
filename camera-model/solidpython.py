from solid import *
from solid.utils import *

result = cylinder(r=10, h=5) + cylinder(r=2, h=30)

with open ('result.scad', 'w') as file:
	file.write(scad_render(result))
