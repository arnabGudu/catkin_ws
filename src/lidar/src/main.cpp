#include "lidar.h"

int main(int argc, char** argv)
{
    ros::init(argc, argv, "lidar");
    lidar l;
    ros::spin();
    return 0;
}
