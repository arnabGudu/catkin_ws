import rospy
import numpy as np
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, LaserScan
from laser_geometry.laser_geometry import LaserProjection

class lidar:
	def __init__(self):
		rospy.init_node('lidar', anonymous=True)
		rospy.Subscriber("scan", LaserScan, self.callback)

		self.lp = LaserProjection()
		self.pub = rospy.Publisher("cloud", PointCloud2,
									queue_size=100)
		self.queue = []
		rospy.spin()

	def callback(self, data):
		#self.median_filter(data)
		self.R = data.ranges							#raw laserscan data in form-
												#of R(theta)
		cloud = self.lp.projectLaser(data)		#convert laserscan to pc2
		self.pub.publish(cloud)					#publish pc2 to /cloud topic

		self.point_gen = pc2.read_points(cloud)	#point_gen reads pc2 data
		self.Print()							#prints pc2 data

		#self.preprocessing()

	def Print(self):
		for i, points in enumerate(self.point_gen):
			print(i, points)

	def median_filter(self, laserScan):
		self.queue.append(laserScan.ranges)
		if len(self.queue) > 3:
			self.queue.pop(0)
		elif len(self.queue) == 3:
			median = []

			for i in range(360 - 2):
				mat = [	self.queue[0][i], self.queue[0][i+1], self.queue[0][i+2],
						self.queue[1][i], self.queue[1][i+1], self.queue[1][i+2],
						self.queue[2][i], self.queue[2][i+1], self.queue[2][i+2]]
				mat.sort()
				median.append(mat[9 / 2])

			print (median)

	#def preprocessing(self):

		#for i in range(len(self.R) - 1):
			#if (self.R[i-1] == np.inf and self.R[i] != np.inf):

			#if (self.R[i] != np.inf and self.R[i+1] == np.inf):


		print("#######################################")
		print(self.R)
		print("#######################################")
		print(blocks)


if __name__ == '__main__':
	l = lidar()
