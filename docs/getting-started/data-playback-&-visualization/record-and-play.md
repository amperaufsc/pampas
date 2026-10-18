# Record and Play Bags

How to record ROS 2 bags in `mcap` format and play them back.

## Requirements

- Pampas built and set up. You can check on [Build](../build.md) page

> **Note:** only the `fs_msgs` package is required for visualization, so you can build just it in your workspace:
>
> ```bash
> colcon build --packages-select fs_msgs
> ```

## Installation

Install the `mcap` storage plugin (we use ROS 2 Humble):

```bash
sudo apt install ros-humble-rosbag2-storage-mcap
```

## Record a bag

Go to `pampas/` and source the workspace, so custom messages (e.g. `fs_msgs`) are available:

```bash
source install/setup.bash
```

Record all topics in `mcap` format:

```bash
ros2 bag record -s mcap -a -o bag_name
```

Or record only specific topics:

```bash
ros2 bag record -s mcap -o bag_name /topic_1 /topic_2 ...
```

| Option | Description |
| --- | --- |
| `-s mcap` | Use the `mcap` storage format (required) |
| `-a` | Record all topics |
| `-o bag_name` | Name of the output bag folder |

Stop the recording with `Ctrl+C`. The bag is saved as a folder containing the `.mcap` file and a `metadata.yaml`.

## Inspect a bag

```bash
ros2 bag info bag_path/bag.mcap
```

## Play a bag

Go to `pampas/` and source the workspace:

```bash
source install/setup.bash
```

Play the bag:

```bash
ros2 bag play bag_path/bag.mcap --loop
```

`--loop` keeps the bag playing in a loop, without closing.

## Next step

To visualize the recorded topics in panels, follow [Foxglove: Quick Start](foxglove-quick-start.md).