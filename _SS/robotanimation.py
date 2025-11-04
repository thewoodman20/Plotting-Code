from mcap.reader import make_reader
from mcap_ros2.decoder import DecoderFactory
import matplotlib.pyplot as plt
import numpy as np
from urdfpy import URDF #different library for loading in the URDF file 

def robot_animation_with_trajectories(mcap_file_path, robot_urdf_file):
    timestamps = []
    x_body_pos_data = []
    y_body_pos_data = []
    z_body_pos_data = []
    pos_foot_x = []
    pos_foot_y = []
    pos_foot_z = []

    # Read MCAP file once for both body and feet data
    with open(mcap_file_path, "rb") as f:
        reader = make_reader(f, decoder_factories=[DecoderFactory()])
        for schema, channel, message, ros_msg in reader.iter_decoded_messages(topics=["/robot_1/state/estimate"]):
            timestamp = message.log_time / 1e9
            timestamps.append(timestamp)

            # Body pose
            x_body_pos_data.append(ros_msg.body.pose.position.x)
            y_body_pos_data.append(ros_msg.body.pose.position.y)
            z_body_pos_data.append(ros_msg.body.pose.position.z)

            # Feet poses
            pos_foot_x.append([foot.position.x for foot in ros_msg.feet.feet])
            pos_foot_y.append([foot.position.y for foot in ros_msg.feet.feet])
            pos_foot_z.append([foot.position.z for foot in ros_msg.feet.feet])

    # Convert to numpy arrays
    timestamps = np.array(timestamps)
    timestamps = timestamps - timestamps[0]
    body_position_data = np.array([x_body_pos_data, y_body_pos_data, z_body_pos_data])
    feet_position_data = np.array([pos_foot_x, pos_foot_y, pos_foot_z])

    # Create single 3D figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(projection="3d")
    ax.set_box_aspect([2, 1, 1])

    # Axis bounds
    x_min, x_max = np.min(feet_position_data[0]), np.max(feet_position_data[0])
    y_min, y_max = -1.0, 1.0
    z_min, z_max = 0.0, 1.0
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_zlim(z_min, z_max)

    # Plot body trajectory
    ax.plot(body_position_data[0], body_position_data[1], body_position_data[2], color="black", linewidth=2, label="Body")

    # Plot each foot trajectory
    foot_labels = ["Front Left (FL)", "Back Left (BL)", "Front Right (FR)", "Back Right (BR)"]
    for i in range(len(feet_position_data[1, 1, :])):
        ax.plot(feet_position_data[0, :, i], feet_position_data[1, :, i], feet_position_data[2, :, i], label=foot_labels[i])

    # Legend and labels
    ax.legend(loc="upper right")
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.set_zlabel("Z [m]")
    ax.set_title("Body and Feet Trajectories")



    #unpack the urdf and code animation
    robot = URDF.load(robot_urdf_file)





if __name__ == "__main__":
    mcap_file = "bag_file/robot_1_quad_log_spirit_20251008_1525_0.mcap"
    robot_urdf_file = "urdf/go2_description.urdf"
    robot_animation_with_trajectories(mcap_file, robot_urdf_file)
    plt.show()