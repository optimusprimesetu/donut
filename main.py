import math

# window dimensions
w = 80
h = 35



# donut

radius = 1.0

width  = 0.5

pi = 3.1415 # 1 radian

a = 0 # skeleton rim |  0 - 2pi

b = 0 # surface ring |  0 - 2pi

# x -> left to right
# y -> bottom to top
# z -> to us to from us

# get 3d position of a point on the donut
def get_3d_point(a: float, b: float) -> list[float, float, float]:
	# 1. find a point on the skeleton rim
	# 2. from rim point find the point on the ring

	# donut is flat on x, z plane -> we see it from the side
	# far z is start point so z = 1, x = 0 at a = 0 to clockwise

	# for x
	# sin(a) = rim_x / radius
	# rim_x = sin(a) * radius
	rim_x = math.sin(a) * radius

	# for z
	# cos(a) = rim_z / radius
	# rim_z = cos(a) * radius
	rim_z = math.cos(a) * radius

	# local calculation from rim to surface (local_x, local_y)
	# y+ is b = 0 to clockwise

	# sin(b) = local_x / width
	# local_x = sin(b) * width
	local_x = math.sin(b) * width

	# cos(b) = local_y / width
	# local_y = cos(b) * width
	local_y = math.cos(b) * width


	# now get global x, and z coordinates
	# sin(a) = x / (radius + local_x)
	# x = sin(a) * (radius + local_x)
	x = math.sin(a) * (radius + local_x)

	# cos(a) = z / (radius + local_x)
	# z = cos(a) * (radius + local_x)
	z = math.cos(a) * (radius + local_x)

	# the height is just local_y
	y = local_y

	# print(f"a: {a:.02f}, b: {b:.02f}\n x: {x} \n y: {y} \n z: {z}")

	return [x, y, z]

def rotate_3d(coords: list[float, float, float], a: float, b: float, c: float) -> list[float, float, float]:
	current = coords
	# ra -> rotate around (0, 0) , plane zx , preserve y
	# distance from origin -> d**2 = coord_x**2 + coord_z**2
	# d = (coord_x**2 + coord_z**2)**0.5
	d = (current[0]**2 + current[2]**2)**0.5

	# get old angle
	# sin(old_ra) = coord_x / d
	# asin(sin(old_ra)) = asin(coord_x / d)
	old_ra = math.asin(current[0] / d)

	# sin(ra) = new_x / d
	new_x = math.sin(old_ra + ra) * d

	# cos(ra) = new_z / d
	new_z = math.cos(old_ra + ra) * d

	# update current calculation coords
	current[0] = new_x
	current[2] = new_z

	# rb -> rotate around (0, 0) , plane yx , preserve z
	# distance from origin -> d**2 = coord_x**2 + coord_y**2
	d = (current[0]**2 + current[1]**2)**0.5

	# get old angle
	# sin(old_rb) = coord_x / d
	# asin(sin(old_rb)) = asin(coord_x / d)
	old_rb = math.asin(current[0] / d)

	# sin(rb) = new_x / d
	new_x = math.sin(old_rb + rb) * d

	# cos(rb) = new_y / d
	new_y = math.cos(old_rb + rb) * d

	current[0] = new_x
	current[1] = new_y

	# rc -> rotate around (0, 0) , plane yz , preserve x
	# distance from origin -> d**2 = coord_z**2 + coord_y**2
	d = (current[2]**2 + current[1]**2)**0.5

	# get old angle
	# sin(old_rc) = coord_z / d
	# asin(sin(old_rc)) = asin(coord_z / d)
	old_rc = math.asin(current[2] / d)

	# sin(rc) = new_z / d
	new_z = math.sin(old_rc + rc) * d

	# cos(rc) = new_y / d
	new_y = math.cos(old_rc + rc) * d

	current[2] = new_z
	current[1] = new_y

	return [*current]

coords = get_3d_point(a, b)

print(coords)

# in radians
ra = 0 # rotation a -> z, x plane z+ x0 start, going clockwise
rb = 0 # rotation b -> y, x plane y+ x0 start, going clockwise
rc = 0 # rotation c -> y, z plane y+ z0 start, going from y: 1, z: 0 to y:0, z: 1

ra = pi

coords = rotate_3d(coords, ra, rb, rc)

print(coords)
