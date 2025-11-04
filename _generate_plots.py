from mcap.reader import make_reader
from mcap_ros2.decoder import DecoderFactory
import matplotlib.pyplot as plt
import numpy as np

mcap_file = "bag_file/robot_1_quad_log_spirit_20251008_1525_0.mcap"

#helper functions for plotting joint, foot, and quaternion data
def plot_joint_data(datasets, timestamps, joint_names):
    for title, data, ylabel in datasets:
        fig, axes = plt.subplots(4, 3, figsize=(15, 12))
        fig.suptitle(title, fontsize=16, fontweight='bold')
        for i, (ax, name) in enumerate(zip(axes.flat, joint_names)):
            ax.plot(timestamps, data[:, i], linewidth=1.5)
            ax.set_title(name, fontsize=10, fontweight='bold')
            ax.set_xlabel('Time (s)', fontsize=8)
            ax.set_ylabel(ylabel, fontsize=8)
            ax.grid(True, alpha=0.3)
        plt.tight_layout()

def plot_foot_data(title, datasets, timestamps, feet_labels, axes_labels, colors):
    fig, axes = plt.subplots(4, 3, figsize=(15, 10), sharex=True)
    fig.suptitle(title, fontsize=16, fontweight='bold')
    for foot_idx in range(4):
        for axis_idx, (data, label, color) in enumerate(zip(datasets, axes_labels, colors)):
            axes[foot_idx, axis_idx].plot(timestamps, data[:, foot_idx], color=color)
            if foot_idx == 0:
                axes[foot_idx, axis_idx].set_title(label)
            if axis_idx == 0:
                axes[foot_idx, axis_idx].set_ylabel(feet_labels[foot_idx])
    plt.tight_layout()

def plot_quaternion_data(title, timestamps, data):
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    labels = ['qx', 'qy', 'qz']
    for i, label in enumerate(labels):
        axs[i].plot(timestamps, data[:, i], label=label)
        axs[i].set_ylabel(f"{label} (radians)")
        axs[i].legend(loc='upper right')
        axs[i].grid(True)
    axs[-1].set_xlabel("Time (s)")
    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.97])



def generate_all_plots(mcap_file_path):
    #initialize all variables
    timestamps = []

    joint_angle_data = []
    joint_velocity_data = []
    joint_effort_data = []

    pos_foot_x = []
    pos_foot_y = []
    pos_foot_z = []

    vel_foot_x = []
    vel_foot_y = []
    vel_foot_z = []
    
    pos_body_x = []
    pos_body_y = []
    pos_body_z = []

    linear_quaternion_data = [] 
    angular_quaternion_data = [] 

    # Read the MCAP file
    with open(mcap_file_path, "rb") as f:
        reader = make_reader(f, decoder_factories=[DecoderFactory()])
        for schema, channel, message, ros_msg in reader.iter_decoded_messages(topics=["/robot_1/state/ground_truth"]):
            timestamp = message.log_time / 1e9
            timestamps.append(timestamp)

            joint_angle_data.append(ros_msg.joints.position) 
            joint_velocity_data.append(ros_msg.joints.velocity) 
            joint_effort_data.append(ros_msg.joints.effort) 

            pos_foot_x.append([foot.position.x for foot in ros_msg.feet.feet])
            pos_foot_y.append([foot.position.y for foot in ros_msg.feet.feet])
            pos_foot_z.append([foot.position.z for foot in ros_msg.feet.feet])

            vel_foot_x.append([foot.velocity.x for foot in ros_msg.feet.feet])
            vel_foot_y.append([foot.velocity.y for foot in ros_msg.feet.feet])
            vel_foot_z.append([foot.velocity.z for foot in ros_msg.feet.feet])

            # Body pose
            pos_body_x.append(ros_msg.body.pose.position.x)
            pos_body_y.append(ros_msg.body.pose.position.y)
            pos_body_z.append(ros_msg.body.pose.position.z)


            linear_q = ros_msg.body.twist.linear
            linear_quaternion_data.append([linear_q.x, linear_q.y, linear_q.z])
            angular_q = ros_msg.body.twist.angular
            angular_quaternion_data.append([angular_q.x, angular_q.y, angular_q.z])

    timestamps = np.array(timestamps)
    timestamps = timestamps - timestamps[0]

    joint_angle_data = np.array(joint_angle_data)
    joint_velocity_data = np.array(joint_velocity_data)
    joint_effort_data = np.array(joint_effort_data)

    pos_foot_x = np.array(pos_foot_x)
    pos_foot_y = np.array(pos_foot_y)
    pos_foot_z = np.array(pos_foot_z)

    vel_foot_x = np.array(vel_foot_x)
    vel_foot_y = np.array(vel_foot_y)
    vel_foot_z = np.array(vel_foot_z)
    
    pos_body_x = np.array(pos_body_x)
    pos_body_y = np.array(pos_body_y)
    pos_body_z = np.array(pos_body_z)
    body_position_data = np.array([pos_body_x, pos_body_y, pos_body_z])
    feet_position_data = np.array([pos_foot_x, pos_foot_y, pos_foot_z])

    linear_quaternion_data = np.array(linear_quaternion_data)
    angular_quaternion_data = np.array(angular_quaternion_data)

    joint_names = [
    'FL_Abd', 'FL_Hip', 'FL_Knee',
    'BL_Abd', 'BL_Hip', 'BL_Knee',
    'FR_Abd', 'FR_Hip', 'FR_Knee',
    'BR_Abd', 'BR_Hip', 'BR_Knee'
    ]
 
    joint_datasets = [
        ("Individual Joint Position", joint_angle_data, "Position (rad)"),
        ("Individual Joint Velocity", joint_velocity_data, "Velocity (rad/s)"),
        ("Individual Joint Effort", joint_effort_data, "Effort (Newtons)")
    ]
    plot_joint_data(joint_datasets, timestamps, joint_names)


    feet_labels = ['Front Left', 'Front Right', 'Rear Left', 'Rear Right']
    axes_labels = ['X Position (m)', 'Y Position (m)', 'Z Position (m)']
    colors = ['blue', 'red', 'green']

    plot_foot_data("Foot Position Over Time (X, Y, Z per Foot)",
                [pos_foot_x, pos_foot_y, pos_foot_z],
                timestamps, feet_labels, axes_labels, colors)

    plot_foot_data("Foot Velocity Over Time (X, Y, Z per Foot)",
                [vel_foot_x, vel_foot_y, vel_foot_z],
                timestamps, feet_labels, axes_labels, colors)
    
    plot_quaternion_data("Linear Body Orientation (Quaternion Components)", timestamps, linear_quaternion_data)
    plot_quaternion_data("Angular Body Orientation (Quaternion Components)", timestamps, angular_quaternion_data)


    #Plot body and foot trajectories in 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(projection="3d")
    ax.set_box_aspect([2, 1, 1])

    x_min, x_max = np.min(feet_position_data[0]), np.max(feet_position_data[0])
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-1.0, 1.0)
    ax.set_zlim(0.0, 1.0)

    ax.plot(*body_position_data[:3], color="black", linewidth=2, label="Body")

    foot_labels = ["Front Left (FL)", "Back Left (BL)", "Front Right (FR)", "Back Right (BR)"]
    for i, label in enumerate(foot_labels):
        ax.plot(feet_position_data[0, :, i], feet_position_data[1, :, i],
                feet_position_data[2, :, i], label=label)

    ax.legend(loc="upper right")
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.set_zlabel("Z [m]")
    ax.set_title("Body and Feet Trajectories")

    plt.show()

    
generate_all_plots(mcap_file)