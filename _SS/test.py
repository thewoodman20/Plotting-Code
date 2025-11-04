from urdfpy import URDF
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the URDF
robot = URDF.load('urdf/go2_description.urdf')

# Create a figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(0, 1.5)

# Plot a base frame or something static
ax.plot([0], [0], [0], 'ko')

# Function to draw the robot at a given configuration
def draw_robot(ax, q):
    ax.cla()
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(0, 1.5)
    points = []
    for link in robot.links:
        if link.visuals:
            # get the position of the link in world coordinates
            T = robot.link_fk(cfg=q)[link]
            p = T[:3, 3]
            points.append(p)
    points = np.array(points)
    ax.plot(points[:,0], points[:,1], points[:,2], 'o-', c='b')

# Generate some motion (simple joint trajectory)
n_frames = 100
q_traj = [np.sin(np.linspace(0, 2*np.pi, n_frames)) * 0.5 for _ in robot.actuated_joints]
q_traj = np.array(q_traj).T  # shape: (n_frames, n_joints)

# Animation function
def update(frame):
    q = {joint.name: q_traj[frame, i] for i, joint in enumerate(robot.actuated_joints)}
    draw_robot(ax, q)
    return ax,

anim = FuncAnimation(fig, update, frames=n_frames, interval=50, blit=False)
plt.show()














# import sys
# import struct
# import json
# import numpy as np
# import matplotlib.pyplot as plt
# from mcap.reader import make_reader
# from collections import defaultdict

# filepath = "bag_file/robot_1_quad_log_spirit_20251008_1525_0.mcap"

# # Dictionary to store schemas and channels
# schemas = {}
# channels = {}
# topic_data = defaultdict(list)
# topic_timestamps = defaultdict(list)
# topic_schemas = {}

# print("="*70)
# print("MCAP FILE ANALYSIS")
# print("="*70)

# # First pass: Read schemas and channels
# with open(filepath, "rb") as f:
#     reader = make_reader(f)
    
#     # Get schema information
#     for schema_id, schema in reader.get_summary().schemas.items():
#         schemas[schema_id] = schema
#         print(f"\n[Schema ID: {schema_id}]")
#         print(f"  Name: {schema.name}")
#         print(f"  Encoding: {schema.encoding}")
#         if schema.data:
#             print(f"  Definition length: {len(schema.data)} bytes")
#             # Try to decode schema definition
#             try:
#                 schema_text = schema.data.decode('utf-8')
#                 print(f"  Definition:\n{schema_text[:500]}")  # First 500 chars
#                 if len(schema_text) > 500:
#                     print(f"    ... ({len(schema_text) - 500} more characters)")
#             except:
#                 print(f"  Definition: (binary data)")
    
#     # Get channel information
#     for channel_id, channel in reader.get_summary().channels.items():
#         channels[channel_id] = channel
#         topic_schemas[channel.topic] = channel.schema_id

# print("\n" + "="*70)
# print("TOPICS AND THEIR SCHEMAS")
# print("="*70)

# # Group channels by topic
# topic_channels = defaultdict(list)
# for channel_id, channel in channels.items():
#     topic_channels[channel.topic].append(channel)

# for topic, topic_channel_list in sorted(topic_channels.items()):
#     print(f"\nTopic: {topic}")
#     for channel in topic_channel_list:
#         schema = schemas.get(channel.schema_id)
#         if schema:
#             print(f"  - Schema: {schema.name} (ID: {channel.schema_id})")
#             print(f"    Encoding: {schema.encoding}")

# # Second pass: Collect messages
# print("\n" + "="*70)
# print("COLLECTING MESSAGES")
# print("="*70)

# with open(filepath, "rb") as f:
#     reader = make_reader(f)
    
#     for schema, channel, message in reader.iter_messages():
#         topic = channel.topic
#         timestamp = message.log_time / 1e9  # Convert to seconds
        
#         topic_data[topic].append({
#             'data': message.data,
#             'schema': schema,
#             'channel': channel
#         })
#         topic_timestamps[topic].append(timestamp)

# # Print summary
# for topic in sorted(topic_data.keys()):
#     print(f"{topic}: {len(topic_data[topic])} messages")

# # Inspect a sample message from each topic
# print("\n" + "="*70)
# print("SAMPLE MESSAGE INSPECTION")
# print("="*70)

# for topic in sorted(topic_data.keys()):
#     if topic_data[topic]:
#         sample = topic_data[topic][0]
#         print(f"\nTopic: {topic}")
#         print(f"  Message size: {len(sample['data'])} bytes")
#         print(f"  Schema: {sample['schema'].name if sample['schema'] else 'None'}")
#         print(f"  First 100 bytes (hex): {sample['data'][:100].hex()}")
#         print(f"  First 100 bytes (raw): {sample['data'][:100]}")
        
#         # Try to identify data patterns
#         print(f"\n  Attempting to parse as different types:")
        
#         # Try as doubles
#         try:
#             num_doubles = len(sample['data']) // 8
#             if num_doubles > 0:
#                 doubles = struct.unpack(f'<{min(num_doubles, 10)}d', sample['data'][:min(num_doubles*8, 80)])
#                 print(f"    As doubles (little-endian): {doubles}")
#         except Exception as e:
#             print(f"    As doubles: Failed - {e}")
        
#         # Try as floats
#         try:
#             num_floats = len(sample['data']) // 4
#             if num_floats > 0:
#                 floats = struct.unpack(f'<{min(num_floats, 10)}f', sample['data'][:min(num_floats*4, 40)])
#                 print(f"    As floats (little-endian): {floats}")
#         except Exception as e:
#             print(f"    As floats: Failed - {e}")
        
#         # Try as integers
#         try:
#             num_ints = len(sample['data']) // 4
#             if num_ints > 0:
#                 ints = struct.unpack(f'<{min(num_ints, 10)}i', sample['data'][:min(num_ints*4, 40)])
#                 print(f"    As ints (little-endian): {ints}")
#         except Exception as e:
#             print(f"    As ints: Failed - {e}")

# print("\n" + "="*70)
# print("CUSTOM PARSER TEMPLATE")
# print("="*70)
# print("""
# # Based on the inspection above, create a custom parser for your topic:

# def parse_my_topic(msg_data):
#     '''
#     Custom parser for a specific message format.
#     Adjust the struct.unpack format string based on your data.
    
#     Format characters:
#     - 'd' = double (8 bytes)
#     - 'f' = float (4 bytes)
#     - 'i' = signed int (4 bytes)
#     - 'I' = unsigned int (4 bytes)
#     - 'q' = long long (8 bytes)
#     - 'Q' = unsigned long long (8 bytes)
#     - 'h' = short (2 bytes)
#     - 'H' = unsigned short (2 bytes)
#     - 'b' = signed char (1 byte)
#     - 'B' = unsigned char (1 byte)
    
#     Prefix '<' for little-endian, '>' for big-endian
#     '''
    
#     # Example: If your message has:
#     # - 1 int (4 bytes) for sequence number
#     # - 1 long (8 bytes) for timestamp
#     # - 3 doubles (24 bytes) for position x, y, z
#     # - 3 doubles (24 bytes) for velocity vx, vy, vz
    
#     offset = 0
    
#     # Parse header (adjust as needed)
#     seq, timestamp = struct.unpack('<iQ', msg_data[offset:offset+12])
#     offset += 12
    
#     # Parse position
#     pos_x, pos_y, pos_z = struct.unpack('<3d', msg_data[offset:offset+24])
#     offset += 24
    
#     # Parse velocity
#     vel_x, vel_y, vel_z = struct.unpack('<3d', msg_data[offset:offset+24])
#     offset += 24
    
#     return {
#         'seq': seq,
#         'timestamp': timestamp,
#         'position': [pos_x, pos_y, pos_z],
#         'velocity': [vel_x, vel_y, vel_z]
#     }

# # Use the parser:
# selected_topic = '/robot_1/state/estimate'
# parsed_data = []

# for msg_dict in topic_data[selected_topic]:
#     parsed = parse_my_topic(msg_dict['data'])
#     parsed_data.append(parsed)

# # Extract specific fields for plotting
# timestamps = np.array(topic_timestamps[selected_topic]) - topic_timestamps[selected_topic][0]
# positions = np.array([d['position'] for d in parsed_data])

# # Plot
# fig, axes = plt.subplots(3, 1, figsize=(12, 8))
# labels = ['X', 'Y', 'Z']
# for i in range(3):
#     axes[i].plot(timestamps, positions[:, i])
#     axes[i].set_ylabel(f'Position {labels[i]}')
#     axes[i].grid(True)
# axes[-1].set_xlabel('Time (s)')
# plt.tight_layout()
# plt.show()
# """)

# print("\n" + "="*70)
# print("RECOMMENDATIONS")
# print("="*70)
# print("""
# 1. Look at the schema definitions above to understand the message structure
# 2. Examine the sample message hex/raw output to identify patterns
# 3. Use the "Attempting to parse as different types" output as hints
# 4. Create a custom parser function using the template above
# 5. Adjust the struct.unpack format string based on your actual data layout

# For ROS2 messages, you might also consider using:
# - foxglove-schemas-protobuf (if using Protobuf encoding)
# - ROS2 message deserializers (if using ROS2 CDR encoding)
# """)