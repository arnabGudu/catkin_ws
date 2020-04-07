#include "lidar.h"

void lidar::callback(const sensor_msgs::LaserScan::ConstPtr& scan)
{
    sensor_msgs::PointCloud cloud;
  	pr.projectLaser(*scan, cloud);
  	pub.publish(cloud);
}
