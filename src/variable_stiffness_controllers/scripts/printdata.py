# #!/usr/bin/env python3
# import rospy
# import numpy as np
# import matplotlib.pyplot as plt
# import csv
# import os
# from datetime import datetime
# from variable_stiffness_controllers.msg import compliance_robot

# class EnergyTankDataCollector:
#     def __init__(self):
#         rospy.init_node('energy_tank_data_collector', anonymous=True)
        
#         # 数据存储列表
#         self.time_data = []
#         self.stiffness_data = []
#         self.desired_stiffness_data = []  # 期望刚度
#         self.torque_data = [[] for _ in range(7)]  # 7个关节力矩
#         self.y_error_data = []
#         self.z_error_data = []
#         self.tank_energy_data = []
        
#         # 订阅话题
#         rospy.Subscriber("/robotNew", compliance_robot, self.callback)
        
#         # 数据保存路径
#         self.save_dir = os.path.join(os.path.expanduser("~"), "energy_tank_data")
#         if not os.path.exists(self.save_dir):
#             os.makedirs(self.save_dir)
        
#         # 时间戳用于文件名
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         self.csv_file = os.path.join(self.save_dir, f"energy_tank_data_{timestamp}.csv")
        
#         # 初始化CSV文件
#         with open(self.csv_file, 'w', newline='') as f:
#             writer = csv.writer(f)
#             headers = ['Time', 'Stiffness', 'Desired_Stiffness', 'Tank_Energy'] + \
#                      [f'Torque_Joint_{i+1}' for i in range(7)] + \
#                      ['Y_Error', 'Z_Error']
#             writer.writerow(headers)
        
#         rospy.loginfo("Energy Tank Data Collector initialized. Saving data to: " + self.csv_file)
    
#     def callback(self, msg):
#         # 获取当前时间
#         current_time = rospy.get_time()
        
#         # 如果是第一次记录，记录起始时间
#         if not self.time_data:
#             self.start_time = current_time
        
#         # 存储相对时间
#         relative_time = current_time - self.start_time
#         self.time_data.append(relative_time)
#         self.stiffness_data.append(msg.kd)
#         self.desired_stiffness_data.append(msg.k_desire)
#         self.tank_energy_data.append(msg.s[0])
        
#         # 存储7个关节力矩
#         for i in range(7):
#             self.torque_data[i].append(msg.taud[i])
        
#         # 存储 Y / Z 方向位置误差
#         if len(msg.positionerror) >= 3:
#             self.y_error_data.append(msg.positionerror[1])
#             self.z_error_data.append(msg.positionerror[2])
        
#         # 实时保存 CSV
#         with open(self.csv_file, 'a', newline='') as f:
#             writer = csv.writer(f)
#             row = [relative_time, msg.kd, msg.k_desire, msg.s[0]] + \
#                   [msg.taud[i] for i in range(7)] + \
#                   [msg.positionerror[1], msg.positionerror[2]]
#             writer.writerow(row)
    
#     def plot_data(self):
#         if not self.time_data:
#             rospy.logwarn("No data collected for plotting")
#             return
        
#         time_array = np.array(self.time_data)
        
#         # 创建2x2布局
#         fig, axs = plt.subplots(2, 2, figsize=(16, 12))
#         fig.suptitle('Energy Tank Controller Performance Analysis', fontsize=16, fontweight='bold')
        
#         colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', 
#                  '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
        
#         # (a) 刚度 vs 时间
#         axs[0, 0].plot(time_array, self.stiffness_data, linewidth=2.5, label='Actual Stiffness')
#         axs[0, 0].plot(time_array, self.desired_stiffness_data, linestyle='--', linewidth=2, label='Desired Stiffness')
#         axs[0, 0].set_xlabel('Time (s)')
#         axs[0, 0].set_ylabel('Stiffness (N/m)')
#         axs[0, 0].set_title('(a) Energy Tank Stiffness vs Time')
#         axs[0, 0].grid(True, linestyle='--', alpha=0.7)
#         axs[0, 0].legend()
        
#         # 刚度统计
#         stiffness_error = np.array(self.desired_stiffness_data) - np.array(self.stiffness_data)
#         stats_text = f'Avg Actual: {np.mean(self.stiffness_data):.2f} N/m\n' \
#                     f'Avg Desired: {np.mean(self.desired_stiffness_data):.2f} N/m\n' \
#                     f'RMS Error: {np.sqrt(np.mean(stiffness_error**2)):.2f} N/m'
#         axs[0, 0].text(0.02, 0.98, stats_text, transform=axs[0, 0].transAxes,
#                       fontsize=10, verticalalignment='top',
#                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
#         # (b) 能量罐
#         axs[0, 1].plot(time_array, self.tank_energy_data, linewidth=2.5)
#         axs[0, 1].set_xlabel('Time (s)')
#         axs[0, 1].set_ylabel('Tank Energy')
#         axs[0, 1].set_title('(b) Energy Tank Level vs Time')
#         axs[0, 1].grid(True, linestyle='--', alpha=0.7)
        
#         energy_stats = f'Avg: {np.mean(self.tank_energy_data):.2f}\n' \
#                        f'Max: {np.max(self.tank_energy_data):.2f}\n' \
#                        f'Min: {np.min(self.tank_energy_data):.2f}'
#         axs[0, 1].text(0.02, 0.98, energy_stats, transform=axs[0, 1].transAxes,
#                       fontsize=10, verticalalignment='top',
#                       bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
#         # (c) 关节力矩
#         for i in range(7):
#             axs[1, 0].plot(time_array, self.torque_data[i], label=f'Joint {i+1}')
#         axs[1, 0].set_xlabel('Time (s)')
#         axs[1, 0].set_ylabel('Torque (Nm)')
#         axs[1, 0].set_title('(c) Joint Torques vs Time')
#         axs[1, 0].grid(True, linestyle='--', alpha=0.7)
#         axs[1, 0].legend(ncol=2, fontsize=9)
        
#         # (d) Y/Z 跟踪误差
#         if self.y_error_data and self.z_error_data:
#             axs[1, 1].plot(time_array, self.y_error_data, linewidth=2, label='Y Error')
#             axs[1, 1].plot(time_array, self.z_error_data, linestyle='--', linewidth=2, label='Z Error')
#             axs[1, 1].set_xlabel('Time (s)')
#             axs[1, 1].set_ylabel('Position Error (m)')
#             axs[1, 1].set_title('(d) End-Effector Tracking Error (Y/Z)')
#             axs[1, 1].grid(True, linestyle='--', alpha=0.7)
#             axs[1, 1].legend()
            
#             rms_y = np.sqrt(np.mean(np.square(self.y_error_data)))
#             rms_z = np.sqrt(np.mean(np.square(self.z_error_data)))
#             max_y = np.max(np.abs(self.y_error_data))
#             max_z = np.max(np.abs(self.z_error_data))
            
#             stats_text = f'RMS Y Error: {rms_y:.4f} m\n' \
#                         f'RMS Z Error: {rms_z:.4f} m\n' \
#                         f'Max |Y| Error: {max_y:.4f} m\n' \
#                         f'Max |Z| Error: {max_z:.4f} m'
            
#             axs[1, 1].text(0.02, 0.98, stats_text, transform=axs[1, 1].transAxes,
#                           fontsize=10, verticalalignment='top',
#                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
#         plt.tight_layout(rect=[0, 0, 1, 0.96])
        
#         plot_file = os.path.join(self.save_dir, f"energy_tank_plots_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
#         plt.savefig(plot_file, dpi=300, bbox_inches='tight')
#         plt.show()
        
#         rospy.loginfo(f"Plots saved to: {plot_file}")
#         rospy.loginfo(f"Data saved to: {self.csv_file}")
    
#     def run(self):
#         rospy.loginfo("Starting data collection... Press Ctrl+C to stop and plot.")
#         try:
#             rospy.spin()
#         except KeyboardInterrupt:
#             rospy.loginfo("Data collection stopped by user")
        
#         self.plot_data()
#         self.print_statistics()
    
#     def print_statistics(self):
#         if not self.time_data:
#             return
        
#         print("\n" + "="*60)
#         print("ENERGY TANK CONTROLLER DATA STATISTICS")
#         print("="*60)
#         print(f"Total data points: {len(self.time_data)}")
#         print(f"Time duration: {self.time_data[-1]:.2f} seconds")
#         print(f"Sampling rate: {len(self.time_data)/self.time_data[-1]:.2f} Hz")
        
#         print("\nStiffness Statistics (N/m):")
#         print(f"  Actual Avg: {np.mean(self.stiffness_data):.2f}")
#         print(f"  Desired Avg: {np.mean(self.desired_stiffness_data):.2f}")
        
#         stiffness_error = np.array(self.desired_stiffness_data) - np.array(self.stiffness_data)
#         print(f"  RMS Error: {np.sqrt(np.mean(stiffness_error**2)):.2f}")
        
#         print("\nEnergy Tank Statistics:")
#         print(f"  Avg Energy: {np.mean(self.tank_energy_data):.2f}")
#         print(f"  Max Energy: {np.max(self.tank_energy_data):.2f}")
#         print(f"  Min Energy: {np.min(self.tank_energy_data):.2f}")
        
#         if self.y_error_data and self.z_error_data:
#             print("\nTracking Error Statistics (m):")
#             print(f"  RMS Y Error: {np.sqrt(np.mean(np.square(self.y_error_data))):.4f}")
#             print(f"  RMS Z Error: {np.sqrt(np.mean(np.square(self.z_error_data))):.4f}")
#             print(f"  Max |Y| Error: {np.max(np.abs(self.y_error_data)):.4f}")
#             print(f"  Max |Z| Error: {np.max(np.abs(self.z_error_data)):.4f}")
        
#         print("\nJoint Torque Statistics (Nm):")
#         print("  Joint |   Mean   |   Std    |   Max    |   Min    |   RMS    |")
#         print("  " + "-"*60)
#         for i in range(7):
#             mean_torque = np.mean(self.torque_data[i])
#             std_torque = np.std(self.torque_data[i])
#             max_torque = np.max(self.torque_data[i])
#             min_torque = np.min(self.torque_data[i])
#             rms_torque = np.sqrt(np.mean(np.square(self.torque_data[i])))
#             print(f"    {i+1}    | {mean_torque:8.3f} | {std_torque:8.3f} | {max_torque:8.3f} | {min_torque:8.3f} | {rms_torque:8.3f} |")
        
#         print("="*60)

# if __name__ == '__main__':
#     try:
#         collector = EnergyTankDataCollector()
#         collector.run()
#     except rospy.ROSInterruptException:
#         pass



#!/usr/bin/env python3
import rospy
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime
from variable_stiffness_controllers.msg import compliance_robot

class EnergyTankDataCollector:
    def __init__(self):
        rospy.init_node('energy_tank_data_collector', anonymous=True)
        
        # 数据存储列表
        self.time_data = []
        self.stiffness_data = []
        self.desired_stiffness_data = []  # 期望刚度
        self.torque_data = [[] for _ in range(7)]  # 7个关节力矩
        self.x_error_data = []   # X方向误差
        self.y_error_data = []   # Y方向误差
        self.z_error_data = []   # Z方向误差
        self.l2_error_data = []  # L2范数误差
        self.tank_energy_data = []
        
        # 订阅话题
        rospy.Subscriber("/robotNew", compliance_robot, self.callback)
        
        # 数据保存路径
        self.save_dir = os.path.join(os.path.expanduser("~"), "energy_tank_data")
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        # 时间戳用于文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csv_file = os.path.join(self.save_dir, f"energy_tank_data_{timestamp}.csv")
        
        # 初始化CSV文件，包含X, Y, Z误差和L2范数
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            headers = ['Time', 'Stiffness', 'Desired_Stiffness', 'Tank_Energy'] + \
                     [f'Torque_Joint_{i+1}' for i in range(7)] + \
                     ['X_Error', 'Y_Error', 'Z_Error', 'L2_Norm_Error']
            writer.writerow(headers)
        
        rospy.loginfo("Energy Tank Data Collector initialized. Saving data to: " + self.csv_file)
    
    def callback(self, msg):
        # 获取当前时间
        current_time = rospy.get_time()
        
        # 如果是第一次记录，记录起始时间
        if not self.time_data:
            self.start_time = current_time
        
        # 存储相对时间
        relative_time = current_time - self.start_time
        self.time_data.append(relative_time)
        self.stiffness_data.append(msg.kd)
        self.desired_stiffness_data.append(msg.k_desire)
        self.tank_energy_data.append(msg.s[0])
        
        # 存储7个关节力矩
        for i in range(7):
            self.torque_data[i].append(msg.taud[i])
        
        # 存储 X, Y, Z 三个方向的位置误差，并计算 L2 范数
        if len(msg.positionerror) >= 3:
            x_err = msg.positionerror[0]
            y_err = msg.positionerror[1]
            z_err = msg.positionerror[2]
            self.x_error_data.append(x_err)
            self.y_error_data.append(y_err)
            self.z_error_data.append(z_err)
            l2_norm = np.sqrt(x_err**2 + y_err**2 + z_err**2)
            self.l2_error_data.append(l2_norm)
        else:
            # 如果消息中没有足够的误差数据，填充默认值
            self.x_error_data.append(0.0)
            self.y_error_data.append(0.0)
            self.z_error_data.append(0.0)
            self.l2_error_data.append(0.0)
        
        # 实时保存 CSV（包含X, Y, Z误差和L2范数）
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            row = [relative_time, msg.kd, msg.k_desire, msg.s[0]] + \
                  [msg.taud[i] for i in range(7)] + \
                  [self.x_error_data[-1], self.y_error_data[-1], 
                   self.z_error_data[-1], self.l2_error_data[-1]]
            writer.writerow(row)
    
    def plot_data(self):
        if not self.time_data:
            rospy.logwarn("No data collected for plotting")
            return
        
        time_array = np.array(self.time_data)
        
        # 创建2x2布局
        fig, axs = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Energy Tank Controller Performance Analysis', fontsize=16, fontweight='bold')
        
        # (a) 刚度 vs 时间
        axs[0, 0].plot(time_array, self.stiffness_data, linewidth=2.5, label='Actual Stiffness')
        axs[0, 0].plot(time_array, self.desired_stiffness_data, linestyle='--', linewidth=2, label='Desired Stiffness')
        axs[0, 0].set_xlabel('Time (s)')
        axs[0, 0].set_ylabel('Stiffness (N/m)')
        axs[0, 0].set_title('(a) Energy Tank Stiffness vs Time')
        axs[0, 0].grid(True, linestyle='--', alpha=0.7)
        axs[0, 0].legend()
        
        # 刚度统计
        stiffness_error = np.array(self.desired_stiffness_data) - np.array(self.stiffness_data)
        stats_text = f'Avg Actual: {np.mean(self.stiffness_data):.2f} N/m\n' \
                    f'Avg Desired: {np.mean(self.desired_stiffness_data):.2f} N/m\n' \
                    f'RMS Error: {np.sqrt(np.mean(stiffness_error**2)):.2f} N/m'
        axs[0, 0].text(0.02, 0.98, stats_text, transform=axs[0, 0].transAxes,
                      fontsize=10, verticalalignment='top',
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # (b) 能量罐
        axs[0, 1].plot(time_array, self.tank_energy_data, linewidth=2.5)
        axs[0, 1].set_xlabel('Time (s)')
        axs[0, 1].set_ylabel('Tank Energy')
        axs[0, 1].set_title('(b) Energy Tank Level vs Time')
        axs[0, 1].grid(True, linestyle='--', alpha=0.7)
        
        energy_stats = f'Avg: {np.mean(self.tank_energy_data):.2f}\n' \
                       f'Max: {np.max(self.tank_energy_data):.2f}\n' \
                       f'Min: {np.min(self.tank_energy_data):.2f}'
        axs[0, 1].text(0.02, 0.98, energy_stats, transform=axs[0, 1].transAxes,
                      fontsize=10, verticalalignment='top',
                      bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        # (c) 关节力矩
        for i in range(7):
            axs[1, 0].plot(time_array, self.torque_data[i], label=f'Joint {i+1}')
        axs[1, 0].set_xlabel('Time (s)')
        axs[1, 0].set_ylabel('Torque (Nm)')
        axs[1, 0].set_title('(c) Joint Torques vs Time')
        axs[1, 0].grid(True, linestyle='--', alpha=0.7)
        axs[1, 0].legend(ncol=2, fontsize=9)
        
        # (d) 三维位置误差的 L2 范数
        if self.l2_error_data:
            axs[1, 1].plot(time_array, self.l2_error_data, linewidth=2, color='#d62728')
            axs[1, 1].set_xlabel('Time (s)')
            axs[1, 1].set_ylabel('L2 Norm of Position Error (m)')
            axs[1, 1].set_title('(d) End-Effector Tracking Error (3D L2 Norm)')
            axs[1, 1].grid(True, linestyle='--', alpha=0.7)
            
            rms_l2 = np.sqrt(np.mean(np.square(self.l2_error_data)))
            max_l2 = np.max(self.l2_error_data)
            min_l2 = np.min(self.l2_error_data)
            stats_text = f'RMS L2 Error: {rms_l2:.4f} m\n' \
                         f'Max L2 Error: {max_l2:.4f} m\n' \
                         f'Min L2 Error: {min_l2:.4f} m'
            axs[1, 1].text(0.02, 0.98, stats_text, transform=axs[1, 1].transAxes,
                          fontsize=10, verticalalignment='top',
                          bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
        plot_file = os.path.join(self.save_dir, f"energy_tank_plots_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        plt.show()
        
        rospy.loginfo(f"Plots saved to: {plot_file}")
        rospy.loginfo(f"Data saved to: {self.csv_file}")
    
    def run(self):
        rospy.loginfo("Starting data collection... Press Ctrl+C to stop and plot.")
        try:
            rospy.spin()
        except KeyboardInterrupt:
            rospy.loginfo("Data collection stopped by user")
        
        self.plot_data()
        self.print_statistics()
    
    def print_statistics(self):
        if not self.time_data:
            return
        
        print("\n" + "="*60)
        print("ENERGY TANK CONTROLLER DATA STATISTICS")
        print("="*60)
        print(f"Total data points: {len(self.time_data)}")
        print(f"Time duration: {self.time_data[-1]:.2f} seconds")
        print(f"Sampling rate: {len(self.time_data)/self.time_data[-1]:.2f} Hz")
        
        print("\nStiffness Statistics (N/m):")
        print(f"  Actual Avg: {np.mean(self.stiffness_data):.2f}")
        print(f"  Desired Avg: {np.mean(self.desired_stiffness_data):.2f}")
        
        stiffness_error = np.array(self.desired_stiffness_data) - np.array(self.stiffness_data)
        print(f"  RMS Error: {np.sqrt(np.mean(stiffness_error**2)):.2f}")
        
        print("\nEnergy Tank Statistics:")
        print(f"  Avg Energy: {np.mean(self.tank_energy_data):.2f}")
        print(f"  Max Energy: {np.max(self.tank_energy_data):.2f}")
        print(f"  Min Energy: {np.min(self.tank_energy_data):.2f}")
        
        if self.x_error_data and self.y_error_data and self.z_error_data and self.l2_error_data:
            print("\nTracking Error Statistics (3D):")
            print(f"  X Error RMS: {np.sqrt(np.mean(np.square(self.x_error_data))):.4f} m")
            print(f"  Y Error RMS: {np.sqrt(np.mean(np.square(self.y_error_data))):.4f} m")
            print(f"  Z Error RMS: {np.sqrt(np.mean(np.square(self.z_error_data))):.4f} m")
            print(f"  L2 Norm RMS: {np.sqrt(np.mean(np.square(self.l2_error_data))):.4f} m")
            print(f"  Max L2 Error: {np.max(self.l2_error_data):.4f} m")
            print(f"  Min L2 Error: {np.min(self.l2_error_data):.4f} m")
        
        print("\nJoint Torque Statistics (Nm):")
        print("  Joint |   Mean   |   Std    |   Max    |   Min    |   RMS    |")
        print("  " + "-"*60)
        for i in range(7):
            mean_torque = np.mean(self.torque_data[i])
            std_torque = np.std(self.torque_data[i])
            max_torque = np.max(self.torque_data[i])
            min_torque = np.min(self.torque_data[i])
            rms_torque = np.sqrt(np.mean(np.square(self.torque_data[i])))
            print(f"    {i+1}    | {mean_torque:8.3f} | {std_torque:8.3f} | {max_torque:8.3f} | {min_torque:8.3f} | {rms_torque:8.3f} |")
        
        print("="*60)

if __name__ == '__main__':
    try:
        collector = EnergyTankDataCollector()
        collector.run()
    except rospy.ROSInterruptException:
        pass