import rospy
from sensor_msgs.msg import LaserScan
import numpy as np

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
	print(start, stop)


def merge_blocks(p, start, stop, width = 1):
	for i, s in enumerate(start):
		e = stop[i - 1]
		d = np.sqrt((p[s][0] - p[e][0]) ** 2 +
					(p[s][1] - p[e][1]) ** 2)
		if (d < width):
			start.pop(i)
			stop.pop(i-1)

def main_function(R, P):
	start = []
	stop = []
	create_blocks(R, start, stop)
	print_data(R, start, stop)
	break_blocks(P, start, stop)
	print(start, stop)
	print(len(start), len(stop))
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# merge_blocks(P, start, stop)
	# print_data(R, start, stop)

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
	main_function(R, P)

def listener():
	rospy.init_node('lidar', anonymous=True)
	rospy.Subscriber("scan", LaserScan, callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
