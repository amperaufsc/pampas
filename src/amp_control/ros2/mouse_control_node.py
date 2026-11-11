#!/opt/venv/bin/python
"""Publishes mouse position normalized to [-1, 1], works on Wayland (via XWayland).

Wayland blocks global pointer reads, so the mouse is captured inside a window.
Normalization is relative to the window size (independent of screen size).

x: -1 = left edge,   +1 = right edge
y: -1 = bottom edge, +1 = top edge

Deps: sudo apt install python3-tk
Run:  python3 mouse_position_node.py --ros-args -p fullscreen:=true
      (Esc or q to quit)
"""

import tkinter as tk

import rclpy
from rclpy.node import Node

from fs_msgs.msg import ControlCommand


def clamp(v, lo=-1.0, hi=1.0):
    return max(lo, min(hi, v))


class MousePositionNode(Node):
    def __init__(self, root: tk.Tk):
        super().__init__("mouse_position")
        self.declare_parameter("rate_hz", 60.0)
        self.declare_parameter("topic", "mouse_position")
        self.declare_parameter("fullscreen", False)

        self.root = root
        self.x = 0.0
        self.y = 0.0

        root.title("Mouse input")
        root.geometry("800x600")
        if self.get_parameter("fullscreen").value:
            root.attributes("-fullscreen", True)
        root.bind("<Motion>", self.on_motion)
        root.bind("<Escape>", lambda e: root.quit())
        root.bind("q", lambda e: root.quit())

        self.pub = self.create_publisher(ControlCommand, "/control", 10)
        self.create_timer(1.0 / 50, self.tick)

    def on_motion(self, event):
        w = max(self.root.winfo_width() - 1, 1)
        h = max(self.root.winfo_height() - 1, 1)
        self.x = clamp(2.0 * event.x / w - 1.0)
        self.y = clamp(-event.y / h)

    def tick(self):
        msg = ControlCommand()
        msg.throttle = self.y
        msg.steering = self.x
        msg.brake = 0.0
        self.pub.publish(msg)


def main():
    rclpy.init()
    root = tk.Tk()
    node = MousePositionNode(root)

    def spin():
        rclpy.spin_once(node, timeout_sec=0)
        root.after(5, spin)

    root.after(5, spin)
    try:
        root.mainloop()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
