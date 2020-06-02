cmake_minimum_required(VERSION 3.0.2)
project(talker)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  lib_node
)

catkin_package(
  CATKIN_DEPENDS lib_node
)

include_directories(
  ${catkin_INCLUDE_DIRS}
  include
)

add_executable( talker src/main.cpp)
target_link_libraries(talker ${catkin_LIBRARIES} )
