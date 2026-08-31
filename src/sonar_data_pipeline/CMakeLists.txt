cmake_minimum_required(VERSION 3.8)
project(sonar_data_pipeline)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# Paste your executable and target dependency definitions here:
add_executable(sonar_publisher src/sonar_publisher.cpp)
ament_target_dependencies(sonar_publisher rclcpp std_msgs)

add_executable(sonar_subscriber src/sonar_subscriber.cpp)
ament_target_dependencies(sonar_subscriber rclcpp std_msgs)

install(TARGETS
  sonar_publisher
  sonar_subscriber
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()