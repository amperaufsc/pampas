In Driverless, we divide the control system into several modules, including:

- Lateral Control
- Longitudinal Control
- Low-Level Lateral Control

In this article, we will focus on the **Lateral Control** problem and its interactions with the preceding and following modules, namely **Path Planning** and **Low-Level Control**, respectively.

Since 2021, we have been using the KLS controller (Kinematic Lateral Steering) in Driverless. It was first introduced in the paper *Path Planning and Guidance Laws of a Formula Student Driverless Car*, published by researchers from the University of Lisbon.

The main idea behind this controller is to go beyond simply correcting the vehicle's positional error. Instead, KLS calculates the desired lateral velocity required to reach a given trajectory.

For example:

- If the vehicle is slightly off the trajectory, a small correction may be sufficient.
- If the vehicle is far away from its intended trajectory, a higher lateral velocity may be necessary.
- If the vehicle is approaching its intended trajectory, the control signal must gradually decrease to prevent overshooting.

Before implementing the controller, we must first define its variables, followed by the node's subscribers and publishers.

## Controller Variables

| Variable | Meaning | Explanation |
|---|---|---|
| \(e_y\) | Vehicle lateral error | Difference between the vehicle's actual position and its intended position along the trajectory. |
| \(e_\psi\) | Heading error | Difference between the vehicle's forward direction and the tangent to the intended trajectory at the vehicle's reference position. |
| \(v_x\) | Longitudinal velocity | Vehicle velocity along its longitudinal axis. |
| \(v_y\) | Lateral velocity | Vehicle velocity along its lateral axis. |
| \(\delta\) | Steering angle | Steering angle commanded by the controller. |
| \(L\) | Vehicle wheelbase | Distance between the front and rear axles. |