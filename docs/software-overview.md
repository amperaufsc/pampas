# Software overview

## Perception
```mermaid
flowchart LR
    %% ROS 2 nodes
    Camera["Node<br/>/camera_node"]
    Yolo["Node<br/>/yolo_recognition"]
    Perception["Node<br/>/perception_node"]
    Mapper["Node<br/>/mapper_node"]

    %% ROS 2 topics
    LeftImage(["Topic<br/>/camera/left/image_raw"])
    RightImage(["Topic<br/>/camera/right/image_raw"])
    Disparity(["Topic<br/>/camera/disparity/image_raw"])
    Inference(["Topic<br/>/inference"])
    Track(["Topic<br/>/track_stamped"])

    %% Communication
    Camera --> LeftImage
    Camera --> RightImage
    Camera --> Disparity

    LeftImage --> Yolo
    Yolo --> Inference

    LeftImage --> Perception
    RightImage --> Perception
    Disparity --> Perception
    Inference --> Perception

    Perception --> Track
    Track --> Mapper

    %% Styles
    classDef nodeStyle fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#000
    classDef topicStyle fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#000

    class Camera,Yolo,Perception,Mapper nodeStyle
    class LeftImage,RightImage,Disparity,Inference,Track topicStyle
```

## Mapper
```mermaid
flowchart LR
    %% =========================
    %% ROS 2 Nodes
    %% =========================
    Perception["Node<br/>/perception_node"]
    Odometry_Message_Node["Node<br/>/Odom_message_node"]
    Transform_Ros_Bus["Node<br/>/tf_ros_bus"]
    Mapper["Node<br/>/mapper_node"]
    Path_Planning["Node<br/>/path_planning_node"]

    %% =========================
    %% ROS 2 Topics
    %% =========================
    Track_Stamped(["Topic<br/>/track_stamped"])
    Odom(["Topic<br/>/odometry"])
    Tf(["Topic<br/>/tf_msg"])
    Track(["Topic<br/>/track"])

    %% =========================
    %% Communication
    %% =========================

    %% Perception
    Perception --> Track_Stamped

    %% Odometry
    Odometry_Message_Node --> Odom

    %% TF
    Transform_Ros_Bus --> Tf

    %% Mapper inputs
    Track_Stamped --> Mapper
    Odom --> Mapper
    Tf --> Mapper

    %% Mapper output
    Mapper --> Track

    %% Planning
    Track --> Path_Planning

    %% =========================
    %% Styles
    %% =========================
    classDef nodeStyle fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#000
    classDef topicStyle fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#000

    class Perception,Odometry_Message_Node,Transform_Ros_Bus,Mapper,Path_Planning nodeStyle
    class Track_Stamped,Odom,Tf,Track topicStyle
```
## Path Planning
```mermaid
flowchart LR
    %% =========================
    %% ROS 2 Nodes
    %% =========================
    Mapper["Node<br/>/mapper_node"]
    Odometry_Message_Node["Node<br/>/Odom_message_node"]
    Can_Receiver["Node<br/>/can_receiver"]
    Path_Planning["Node<br/>/path_planning_node"]
    Control_Node["Node<br/>/control_node"]

    %% =========================
    %% ROS 2 Topics
    %% =========================
    Track(["Topic<br/>/track"])
    Odom(["Topic<br/>/odometry"])
    Res_Go(["Topic<br/>/res/go"])
    Path(["Topic<br/>/path"])
    Path_Concatenated(["Topic<br/>/path_concatenated"])
    Track_Pointcloud(["Topic<br/>/track_pointcloud"])

    %% =========================
    %% Communication
    %% =========================

    %% Publishers
    Mapper --> Track
    Odometry_Message_Node --> Odom
    Can_Receiver --> Res_Go

    %% Path Planning inputs
    Track --> Path_Planning
    Odom --> Path_Planning
    Res_Go --> Path_Planning

    %% Path Planning outputs
    Path_Planning --> Path
    Path_Planning --> Path_Concatenated
    Path_Planning --> Track_Pointcloud

    %% Control Node inputs
    Path 
    Path_Concatenated --> Control_Node
    Track_Pointcloud

    %% =========================
    %% Styles
    %% =========================
    classDef nodeStyle fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#000
    classDef topicStyle fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#000

    class Mapper,Odometry_Message_Node,Can_Receiver,Path_Planning,Control_Node nodeStyle
    class Track,Odom,Res_Go,Path,Path_Concatenated,Track_Pointcloud topicStyle
```
## Mapper
```mermaid
flowchart LR
    %% =========================
    %% ROS 2 Nodes
    %% =========================
    Perception["Node<br/>/perception_node"]
    Odometry_Message_Node["Node<br/>/Odom_message_node"]
    Transform_Ros_Bus["Node<br/>/tf_ros_bus"]
    Mapper["Node<br/>/mapper_node"]
    Path_Planning["Node<br/>/path_planning_node"]

    %% =========================
    %% ROS 2 Topics
    %% =========================
    Track_Stamped(["Topic<br/>/track_stamped"])
    Odom(["Topic<br/>/odometry"])
    Tf(["Topic<br/>/tf_msg"])
    Track(["Topic<br/>/track"])

    %% =========================
    %% Communication
    %% =========================

    %% Perception
    Perception --> Track_Stamped

    %% Odometry
    Odometry_Message_Node --> Odom

    %% TF
    Transform_Ros_Bus --> Tf

    %% Mapper inputs
    Track_Stamped --> Mapper
    Odom --> Mapper
    Tf --> Mapper

    %% Mapper output
    Mapper --> Track

    %% Planning
    Track --> Path_Planning

    %% =========================
    %% Styles
    %% =========================
    classDef nodeStyle fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#000
    classDef topicStyle fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#000

    class Perception,Odometry_Message_Node,Transform_Ros_Bus,Mapper,Path_Planning nodeStyle
    class Track_Stamped,Odom,Tf,Track topicStyle
```
## Control

```mermaid
flowchart LR
    %% =========================
    %% ROS 2 Nodes
    %% =========================
    Path_Planning["Node<br/>/path_planning_node"]
    Odometry_Message_Node["Node<br/>/Odom_message_node"]
    Control_Node["Node<br/>/control_node"]
    Low_Level_Control["Node<br/>/low_level_control"]

    %% =========================
    %% ROS 2 Topics (Inputs)
    %% =========================
    Path(["Topic<br/>/path_concatenated"])
    Odom(["Topic<br/>/odom"])

    %% =========================
    %% ROS 2 Topics (Control Outputs)
    %% =========================
    Control_Command(["Topic<br/>/control_command"])
    Speed(["Topic<br/>/speed"])
    Erro_Ant(["Topic<br/>/erro_ant"])
    Eh(["Topic<br/>/eh"])
    Ey(["Topic<br/>/ey"])
    Reference_Path(["Topic<br/>/reference_path"])

    %% =========================
    %% ROS 2 Topics (Low Level Outputs)
    %% =========================
    Sensor_Value(["Topic<br/>/sensor/value"])
    Control_Actual(["Topic<br/>/control/actual_value"])
    Control_Anti_Windup(["Topic<br/>/control/anti_windup_value"])
    Control_Error(["Topic<br/>/control/error"])
    Control_Min(["Topic<br/>/control/min_value"])
    Control_Max(["Topic<br/>/control/max_value"])

    %% =========================
    %% Communication
    %% =========================

    %% External Publishers
    Path_Planning --> Path
    Odometry_Message_Node --> Odom

    %% Control Node Inputs
    Path --> Control_Node
    Odom --> Control_Node

    %% Control Node Outputs
    Control_Node --> Speed
    Control_Node --> Erro_Ant
    Control_Node --> Eh
    Control_Node --> Ey
    Control_Node --> Reference_Path
    Control_Node --> Control_Command

    %% Interconnection
    Control_Command --> Low_Level_Control

    %% Low Level Control Outputs
    Low_Level_Control --> Sensor_Value
    Low_Level_Control --> Control_Actual
    Low_Level_Control --> Control_Anti_Windup
    Low_Level_Control --> Control_Error
    Low_Level_Control --> Control_Min
    Low_Level_Control --> Control_Max

    %% =========================
    %% Styles
    %% =========================
    classDef nodeStyle fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#000
    classDef topicStyle fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#000

    class Path_Planning,Odometry_Message_Node,Control_Node,Low_Level_Control nodeStyle
    class Path,Odom,Control_Command,Speed,Erro_Ant,Eh,Ey,Reference_Path,Sensor_Value,Control_Actual,Control_Anti_Windup,Control_Error,Control_Min,Control_Max topicStyle
```

## State Machine

- It highlights all possible states and the specific events responsible for state transitions.

```mermaid
flowchart TD
    %% =========================
    %% Estados
    %% =========================
    st_AsOff["State<br/>st_AsOff"]
    st_AsReady["State<br/>st_AsReady"]
    st_AsCalibration["State<br/>st_AsCalibration"]
    st_AsChecking["State<br/>st_AsChecking"]
    st_AsDriving["State<br/>st_AsDriving"]
    st_AsFinished["State<br/>st_AsFinished"]
    st_AsEmergency["State<br/>st_AsEmergency"]

    %% =========================
    %% Transições (Eventos)
    %% =========================
    st_AsOff -->|EvAllNodesConfigured| st_AsReady
    st_AsOff -->|EvNodeCrashed<br/>EvStopListener| st_AsEmergency

    st_AsReady -->|EvCheckListener| st_AsChecking
    st_AsReady -->|EvReadyToDrive| st_AsDriving
    st_AsReady -->|EvCalibrationListener| st_AsCalibration
    st_AsReady -->|EvNodeCrashed<br/>EvStopListener| st_AsEmergency

    st_AsCalibration -->|EvCalibrationListener| st_AsReady
    st_AsCalibration -->|EvStopListener<br/>EvNodeCrashed| st_AsEmergency

    st_AsChecking -->|EvCheckListener| st_AsReady
    st_AsChecking -->|EvNodeCrashed<br/>EvStopListener| st_AsEmergency

    st_AsDriving -->|EvFinishedListener| st_AsFinished
    st_AsDriving -->|EvNodeCrashed<br/>EvStopListener| st_AsEmergency

    st_AsFinished -->|EvCalibrationListener| st_AsReady
    st_AsFinished -->|EvStopListener| st_AsEmergency

    %% =========================
    %% Styles
    %% =========================
    classDef nodeStyle fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#000
    classDef topicStyle fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#000

    class st_AsOff,st_AsReady,st_AsCalibration,st_AsChecking,st_AsDriving,st_AsFinished,st_AsEmergency nodeStyle
```

- The following section demonstrates the state machine's operation across the system.

```mermaid
flowchart LR
    %% =========================
    %% ROS 2 Nodes
    %% =========================
    Yolo["Node<br/>/yolo_recognition"]
    Perception["Node<br/>/perception_node"]
    Mapper["Node<br/>/mapper_node"]
    Path_Planning["Node<br/>/path_planning_node"]
    Control_Node["Node<br/>/control_node"]
    State_Machine["Node<br/>/state_machine"]

    %% =========================
    %% ROS 2 Topics (Change State Only)
    %% =========================
    State_Yolo(["Topic<br/>/yolo_recognition/change_state"])
    State_Perception(["Topic<br/>/perception_node/change_state"])
    State_Mapper(["Topic<br/>/mapper_node/change_state"])
    State_Path(["Topic<br/>/path_planning_node/change_state"])
    State_Control(["Topic<br/>/control_node/change_state"])

    %% =========================
    %% Communication
    %% =========================

    %% State Machine connections
    State_Machine --> State_Yolo --> Yolo
    State_Machine --> State_Perception --> Perception
    State_Machine --> State_Mapper --> Mapper
    State_Machine --> State_Path --> Path_Planning
    State_Machine --> State_Control --> Control_Node

    %% =========================
    %% Styles
    %% =========================
    classDef nodeStyle fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#000
    classDef topicStyle fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#000

    class Yolo,Perception,Mapper,Path_Planning,Control_Node,State_Machine nodeStyle
    class State_Yolo,State_Perception,State_Mapper,State_Path,State_Control topicStyle
```
