cmake_minimum_required(VERSION 2.8.3)
project(lidar)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  laser_geometry
)

catkin_package(

)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_library(lidar_lib include/lidar.h src/lidar.cpp)
add_executable(lidar src/main.cpp)
target_link_libraries(lidar lidar_lib ${catkin_LIBRARIES})
