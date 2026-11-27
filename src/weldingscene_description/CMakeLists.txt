cmake_minimum_required(VERSION 3.8)
project(weldingscene_description)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
  FILES_MATCHING PATTERN "*.launch.py"
  PATTERN "__pycache__" EXCLUDE
)
install(DIRECTORY urdf meshes rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
