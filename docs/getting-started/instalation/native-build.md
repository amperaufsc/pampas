# Native Build

This page explains how to build and run Pampas directly on your machine, without Docker. If you prefer containers, see the [Docker](docker.md) page.

## 1. Requirements

- **Ubuntu 22.04**
- **git**
- **[ROS 2 Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)**, with the desktop install and the development tools (they provide RViz, `rosdep`, `colcon` and the compilers):

  ```bash
  sudo apt install ros-humble-desktop ros-dev-tools
  ```

- **uv** (Python environment package manager). See the [installation guide](https://docs.astral.sh/uv/getting-started/installation/); the standalone installer is the simplest option:

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

## 2. Get the code

Clone the repository **recursively** so that all submodules are downloaded:

```bash
git clone --recursive https://github.com/amperaufsc/pampas.git
```

The `pampas/` folder is the **ROS 2 workspace**. All `colcon` commands below must be run from its root unless stated otherwise.

## 3. Install the dependencies

ROS 2 must be sourced in the terminal you use to build. Then use `rosdep` to download all the dependencies declared by the packages in the workspace:

```bash
source /opt/ros/humble/setup.bash
cd pampas
sudo apt update
sudo rosdep init   # only the first time rosdep is used on this machine
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

## 4. Build ORB-SLAM3

ORB-SLAM3 and its ROS 2 wrapper must be built **before** the main packages.

### 4.1 Pangolin

[Pangolin](https://github.com/stevenlovegrove/Pangolin) is the OpenGL library that ORB_SLAM3 uses for its viewer, and it is required to compile ORB_SLAM3.

From the Pangolin source directory, install its prerequisites, then build and install it:

```bash
./scripts/install_prerequisites.sh
cmake -B build
cmake --build build
cd build/
sudo make install
sudo ldconfig
```

### 4.2 ORB_SLAM3

From the ORB_SLAM3 source directory:

```bash
chmod +x build.sh
./build.sh
```
> **Note:** If the system freezes during the build, or the build stops with a `Killed` message, the machine has probably run out of memory (OOM). To avoid this, open the `build.sh` file and change the last line to `make -j2` (the default is `make -j4`). If it still freezes, try `make -j1`. The `-j` flag of `make` sets how many compile jobs run at the same time, and each job uses a lot of RAM.

### 4.3 ORB_SLAM3 ROS 2 package

Before building, install the workspace dependencies (skip if you already did it in section 3):

```bash
sudo apt update
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

Then build the package:

```bash
colcon build --symlink-install --packages-select orbslam3_ros2
```

> **Note:** The `--parallel-workers` flag of `colcon` sets how many packages are built at the same time (by default, one per CPU core). If the system freezes or runs out of memory during this build, add `--parallel-workers 1` to the command above. If it still happens, also limit the compile jobs inside each package, for example with `MAKEFLAGS=-j2 colcon build ...`.

### 4.4 Extract the ORB vocabulary

The vocabulary is shipped compressed as `ORBvoc.txt.tar.gz`, so `ORBvoc.txt` does not exist until it is extracted. If you skip this step, the node fails when launching:

```text
Loading ORB Vocabulary. This could take a while...
Vocabulary loading failure: This is not a correct text file!
Wrong path to vocabulary. Failed to open at: /home/<USER>/pampas/install/orbslam3_ros2/share/orbslam3_ros2/vocabulary/ORBvoc.txt
```

1. Check the contents of the vocabulary directory:

   ```bash
   ls /home/<USER>/pampas/install/orbslam3_ros2/share/orbslam3_ros2/vocabulary/
   ```

2. If only `ORBvoc.txt.tar.gz` is listed, enter the directory and extract it:

   ```bash
   cd /home/<USER>/pampas/install/orbslam3_ros2/share/orbslam3_ros2/vocabulary/
   tar -xzf ORBvoc.txt.tar.gz
   ```

3. Confirm that `ORBvoc.txt` now exists:

   ```bash
   ls
   ```

## 5. Build the main packages

From the root of `pampas/`:

```bash
colcon build --packages-up-to perception control mapper path_planning amp_utils amp_sm depthai_ros_driver amp_bringup yolobot_recognition
```

> **Note:** If the system freezes or runs out of memory during this build, add the `--parallel-workers 1` flag to the command above (see the note in section 4.3).

## 6. Run

After the build finishes, source ROS 2 and the workspace in every new terminal:

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
```

**Alternative:** to avoid sourcing manually in every new terminal, add the setup scripts to your `~/.bashrc`:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
echo "source /home/<USER>/pampas/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

> **Note:** Replace `/home/<USER>/pampas` with the actual path of your workspace. Add the second line only after the first successful build, since `install/setup.bash` does not exist before it. If you rebuild the workspace, no extra step is needed, since the path stays the same.

Then, to start the project, just run:

```bash
ros2 launch amp_bringup amp_as_bringup_mapper.launch.py
```