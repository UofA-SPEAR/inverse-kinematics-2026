cmake_minimum_required(VERSION 3.8)
project(plex_arm_urdf)

find_package(ament_cmake REQUIRED)

install(DIRECTORY config urdf meshes launch textures
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
