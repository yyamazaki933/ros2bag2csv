#!/usr/bin/env python3

from sys import argv
from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr
import pandas as pd
import parser.sensor_msgs_parser as sensor_msgs
import parser.geometry_msgs_parser as geometry_msgs

bag_file = argv[1]
topic = argv[2]

supported_type = [
    sensor_msgs.NAVSATFIX_TYPE,
    geometry_msgs.POSE_STAMPED_TYPE
]

with Reader(bag_file) as reader:

    if topic == "-l" or topic == "--list":
        for connection in reader.connections:

            if connection.msgtype in supported_type:
                print(connection.topic, ':', connection.msgtype)
            else:
                print(connection.topic, ':', connection.msgtype, "*")
        
        print("* is unsupported type.")
    
    else:
        data = []
        length = 0

        for connection, timestamp, rawdata in reader.messages():
            if connection.topic == topic:
                msg = deserialize_cdr(rawdata, connection.msgtype)

                if connection.msgtype == sensor_msgs.NAVSATFIX_TYPE:
                    if length == 0:
                        data.append(sensor_msgs.NAVSATFIX_HEADER)
                    data.append(sensor_msgs.navsatfix_parser(msg))
                    length += 1

                if connection.msgtype == geometry_msgs.POSE_STAMPED_TYPE:
                    if length == 0:
                        data.append(geometry_msgs.POSE_STAMPED_HEADER)
                    data.append(geometry_msgs.pose_stamped_parser(msg))
                    length += 1
                
                print("length:", length, end='\r')
        
        print("length:", length)
        
        csv = pd.DataFrame(data)
        csv.to_csv(bag_file + '.csv', header=False, index=False)
        
        print('save at', bag_file + '.csv')
