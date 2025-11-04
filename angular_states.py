from mcap.reader import make_reader
from mcap_ros2.decoder import DecoderFactory
import matplotlib.pyplot as plt
import numpy as np

def plot_angular_states(mcap_file_path):
    #read and decode body data
    timestamps = []
    quaternion_data = []

    with open(mcap_file_path, "rb") as f:
        reader = make_reader(f, decoder_factories=[DecoderFactory()])
        for schema, channel, message, ros_msg in reader.iter_decoded_messages(topics=["/robot_1/state/ground_truth"]):
            timestamp = message.log_time / 1e9
            timestamps.append(timestamp)

            q = ros_msg.body.twist.angular
            quaternion_data.append([q.x, q.y, q.z])

    timestamps = np.array(timestamps)
    quaternion_data = np.array(quaternion_data)
    timestamps = timestamps - timestamps[0]

    #plot body trajectory
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    labels = ['qx', 'qy', 'qz']
    for i in range(3):
        axs[i].plot(timestamps, quaternion_data[:, i], label=labels[i])
        axs[i].set_ylabel(f"{labels[i]} (radians)")
        axs[i].legend(loc='upper right')
        axs[i].grid(True)

    axs[-1].set_xlabel("Time (s)")
    fig.suptitle("Body Orientation (Quaternion Components)")
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()

if __name__ == "__main__":
    mcap_file = "bag_file/robot_1_quad_log_spirit_20251008_1525_0.mcap"
    plot_angular_states(mcap_file)
