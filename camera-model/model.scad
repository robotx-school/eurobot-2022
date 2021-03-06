// Generated by SolidPython 1.1.1 on 2021-11-12 14:02:44
$fn = 200;


union() {
	difference() {
		cube(size = [200, 200, 4]);
		translate(v = [-1, -1, -1]) {
			cube(size = [5, 21, 6]);
		}
		translate(v = [196, -1, -1]) {
			cube(size = [5, 21, 6]);
		}
		union() {
			translate(v = [-1, 40, -1]) {
				cube(size = [5, 20, 6]);
			}
			translate(v = [196, 40, -1]) {
				cube(size = [5, 20, 6]);
			}
		}
		union() {
			translate(v = [-1, 80, -1]) {
				cube(size = [5, 20, 6]);
			}
			translate(v = [196, 80, -1]) {
				cube(size = [5, 20, 6]);
			}
		}
		union() {
			translate(v = [-1, 120, -1]) {
				cube(size = [5, 20, 6]);
			}
			translate(v = [196, 120, -1]) {
				cube(size = [5, 20, 6]);
			}
		}
		union() {
			translate(v = [-1, 160, -1]) {
				cube(size = [5, 20, 6]);
			}
			translate(v = [196, 160, -1]) {
				cube(size = [5, 20, 6]);
			}
		}
		translate(v = [40, 196, -1]) {
			cube(size = [40, 5, 6]);
		}
		translate(v = [120, 196, -1]) {
			cube(size = [40, 5, 6]);
		}
		translate(v = [100, 100, -1]) {
			cylinder(d = 10, h = 6);
		}
	}
	union() {
		rotate(a = [90, 0, 90]) {
			difference() {
				union() {
					difference() {
						union() {
							difference() {
								cube(size = [200, 50, 4]);
								rotate(a = -90) {
									translate(v = [-4, 180, -1]) {
										cube(size = [5, 21, 6]);
									}
								}
							}
							translate(v = [-6, 4, 0]) {
								linear_extrude(height = 4) {
									difference() {
										circle(r = 46);
										rotate(a = 90) {
											translate(v = [0, -46, 0]) {
												square(center = true, size = [138, 92]);
											}
										}
										rotate(a = -45) {
											translate(v = [0, -46, 0]) {
												square(center = true, size = [138, 92]);
											}
										}
									}
								}
							}
							translate(v = [-6, 4, 0]) {
								rotate(a = [0, 0, 135]) {
									translate(v = [-4, 0, 0]) {
										cube(size = [50, 5.5000000000, 4]);
									}
								}
							}
							mirror(v = [1, 0, 0]) {
								cube(size = [6, 50, 4]);
							}
						}
						translate(v = [0, 0, -0.5000000000]) {
							rotate(a = [0, 0, 180]) {
								cube(size = [15, 5, 5]);
							}
						}
						translate(v = [-6, 4, -0.5000000000]) {
							linear_extrude(height = 5) {
								difference() {
									circle(r = 42);
									rotate(a = 90) {
										translate(v = [0, -42, 0]) {
											square(center = true, size = [126, 84]);
										}
									}
									rotate(a = -45) {
										translate(v = [0, -42, 0]) {
											square(center = true, size = [126, 84]);
										}
									}
								}
							}
						}
					}
					translate(v = [-6, 4, 0]) {
						linear_extrude(height = 4) {
							difference() {
								circle(r = 39);
								rotate(a = 90) {
									translate(v = [0, -39, 0]) {
										square(center = true, size = [117, 78]);
									}
								}
								rotate(a = -45) {
									translate(v = [0, -39, 0]) {
										square(center = true, size = [117, 78]);
									}
								}
							}
						}
					}
				}
				translate(v = [-6, 4, -0.5000000000]) {
					rotate(a = [0, 0, 0]) {
						translate(v = [0, 40.5000000000, 0]) {
							cylinder(d = 3, h = 5);
						}
					}
				}
				translate(v = [-6, 4, -0.5000000000]) {
					rotate(a = [0, 0, 45]) {
						translate(v = [0, 40.5000000000, 0]) {
							cylinder(d = 3, h = 5);
						}
					}
				}
				translate(v = [-6, 4, -0.5000000000]) {
					cylinder(d = 3, h = 5);
				}
				translate(v = [-6, 4, -0.5000000000]) {
					rotate(a = [0, 0, 45]) {
						translate(v = [0, 40.5000000000, 0]) {
							difference() {
								translate(v = [-6, 0, 0]) {
									cube(size = [6, 6, 5]);
								}
								cylinder(h = 5, r = 5.5000000000);
							}
						}
					}
				}
				translate(v = [-7.5000000000, 5.5000000000, -0.5000000000]) {
					rotate(a = [0, 0, 0]) {
						difference() {
							translate(v = [-3.9000000000, -6, 0]) {
								cube(size = [3.9000000000, 6, 5]);
							}
							cylinder(h = 5, r = 5.5000000000);
						}
					}
				}
				rotate(a = -90) {
					translate(v = [-4, 20, -1]) {
						cube(size = [5, 20, 6]);
					}
				}
				rotate(a = -90) {
					translate(v = [-4, 60, -1]) {
						cube(size = [5, 20, 6]);
					}
				}
				rotate(a = -90) {
					translate(v = [-4, 100, -1]) {
						cube(size = [5, 20, 6]);
					}
				}
				rotate(a = -90) {
					translate(v = [-4, 140, -1]) {
						cube(size = [5, 20, 6]);
					}
				}
				translate(v = [196, 17.0000000000, -1]) {
					cube(size = [5, 20, 6]);
				}
			}
		}
		translate(v = [196, 0, 0]) {
			rotate(a = [90, 0, 90]) {
				difference() {
					union() {
						difference() {
							union() {
								difference() {
									cube(size = [200, 50, 4]);
									rotate(a = -90) {
										translate(v = [-4, 180, -1]) {
											cube(size = [5, 21, 6]);
										}
									}
								}
								translate(v = [-6, 4, 0]) {
									linear_extrude(height = 4) {
										difference() {
											circle(r = 46);
											rotate(a = 90) {
												translate(v = [0, -46, 0]) {
													square(center = true, size = [138, 92]);
												}
											}
											rotate(a = -45) {
												translate(v = [0, -46, 0]) {
													square(center = true, size = [138, 92]);
												}
											}
										}
									}
								}
								translate(v = [-6, 4, 0]) {
									rotate(a = [0, 0, 135]) {
										translate(v = [-4, 0, 0]) {
											cube(size = [50, 5.5000000000, 4]);
										}
									}
								}
								mirror(v = [1, 0, 0]) {
									cube(size = [6, 50, 4]);
								}
							}
							translate(v = [0, 0, -0.5000000000]) {
								rotate(a = [0, 0, 180]) {
									cube(size = [15, 5, 5]);
								}
							}
							translate(v = [-6, 4, -0.5000000000]) {
								linear_extrude(height = 5) {
									difference() {
										circle(r = 42);
										rotate(a = 90) {
											translate(v = [0, -42, 0]) {
												square(center = true, size = [126, 84]);
											}
										}
										rotate(a = -45) {
											translate(v = [0, -42, 0]) {
												square(center = true, size = [126, 84]);
											}
										}
									}
								}
							}
						}
						translate(v = [-6, 4, 0]) {
							linear_extrude(height = 4) {
								difference() {
									circle(r = 39);
									rotate(a = 90) {
										translate(v = [0, -39, 0]) {
											square(center = true, size = [117, 78]);
										}
									}
									rotate(a = -45) {
										translate(v = [0, -39, 0]) {
											square(center = true, size = [117, 78]);
										}
									}
								}
							}
						}
					}
					translate(v = [-6, 4, -0.5000000000]) {
						rotate(a = [0, 0, 0]) {
							translate(v = [0, 40.5000000000, 0]) {
								cylinder(d = 3, h = 5);
							}
						}
					}
					translate(v = [-6, 4, -0.5000000000]) {
						rotate(a = [0, 0, 45]) {
							translate(v = [0, 40.5000000000, 0]) {
								cylinder(d = 3, h = 5);
							}
						}
					}
					translate(v = [-6, 4, -0.5000000000]) {
						cylinder(d = 3, h = 5);
					}
					translate(v = [-6, 4, -0.5000000000]) {
						rotate(a = [0, 0, 45]) {
							translate(v = [0, 40.5000000000, 0]) {
								difference() {
									translate(v = [-6, 0, 0]) {
										cube(size = [6, 6, 5]);
									}
									cylinder(h = 5, r = 5.5000000000);
								}
							}
						}
					}
					translate(v = [-7.5000000000, 5.5000000000, -0.5000000000]) {
						rotate(a = [0, 0, 0]) {
							difference() {
								translate(v = [-3.9000000000, -6, 0]) {
									cube(size = [3.9000000000, 6, 5]);
								}
								cylinder(h = 5, r = 5.5000000000);
							}
						}
					}
					rotate(a = -90) {
						translate(v = [-4, 20, -1]) {
							cube(size = [5, 20, 6]);
						}
					}
					rotate(a = -90) {
						translate(v = [-4, 60, -1]) {
							cube(size = [5, 20, 6]);
						}
					}
					rotate(a = -90) {
						translate(v = [-4, 100, -1]) {
							cube(size = [5, 20, 6]);
						}
					}
					rotate(a = -90) {
						translate(v = [-4, 140, -1]) {
							cube(size = [5, 20, 6]);
						}
					}
					translate(v = [196, 17.0000000000, -1]) {
						cube(size = [5, 20, 6]);
					}
				}
			}
		}
	}
	translate(v = [0, -6, 4]) {
		rotate(a = [135, 0, 0]) {
			translate(v = [4, 0, -2.0000000000]) {
				difference() {
					union() {
						difference() {
							cube(size = [192, 46, 4]);
							translate(v = [48.0000000000, 9.5000000000, 0]) {
								hull() {
									union() {
										translate(v = [5, 5, -1]) {
											translate(v = [0, 0, 0]) {
												cylinder(h = 6, r = 5);
											}
										}
										translate(v = [5, 5, -1]) {
											translate(v = [86, 0, 0]) {
												cylinder(h = 6, r = 5);
											}
										}
										translate(v = [5, 5, -1]) {
											translate(v = [0, 17, 0]) {
												cylinder(h = 6, r = 5);
											}
										}
										translate(v = [5, 5, -1]) {
											translate(v = [86, 17, 0]) {
												cylinder(h = 6, r = 5);
											}
										}
									}
								}
							}
						}
						translate(v = [0, -5.5000000000, 0]) {
							cube(size = [192, 5.5000000000, 4]);
						}
					}
					translate(v = [0, 42, 0]) {
						rotate(a = [0, 0, -90]) {
							union() {
								translate(v = [0, -1, -1]) {
									cube(size = [3, 14, 6]);
								}
								translate(v = [-1.2500000000, 5.2500000000, -1]) {
									cube(size = [5.5000000000, 2.5000000000, 6]);
								}
							}
						}
					}
					translate(v = [192, 39, 0]) {
						rotate(a = [0, 0, 90]) {
							union() {
								translate(v = [0, -1, -1]) {
									cube(size = [3, 14, 6]);
								}
								translate(v = [-1.2500000000, 5.2500000000, -1]) {
									cube(size = [5.5000000000, 2.5000000000, 6]);
								}
							}
						}
					}
					translate(v = [0, 1.5000000000, 0]) {
						rotate(a = [0, 0, -90]) {
							union() {
								translate(v = [0, -1, -1]) {
									cube(size = [3, 14, 6]);
								}
								translate(v = [-1.2500000000, 5.2500000000, -1]) {
									cube(size = [5.5000000000, 2.5000000000, 6]);
								}
							}
						}
					}
					translate(v = [192, -1.5000000000, 0]) {
						rotate(a = [0, 0, 90]) {
							union() {
								translate(v = [0, -1, -1]) {
									cube(size = [3, 14, 6]);
								}
								translate(v = [-1.2500000000, 5.2500000000, -1]) {
									cube(size = [5.5000000000, 2.5000000000, 6]);
								}
							}
						}
					}
				}
			}
		}
	}
	translate(v = [0, 200, 0]) {
		rotate(a = [90, 0, 0]) {
			union() {
				translate(v = [4, 4, 0]) {
					cube(size = [192, 46, 4]);
				}
				translate(v = [0, 17.0000000000, 0]) {
					cube(size = [4, 20, 4]);
				}
				translate(v = [196, 17.0000000000, 0]) {
					cube(size = [4, 20, 4]);
				}
				translate(v = [40, 0, 0]) {
					cube(size = [40, 4, 4]);
				}
				translate(v = [120, 0, 0]) {
					cube(size = [40, 4, 4]);
				}
			}
		}
	}
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
from solid import *
from solid.utils import *
import math as m

def main():
    SEGMENTS = 200
    f = 4
  
    #-- camera

    front_camera = 0
    for i in [[0, 0, 0], [86, 0, 0], [0, 0, 17], [86, 0, 17]]:
        front_camera += \
        translate(i)(
        rotate([90, 0, 0])(
        cylinder(5, 4)
        ))

    front_camera = \
    hull()(
    front_camera
    )

    front_camera_extrude = 0
    for i in [[0, 0, 0], [86, 0, 0], [0, 17, 0], [86, 17, 0]]:
        front_camera_extrude += \
        translate([5, 5, -1])(
        translate(i)(
        cylinder(5, f+2)
        ))

    front_camera_extrude = \
    hull()(
    front_camera_extrude
    )

    camera = \
    translate([5, f, 5])(front_camera) + \
    translate([(96-57)/2, 4, (27-21)/2])(
    cube([57, 16, 21])
    )

    for i in [27/2, 96-27/2]:
        camera += \
        translate([i, 9+4, 27/2])(
        rotate([90, 0, 0])(
        cylinder(4, 9)
        ))

    camera = \
    color('grey')(
    camera
    )

    #-- bottom

    hole = \
    cube([f+1, 20, f+2])

    hole_w_1 = \
    cube([f+1, 21, f+2])

    big_hole = \
    cube([40, f+1, f+2])

    bottom = \
    cube([200, 200, f]) - \
    translate([-1, -1, -1])(
    hole_w_1
    ) - \
    translate([200-f, -1, -1])(
    hole_w_1
    )

    for i in range(40, 200, 40):
        bottom -= \
        translate([-1, i, -1])(
        hole
        ) + \
        translate([200-f, i, -1])(
        hole
        )
    
    for i in [40, 120]:
        bottom -= \
        translate([i, 200-f, -1])(
        big_hole
        )

    bottom -= \
    translate([100, 100, -1])(
    cylinder(h=f+2, d=10)
    )

    #-- front part

    bolt_ext = \
    translate([0, -1, -1])(
    cube([3, 13+1, f+2])
    ) + \
    translate([-(5.5-3)/2, 13/2-2.5/2, -1])(
    cube([5.5, 2.5, f+2])
    )

    fr_part_h = 50-f

    front_part = \
    cube([200-f*2, fr_part_h, f]) - \
    translate([(200-f*2-96)/2, (fr_part_h-27)/2, 0])(
    front_camera_extrude
    )

    dip = 1.5 + 4
    front_part += \
    translate([0, -dip, 0])(
    cube([200 - f * 2, dip, f])
    )
    dip = 0

    h = 42
    h_2 = 1.5
    for i in (h, h_2):
        front_part -= \
        forward(i)(
        rotate([0, 0, -90])(
        bolt_ext
        ))

        front_part -= \
        translate([200-f*2, i-3, 0])(
        rotate([0, 0, 90])(
        bolt_ext
        ))
    h = 0

    #-- side

    lean_offset = 0

    side = \
    cube([200, 50, f]) - \
    rotate(-90)(
    translate([-f, 180, -1])(
    hole_w_1
    ))

    side += \
    translate([-6, f, 0])(
    linear_extrude(f)(
    arc(rad=fr_part_h, start_degrees=90+lean_offset, end_degrees=135+lean_offset)
    ))

    side += \
    translate([-6, f, 0])(
    rotate([0, 0, 135])(
    translate([-4, 0, 0])(
    cube([fr_part_h + 4, f + 1.5, f])
    )))

    side += \
    mirror([1, 0, 0])(
    cube([6, fr_part_h + f, f])
    )

    side -= \
    translate([0, 0, -0.5])(
    rotate([0, 0, 180])(
    cube([15, 5, f + 1])
    ))

    side -= \
    translate([-6, f, -0.5])(
    linear_extrude(f + 1)(
    arc(rad=fr_part_h - f, start_degrees=90+lean_offset, end_degrees=135+lean_offset)
    ))

    side += \
    translate([-6, f, 0])(
    linear_extrude(f)(
    arc(rad=fr_part_h - f - 3, start_degrees=90+lean_offset, end_degrees=135+lean_offset)
    ))

    for i in (0, 45):
        side -= \
        translate([-6, f, -0.5])(
        rotate([0, 0, i])(
        forward(fr_part_h-1.5-f)(
        cylinder(h=f + 1, d=3)
        )))

    side -= \
    translate([-6, f, -0.5])(
    cylinder(h=f + 1, d=3)
    )

    side -= \
    translate([-6, f, -0.5])(
    rotate([0, 0, 45])(
    forward(fr_part_h-1.5-f)(
    translate([-6, 0, 0])(cube([6, 6, f + 1])) - \
    cylinder(h=f + 1, r = 5.5)
    )))

    side -= \
    translate([-7.5, 5.5, -0.5])(
    rotate([0, 0, 0])(
    translate([-3.9, -6, 0])(cube([3.9, 6, f + 1])) - \
    cylinder(h=f + 1, r = 5.5)
    ))

    for i in range(20, 180, 40):
        side -= \
        rotate(-90)(
        translate([-f, i, -1])(
        hole
        ))

    side -= \
    translate([200-f, 15+f/2, -1])(
    cube([f+1, 20, f+2])
    )

    #-- back_part

    back_part = \
    translate([f, f, 0])(
    cube([200-f*2, 50-f, f])
    )

    for i in [0, 200-f]:
        back_part += \
        translate([i, 15+f/2, 0])(
        cube([f, 20, f])
        )

    for i in [40, 120]:
        back_part += \
        translate([i, 0, 0])(
        cube([40, f, f])
        )

    #-- front part with camera

    deg = 45
    front_part_w_camera = \
    translate([0, -6, f])(
    rotate([90+deg, 0, 0])(
    translate([f, 0, -f/2])(
    front_part
    )))
    deg = 0

    #-- model

    model = \
    bottom

    model += \
    rotate([90, 0, 90])(
    side
    ) + \
    right(200-f)(
    rotate([90, 0, 90])(
    side
    ))

    model += \
    front_part_w_camera

    model += \
    translate([0, 200, 0])(
    rotate([90, 0, 0])(
    back_part
    ))

    scad_render_to_file(model, 'model.scad', file_header=f'$fn = {SEGMENTS};')

    #-- result

    result = \
    bottom

    for i in range(1, 3):
        result += \
        translate([200+52*i, 40.2, 0])(
        rotate([0, 0, 90])(
        side
        ))

    result += \
    translate([0, 208, 0])(
    front_part
    )

    result += \
    translate([0, 208+48, 0])(
    back_part
    )

    result = \
    projection()(
    result
    )

    scad_render_to_file(result, 'result.scad', file_header=f'$fn = {SEGMENTS};')
  
if __name__ == '__main__':
    main()
 
 
************************************************/
