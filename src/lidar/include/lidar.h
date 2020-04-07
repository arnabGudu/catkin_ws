#include <ros/ros.h>
#include <laser_geometry/laser_geometry.h>

class lidar {
	public:
		lidar();
		void callback(const sensor_msgs::LaserScan::ConstPtr& scan);
	private:
		ros::NodeHandle nh;
		laser_geometry::LaserProjection pr;

		ros::Publisher pub;
		ros::Subscriber sub;
};

lidar::lidar()
{
    sub = nh.subscribe<sensor_msgs::LaserScan> ("/scan", 100, &lidar::callback, this);
    pub = nh.advertise<sensor_msgs::PointCloud> ("/cloud", 100, false);
}
