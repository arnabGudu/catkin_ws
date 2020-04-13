import rospy
from sensor_msgs.msg import LaserScan, PointCloud, ChannelFloat32
import numpy as np
import std_msgs.msg
from geometry_msgs.msg import Point32

def create_blocks(R, start, stop):
	for i in range(len(R)):
		if R[i - 1] == np.inf and R[i] != np.inf:
			start.append(i)
		if R[i - 1] != np.inf and R[i] == np.inf:
			stop.append(i-1)

	if stop[0] < start[0]:
		start[-1] = start[-1] - 360
		start.sort()

def break_blocks(p, start, stop, width = 1):
	for n,s in enumerate(start):
		for i in range(s, stop[n]):
			print(i, start[n], stop[n])
			d = np.sqrt((p[i][0] - p[i+1][0]) ** 2 +
						(p[i][1] - p[i+1][1]) ** 2	)
			if (d > width):
				stop.append(i - 1)
				start.append(i)
				print("............")
	start.sort()
	stop.sort()
	print(start, stop, len(start))

def merge_blocks(p, start, stop, width = 1):
	for i, s in enumerate(start):
		e = stop[i - 1]
		d = np.sqrt((p[s][0] - p[e][0]) ** 2 +
					(p[s][1] - p[e][1]) ** 2)
		if (d < width):
			start.pop(i)
			stop.pop(i-1)

def clustering(P, start, stop):
	for i in range(len(start)):
		print("...............")
		X = P[start[i] : stop[i]]
		n = len(X)

		if (n < 5 and n > 0):
			O = (X[0] + X[-1]) / 2
			d = np.sqrt(np.sum( (X - O) ** 2, axis = 0))
		 	D = np.max(d)
		else:
			a = (X[-1][1] - X[0][1]) / (X[-1][0] - X[0][0])
			b = -a * X[0][0] + X[0][1]
			d = (a*X + b) / np.sqrt(a ** 2 + b ** 2)
			s = np.sqrt(np.sum((X[-1] - X[0]) ** 2, axis = 0))
			D = np.max(np.abs(d))
			if D < 0.2 * s:
				cluster.append((X[0], X[-1]))
			else:
				b_above = np.max(d) * np.sqrt(a ** 2 + b ** 2)
				b_below = np.min(d) * np.sqrt(a ** 2 + b ** 2)

def main_function(R, P):
	start = []
	stop = []
	create_blocks(R, start, stop)
	# print_data(P, start, stop)
	break_blocks(P, start, stop)
	# print(start, stop)
	# print(len(start), len(stop))
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# merge_blocks(P, start, stop)
	# print_data(R, start, stop)
	# clustering(P, start, stop)
	publish_pointCloud(P, start, stop)

def publish_pointCloud(P, start, stop):
	pc = PointCloud()
	pub = rospy.Publisher("cloud", PointCloud, queue_size=100)
	header = std_msgs.msg.Header()
	header.stamp = rospy.Time.now()
	header.frame_id = 'laser'
	pc.header = header
	pc.points = [Point32(p[0], p[1], 0) for p in P
				if (p[0] != np.inf and p[0] != -np.inf)]

	clst_color = np.array(np.random.choice(range(256), size=(len(start),3)))
	# print(clst_color)
	color = np.zeros((len(pc.points), 3))
	k = 0
	for i in range(len(start)):
		for j in range(stop[i] - start[i] + 1):
			color[k] = np.array(clst_color[i])
			k = k + 1

	# http://wiki.ros.org/rviz/DisplayTypes/PointCloud
	r = ChannelFloat32(name = 'r')
	g = ChannelFloat32(name = 'g')
	b = ChannelFloat32(name = 'b')
	# color = [int(c) for c in bin(i)[2:]]	# decimal to bin list
	r.values = list(color[:, 0])
	g.values = list(color[:, 1])
	b.values = list(color[:, 2])
	pc.channels.append(r)
	pc.channels.append(g)
	pc.channels.append(b)
	pub.publish(pc)

def print_data(data, start, stop):
	for i in range(len(data)):
		print(i, data[i])
	print("###########################")
	print(start, stop)
	print(len(start), len(stop))
	print("///////////////////////////")

def callback(data):
	R = data.ranges
	P = []
	for i, r in enumerate(R):
		x = r * np.cos(i * np.pi / 180 - 3.12413907051)
		y = r * np.sin(i * np.pi / 180 - 3.12413907051)
		P.append((x, y))
	P = np.array(P)
	main_function(R, P)

def listener():
	rospy.init_node('lidar', anonymous=True)
	rospy.Subscriber("scan", LaserScan, callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
