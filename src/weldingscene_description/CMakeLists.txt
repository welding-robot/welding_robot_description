cmake_minimum_required(VERSION 3.8)
project(weldingscene_description)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
  FILES_MATCHING PATTERN "*.launch.py"
)
install(DIRECTORY urdf meshes
  DESTINATION share/${PROJECT_NAME}
)
install(FILES welding_support.rviz
  DESTINATION share/${PROJECT_NAME}/rviz
)

ament_package()
