from sys import argv
from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr
import pandas as pd

bag_file = argv[1]
topic = argv[2]

POSE_STAMPED = 'geometry_msgs/msg/PoseStamped'
POSE_STAMPED_HEADER = [
    'msg.header.stamp', 
    'msg.header.frame_id', 
    'msg.pose.position.x', 
    'msg.pose.position.y', 
    'msg.pose.position.z',
    'msg.pose.orientation.x',
    'msg.pose.orientation.y',
    'msg.pose.orientation.z',
    'msg.pose.orientation.w']

def timestamp_parser(msg):
    stamp = msg.header.stamp.sec + (float)(msg.header.stamp.nanosec / 1000000000)
    return stamp

def pose_stamped_parser(msg):
    line = [
        timestamp_parser(msg), 
        msg.header.frame_id, 
        msg.pose.position.x, 
        msg.pose.position.y, 
        msg.pose.position.z,
        msg.pose.orientation.x,
        msg.pose.orientation.y,
        msg.pose.orientation.z,
        msg.pose.orientation.w]
    return line

# create reader instance and open for reading
with Reader(bag_file) as reader:
    # topic and msgtype information is available on .connections list

    if topic == "-l" or topic == "--list":
        for connection in reader.connections:
            print(connection.topic, ':', connection.msgtype)
    
    else:
        data = []
        data.append(POSE_STAMPED_HEADER)

        # iterate over messages
        for connection, timestamp, rawdata in reader.messages():
            if connection.topic == topic:
                msg = deserialize_cdr(rawdata, connection.msgtype)
                data.append(pose_stamped_parser(msg))
        
        csv = pd.DataFrame(data)
        csv.to_csv(bag_file + '.csv', header=False, index=False)
        
        print('save at', bag_file + '.csv')
