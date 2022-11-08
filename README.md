# ros2bag2csv

Support message types

- sensor_msgs/msg/NavSatFix
- geometry_msgs/msg/PoseStamped


## Usage

### Write out a topic

```
python3 ros2bag2csv.py ~/path_to_rosbag2_dir /topic
```

### View the topics contained in the bag

```
python3 ros2bag2csv.py ~/path_to_rosbag2_dir --list (-l)
```

---

2022.10 yudai.yamazaki
