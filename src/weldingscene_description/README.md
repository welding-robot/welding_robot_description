# Welding robot RViz2 visualization

This package visualizes `urdf/weldingrobot.urdf.xacro` in RViz2. It uses the
UR5 and RealSense description packages in this workspace and publishes joint
states from the GUI sliders.

Build the packages from the workspace root after sourcing your ROS 2 setup:

```bash
colcon build --packages-up-to weldingscene_description
source install/setup.bash
ros2 launch weldingscene_description view_weldingrobot.launch.py
```

The launch starts `robot_state_publisher`, `joint_state_publisher_gui`, and
RViz2. To run without RViz2, pass `use_rviz:=false`; to use a simulation clock,
pass `use_sim_time:=true`.
