import math
import time


# donut

radius = 1.0

width  = 0.6

pi = 3.1415 # 1 radian

a = 0 # skeleton rim |  0 - 2pi

b = 0 # surface ring |  0 - 2pi

# window dimensions
w = 80
h = 35
screen_pos = {'x': 0.0, 'y': 0.0, 'z': -4.0}
screen_w = 1
screen_h = 1

# calculate cam fov to capture the whole torus
# when rotated vertically torus will stand from y: -1.5 to y: 1.5
# width would be as far -> x: -1.5 to x: 1.5
# tan(fov/2) = 1 / h
# tan(fov/2) = 1.5 / (2 + h)
# h = 1 / tan(fov/2)
# (2 + h) = 1.5 / tan(fov/2)
# h = (1.5 / tan(fov/2)) - 2
# 1 / tan(fov/2) = (1.5 / tan(fov/2)) - 2
# 1 / tan(fov/2) = (1.5 / tan(fov/2)) - (2 * tan(fov/2)) / (tan(fov/2))
# 1 / tan(fov/2) = (1.5 - 2 * tan(fov/2)) / tan(fov/2)
# 1 = 1.5 - 2 * tan(fov/2)
# 1 - 1.5 = -0.5 = -2 * tan(fov/2) # /-2
# -0.5 / -2 = tan(fov/2)
# fov/2 = atan(0.25)
# fov/2 = 0.24497866
# h = 1 / tan(0.24497866)
# h = 1 / 0.25
cam_h = 4


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

def rotate_3d(coords: list[float, float, float], ra: float, rb: float, rc: float) -> list[float, float, float]:
	current = coords
	# ra -> rotate around (0, 0) , plane zx , preserve y
	# distance from origin -> d**2 = coord_x**2 + coord_z**2
	# d = (coord_x**2 + coord_z**2)**0.5
	d = (current[0]**2 + current[2]**2)**0.5

	if not d == 0:
		# get old angle
		# sin(old_ra) = coord_x / d
		# asin(sin(old_ra)) = asin(coord_x / d)
		old_ra = math.atan2(current[0], current[2])

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

	if not d == 0:
		# get old angle
		# sin(old_rb) = coord_x / d
		# asin(sin(old_rb)) = asin(coord_x / d)
		old_rb = math.atan2(current[0], current[1])

		# sin(rb) = new_x / d
		new_x = math.sin(old_rb + rb) * d

		# cos(rb) = new_y / d
		new_y = math.cos(old_rb + rb) * d

		current[0] = new_x
		current[1] = new_y

	# rc -> rotate around (0, 0) , plane yz , preserve x
	# distance from origin -> d**2 = coord_z**2 + coord_y**2
	d = (current[2]**2 + current[1]**2)**0.5

	if not d == 0:
		# get old angle
		# sin(old_rc) = coord_z / d
		# asin(sin(old_rc)) = asin(coord_z / d)
		old_rc = math.atan2(current[2], current[1])

		# sin(rc) = new_z / d
		new_z = math.sin(old_rc + rc) * d

		# cos(rc) = new_y / d
		new_y = math.cos(old_rc + rc) * d

		current[2] = new_z
		current[1] = new_y

	return [*current]


def normalize(vector: list[float, float, float]) -> list[float, float, float]:
	v = vector
	d = (v[0]**2 + v[1]**2 + v[2]**2)**0.5

	if d == 0:
		return [0, 0, 0]

	new_x = v[0] / d
	new_y = v[1] / d
	new_z = v[2] / d
	
	return [new_x, new_y, new_z]

def get_normal(ra: float, rb: float, rc: float, a: float, b: float) -> list[float, float, float]:
	# normalized vector from skeleton rim to the surface

	# 1. find a point on the skeleton rim (with regard to rotations)
	# 2. from rim point find the point on surface (with regard to rotations)
	# 3. calculate the height from the rim to the surface point and normalize

	# get rim and surface caculations, then apply rotation math to them to get actual virtual rim

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

	y = local_y

	rim           = [rim_x, 0, rim_z]
	surface_point = [x, y, z]

	# now get the vector distance
	sf = surface_point
	r = rim
	vector = [sf[0] - r[0], sf[1] - r[1], sf[2] - r[2]] # surface_point_vec3 - rim_vec3

	# apply rotations

	vector = rotate_3d(vector, ra, rb, rc)

	# normalize vector
	vector = normalize(vector)

	return vector

def project_on_screen(point: list[float, float, float]) -> list[float, float]:
	'''
	w = 80
	h = 35
	screen_pos = {'x': 0.0, 'y': 0.0, 'z': -2.0}
	screen_w = 1
	screen_h = 1
	cam_h = 4
	'''
	p2 = {'x': 0, 'y': 0}

	cam_pos = {'x': 0, 'y': 0, 'z': screen_pos['z'] - cam_h}

	# horizontal
	# (point_z - cam_pos_z) / point_x = cam_h / p2.x
	# p2.x * (point_z - cam_pos_z) = point_x * cam_h
	# p2.x = (point_x * cam_h) / (point_z - cam_pos_z)
	p2['x'] = (point[0] * cam_h) / (point[2] - cam_pos['z'])

	# vertical
	# (point_z - cam_pos_z) / point_y = cam_h / p2.y
	# p2.y = (point_y * cam_h) / (point_z - cam_pos_z)
	p2['y'] = (point[1] * cam_h) / (point[2] - cam_pos['z'])

	return [p2['x'], p2['y']]


def get_to_cam_distance(point: list[float, float, float]) -> float:
	cam_pos = {'x': 0, 'y': 0, 'z': screen_pos['z'] - cam_h}

	d_sq = (point[0] - cam_pos['x'])**2 + (point[1] - cam_pos['y'])**2 + (point[2] - cam_pos['z'])**2

	d = d_sq ** 0.5

	return d

def is_normal_face_visible(normal):
	camera_direction = [0, 0, 1]

	return (normal[0]*camera_direction[0] + normal[1]*camera_direction[1] + normal[2]*camera_direction[2]) < 0

# https://www.google.com/url?sa=t&source=web&rct=j&url=https%3A%2F%2Fwww.tiktok.com%2F%40jomaoppa%2Fvideo%2F7085420569780440366&ved=0CBYQjRxqGAoTCJCthPS7sZUDFQAAAAAdAAAAABCgAQ&opi=89978449
colors = ".,-~!;=/$#@"

def get_color(normal):
	light = normalize([0,0,-1])

	brightness = max(normal[0]*light[0] + normal[1]*light[1] + normal[2]*light[2], 0)

	index = int(brightness * (len(colors)))

	return colors[index]

point = get_3d_point(0, pi / 2)

# in radians
ra = 0 # rotation a -> z, x plane z+ x0 start, going clockwise
rb = 0 # rotation b -> y, x plane y+ x0 start, going clockwise
rc = 0 # rotation c -> y, z plane y+ z0 start, going from y: 1, z: 0 to y:0, z: 1

#normal = get_normal(ra, rb, rc, test_a, test_b)

print(point)

point = rotate_3d(point, ra, rb, rc)



print("Projection must be at: [0, 0]")

print(f"projection coords: {project_on_screen(point)}")

# pipeline
# 1. Decide the Skeleton Rim Points number
num_rim = 150

# 2. Decide the Surface Rings Points' Number
num_ring = 150

points   = []

rim_ring = []

normals_world = []

# 3. Get the points
for rim_n in range(num_rim):
	for ring_n in range(num_ring):
		a = ((pi*2) / num_rim ) * rim_n
		b = ((pi*2) / num_ring) * ring_n

		point = get_3d_point(a, b)
		points.append(point)
		rim_ring.append([rim_n, ring_n])

		# unit surface normal in local space
		# rotated in sync with the point below
		normals_world.append(normalize([
			math.sin(b) * math.sin(a),
			math.cos(b),
			math.sin(b) * math.cos(a),
		]))



dt = 1 / 60
acc = 0
last = time.perf_counter()

while 1:
	now = time.perf_counter()
	acc += now - last
	last = now

	while acc >= dt:
		acc -= dt

		# rotate at 1 radian per second
		ra = rb = rc = pi*dt

		# rotate the points
		for i in range(len(points)):
			points[i] = rotate_3d(points[i], ra, rb, rc)
			normals_world[i] = rotate_3d(normals_world[i], ra, rb, rc)

		# 4. Project the points onto a screen & Color the pixels by calculating the distances to the surface
		projections = []
		depths      = []
		normals     = []
		for p, normal in zip(points, normals_world):
			proj = project_on_screen(p)

			if proj[0] > 1 or proj[0] < -1 or proj[1] > 1 or proj[1] < -1:
				continue

			if not is_normal_face_visible(normal):
				continue

			normals.append(normal)

			projections.append(proj)

			# depth for the z-buffer: camera sits at -z looking toward +z,
			# so a smaller z is closer to the camera
			depths.append(p[2])

		grid_points = []
		# for each projection find its place on the terminal grid
		# translate screen float to terminal int
		for p in projections.copy():
			grid_points.append(  (int(((p[0] + 1) / 2) * w), int(((p[1] + 1) / 2) * h))  )

		buffer = list(' ' * ((w + 1) * h))
		# z-buffer: nearest z drawn into each cell so far (inf = still empty)
		depth_buffer = [float('inf')] * ((w + 1) * h)

		for gp, n, z in zip(grid_points, normals, depths):
			cell = (w + 1) * gp[1] + gp[0]

			# only draw if this point is nearer than whatever is already there,
			# so the far side of the donut can't overwrite the near side
			if z < depth_buffer[cell]:
				depth_buffer[cell] = z
				buffer[cell] = get_color(n)

		for i in range(h):
			buffer[w] = '\n'

		print(''.join(buffer))
