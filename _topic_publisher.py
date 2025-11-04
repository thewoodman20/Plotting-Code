#this code publishes topics

import sys
import struct
import numpy as np
import matplotlib.pyplot as plt
from mcap.reader import make_reader
from collections import defaultdict

filepath = "bag_file/robot_1_quad_log_spirit_20251008_1525_0.mcap"

topic_data = defaultdict(list)
topic_timestamps = defaultdict(list)

#read and collect messages from mcap files
with open(filepath, "rb") as f:
    reader = make_reader(f)
    for schema, channel, message in reader.iter_messages():
        topic = channel.topic
        timestamp = message.log_time / 1e9 #convert nanosec to sec
        topic_data[topic].append(message.data)
        topic_timestamps[topic].append(timestamp)
    

#print available topics
print("Available topics:")
for i, topic in enumerate(sorted(topic_data.keys()), 1):
    print(f"{i}. {topic} ({len(topic_data[topic])} messages)")