import rospy
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, LaserScan
from laser_geometry.laser_geometry import LaserProjection
import numpy as np

lp = LaserProjection()
pub = rospy.Publisher("cloud", PointCloud2, queue_size=100)

def create_blocks(R, start, stop):
	j = 0
	for i in range(len(R)):
		if R[i] != np.inf:
			j = j + 1
		if R[i - 1] == np.inf and R[i] != np.inf:
			start.append(j)
		if R[i - 1] != np.inf and R[i] == np.inf:
			stop.append(j-1)

def break_blocks(p, start, stop, width = 1):
	for i in range(len(p)):
		d = np.sqrt((p[i-1][0] - p[i][0]) ** 2 +
					(p[i-1][1] - p[i][1]) ** 2	)
		if (d > width):
			stop.append(p[i-1][4])
			stop.sort()
			start.append(p[i][4])
			start.sort()

# def merge_blocks(p, start, stop, width = 1):
# 	if (start[0] < stop[0]):
# 		for i in range(len(start)):
# 			d = np.sqrt((p[i-1][0] - p[i][0]) ** 2 +
# 					(p[i-1][1] - p[i][1]) ** 2	)
# 	else:
# 		for i in range(len(stop)):
# 			d = np.

def main_function(R, P):
	start = []
	stop = []
	create_blocks(R, start, stop)
	# print_data(R, start, stop)
	# print("***************************")
	# break_blocks(P, start, stop)
	# merge_blocks()
	print_data(R, start, stop)
	print_data(P, start, stop)

def print_data(data, start, stop):
	for i in range(len(data)):
		print(i, data[i])
	print("###########################")
	print(start, stop)
	print(len(start), len(stop))
	print("///////////////////////////")

def callback(data):
	R = data.ranges
	cloud = lp.projectLaser(data)
	pub.publish(cloud)
	point_gen = pc2.read_points(cloud)
	P = list(point_gen)
	main_function(R, P)

def listener():
	rospy.init_node('lidar', anonymous=True)

	rospy.Subscriber("scan", LaserScan, callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
