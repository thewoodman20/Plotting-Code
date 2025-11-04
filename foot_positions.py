from mcap.reader import make_reader
from mcap_ros2.decoder import DecoderFactory
import matplotlib.pyplot as plt
import numpy as np

def plot_feet_positions(mcap_file_path):
    timestamps = []
    pos_foot_x = []
    pos_foot_y = []
    pos_foot_z = []
    
    # Read the MCAP file
    with open(mcap_file_path, "rb") as f:
        reader = make_reader(f, decoder_factories=[DecoderFactory()])
        for schema, channel, message, ros_msg in reader.iter_decoded_messages(topics=["/robot_1/state/ground_truth"]): 
            timestamp = message.log_time / 1e9
            timestamps.append(timestamp)
            
            # Extract positions for all 4 feet at this time step
            pos_foot_x.append([foot.position.x for foot in ros_msg.feet.feet])
            pos_foot_y.append([foot.position.y for foot in ros_msg.feet.feet])
            pos_foot_z.append([foot.position.z for foot in ros_msg.feet.feet])

    # Convert to numpy arrays
    timestamps = np.array(timestamps)
    timestamps = timestamps - timestamps[0]
    pos_foot_x = np.array(pos_foot_x)  # shape: (timesteps, 4)
    pos_foot_y = np.array(pos_foot_y)
    pos_foot_z = np.array(pos_foot_z)
    
    # Plot 12 subplots (4 feet × 3 axes)
    fig, axes = plt.subplots(4, 3, figsize=(15, 10), sharex=True)
    feet_labels = ['Front Left', 'Front Right', 'Rear Left', 'Rear Right']
    axes_labels = ['X Position (m)', 'Y Position (m)', 'Z Position (m)']
    colors = ['blue', 'red', 'green']

    for foot_idx in range(4):
        for axis_idx, (data, label, color) in enumerate(zip(
            [pos_foot_x, pos_foot_y, pos_foot_z],
            axes_labels,
            colors
        )):
            axes[foot_idx, axis_idx].plot(timestamps, data[:, foot_idx], color=color)
            if foot_idx == 0:
                axes[foot_idx, axis_idx].set_title(label)
            if axis_idx == 0:
                axes[foot_idx, axis_idx].set_ylabel(feet_labels[foot_idx])
    
    fig.suptitle('Foot Position Over Time (X, Y, Z per Foot)', fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.93)
    plt.show()


if __name__ == "__main__":
    mcap_file = "bag_file/robot_1_quad_log_spirit_20251008_1525_0.mcap"
    plot_feet_positions(mcap_file)
