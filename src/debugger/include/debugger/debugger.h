#include "iostream"
#include "std_msgs/String.h"
#include <fstream>
#include <ros/package.h>
#include <ros/ros.h>
#include <time.h>

using namespace std;

class Debugger {
public:
  Debugger(ros::NodeHandle, string, string);
  void debug(string);

private:
  ros::NodeHandle nh;
  ros::Publisher pub;
  string pkgName;
  string nodeName;
  string logFileName;
  std_msgs::String msg;
};
