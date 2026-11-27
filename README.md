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

## 4. 焊枪工具坐标系 TCP

场景通过固定关节 `welding_torch_to_tcp` 定义工具末端 `torch_tcp`：

```text
tool0
└── welding_torch
    └── torch_tcp
```

`torch_tcp` 是用于轨迹规划的空 link，由 `robot_state_publisher` 自动发布 TF。
RViz2 中的 `Torch TCP` 显示项单独显示它的坐标轴和名称：红色为 X，绿色为 Y，蓝色为 Z。

TCP 位姿在 `src/weldingscene_description/urdf/weldingrobot.urdf.xacro` 顶部，
通过修改 `torch_tcp_xyz`、`torch_tcp_rpy` 的 `default` 值设置，均相对于父坐标系 `welding_torch`：

| 参数 | 默认值 | 单位 |
| --- | --- | --- |
| `torch_tcp_xyz` | `0 0 0` | 米，按 X、Y、Z 排列 |
| `torch_tcp_rpy` | `0 -0.84997 -1.5707963267948966` | 弧度，按 roll、pitch、yaw 排列 |

默认位置取现有 STL 前端圆口的中心，默认 Z 轴沿前端轴线指向焊枪外侧，
X 轴位于焊枪弯曲平面内，Y 轴按右手规则确定。
这些值依据网格估算，尚未经过实物标定，也未包含焊丝伸出长度。
实际使用时，应明确工作点取接触嘴出口还是焊丝尖端，并替换为该工作点的标定位姿。
