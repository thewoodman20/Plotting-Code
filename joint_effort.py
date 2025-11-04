from mcap.reader import make_reader
from mcap_ros2.decoder import DecoderFactory
import matplotlib.pyplot as plt
import numpy as np


def plot_joint_effort(mcap_file_path):
    timestamps = []
    joint_effort_data = []
    
    # Read the MCAP file
    with open(mcap_file_path, "rb") as f:
        reader = make_reader(f, decoder_factories=[DecoderFactory()])

        #loop takes all messages in the estimate topic and appends it to a variable for plotting
        for schema, channel, message, ros_msg in reader.iter_decoded_messages(topics=["/robot_1/state/ground_truth"]): 
            timestamp = message.log_time / 1e9
            timestamps.append(timestamp)
            joint_effort_data.append(ros_msg.joints.effort) 

    timestamps = np.array(timestamps)
    joint_effort_data = np.array(joint_effort_data) 
    timestamps = timestamps - timestamps[0]
    
    joint_names = [
        'FL_Abd', 'FL_Hip', 'FL_Knee',
        'BL_Abd', 'BL_Hip', 'BL_Knee',
        'FR_Abd', 'FR_Hip', 'FR_Knee',
        'BR_Abd', 'BR_Hip', 'BR_Knee'
    ]
    
    # Create 12 subplots
    fig, axes = plt.subplots(4, 3, figsize=(15, 12))
    fig.suptitle('Individual Joint Effort', fontsize=16, fontweight='bold')
    for i, (ax, name) in enumerate(zip(axes.flat, joint_names)):
        ax.plot(timestamps, joint_effort_data[:, i], linewidth=1.5)
        ax.set_title(name, fontsize=10, fontweight='bold')
        ax.set_xlabel('Time (s)', fontsize=8)
        ax.set_ylabel('Effort (Newtons)', fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.show()


if __name__ == "__main__":
    mcap_file = "bag_file/robot_1_quad_log_spirit_20251008_1525_0.mcap"
    plot_joint_effort(mcap_file)