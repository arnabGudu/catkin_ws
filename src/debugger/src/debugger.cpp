#include "debugger/debugger.h"

Debugger::Debugger(ros::NodeHandle _nh, string package_name, 
string node_name) : nh(_nh) 
{
  pub = nh.advertise<std_msgs::String>("debud_data", 10, true);
  //logFileName = ros::package::getPath("logger") + "/log.txt";
  // std::ifstream confFile(logFileName.c_str());
  pkgName = package_name;
  nodeName = node_name;
}

void Debugger::debug(string _msg) {

  msg.data = _msg;
  /*ROS_INFO(msg);
  ofstream fileWrite;
  fileWrite.open(logFileName);
  fileWrite << ros::WallTime << " " << packageName << " " << nodeName << " "
            << msg;
  fileWrite.close();*/
  pub.publish(msg);
}
