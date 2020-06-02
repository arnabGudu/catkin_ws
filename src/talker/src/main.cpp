#include "ros/ros.h"
#include "std_msgs/String.h"
#include "lib_node/lib_node.h"

using namespace std;

int main(int argc, char** argv)
{
	lib_node ln;
	ln.print(argc);
}
