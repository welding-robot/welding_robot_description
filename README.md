# welding_robot_description

UR5、RealSense D415、焊枪及支架的 ROS 2 描述与 RViz2 可视化。

## 1. 可视化 UR description

在已加载 ROS 2 环境的工作区根目录编译并加载工作区：

```bash
colcon build --symlink-install
source install/setup.bash
```

启动 UR5（默认模型）：

```bash
ros2 launch ur_description view_robot.launch.py
```

选择其他型号或关闭 RViz2：

```bash
ros2 launch ur_description view_robot.launch.py model:=ur3
ros2 launch ur_description view_robot.launch.py model:=ur10 limited:=false
ros2 launch ur_description view_robot.launch.py use_rviz:=false
```

## 2. 可视化 RealSense

```bash
ros2 launch realsense2_description view_camera_model.launch.py camera_model:=d415
```

## 3. 可视化焊接机器人场景

`weldingscene_description` 展示 UR5、末端安装的 RealSense D415、焊枪及支架，
依赖工作区中的 `ur_description` 和 `realsense2_description`。

目录结构：

```text
src/weldingscene_description/
├── CMakeLists.txt
├── package.xml
├── launch/
│   └── view_weldingrobot.launch.py
├── rviz/
│   └── welding_scene.rviz
├── urdf/
│   └── weldingrobot.urdf.xacro
└── meshes/
    └── torch/
        ├── torch.stl
        └── torch_support.stl
```

场景由 `src/weldingscene_description/urdf/weldingrobot.urdf.xacro` 组装。
显示和碰撞几何共用 `src/weldingscene_description/meshes/torch/` 中的网格，
RViz2 配置位于 `src/weldingscene_description/rviz/welding_scene.rviz`。

在已加载 ROS 2 环境的工作区根目录，仅编译场景及其依赖并启动：

```bash
colcon build --packages-up-to weldingscene_description
source install/setup.bash
ros2 launch weldingscene_description view_weldingrobot.launch.py
```

启动后会运行 `robot_state_publisher`、`joint_state_publisher_gui` 和 RViz2，
可通过 GUI 滑块调整关节状态。添加 `use_rviz:=false` 可关闭 RViz2，
添加 `use_sim_time:=true` 可使用仿真时钟。
