import rospy
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, LaserScan
from laser_geometry.laser_geometry import LaserProjection

lp = LaserProjection()
pub = rospy.Publisher("cloud", PointCloud2, queue_size=100)

def callback(data):
	cloud = lp.projectLaser(data)
	pub.publish(cloud)
	point_gen = pc2.read_points(cloud)
	
	for i, points in enumerate(point_gen):
		print(i, points)
	
def listener():
	rospy.init_node('lidar', anonymous=True)

	rospy.Subscriber("scan", LaserScan, callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
