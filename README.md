# energytank
# Variable Stiffness Controllers with Energy Tank

基于能量罐（Energy Tank）的笛卡尔空间变阻抗控制器，适用于 **Franka Emika Panda** 机械臂。
##  1.文件结构

```
src/variable_stiffness_controllers/
├── include/
│   ├── icvs_energy.h           # 障碍函数能量罐控制器头文件
│   └── franka_utils/           # 解析动力学模型（Mass/Coriolis/Gravity）
├── src/
│   ├── icvs_energy.cpp         # 障碍函数能量罐实现
│   ├── MassMatrix.cpp          # Panda 质量矩阵 M(q)
│   ├── CoriolisMatrix.cpp      # Panda 科氏力矩阵 C(q, q̇)
│   ├── GravityVector.cpp       # Panda 重力向量 G(q)
│   └── FrictionTorque.cpp      # Panda 摩擦力矩 τ_f(q̇)
├── config/
│   ├── variable_stiffness_energy.yaml   # icvs_energy 参数
├── launch/
│   ├── variable_stiffness_energy.launch # 启动障碍函数能量罐
│   └── test.launch                      # 启动gazebo仿真测试
├── msg/
│   └── compliance_robot.msg    # 自定义发布消息（位姿/误差/刚度/能量罐状态）
├──scripts/
│   ├──franka_to_geometry_messages.py  # 将 FrankaState 转为 PoseStamped（RViz用）
│   └──printdata.py                    # 打印实验数据并绘图    
```

---

## 2 编译与运行

### 2.1 编译

```bash
cd ~/energytank_ws
catkin_make 
source devel/setup.bash
```
### 2.2 启动障碍函数能量罐（icvs_energy）

```bash
roslaunch variable_stiffness_controllers variable_stiffness_energy.launch 
```


## 3 参考文献

FERRAGUTI F, SECCHI C, FANTUZZI C. A tank-based approach to impedance control
with variable stiffness[C]//Proc. IEEE Int. Conf. Robot. Automat. 2013: 4948-4953.
