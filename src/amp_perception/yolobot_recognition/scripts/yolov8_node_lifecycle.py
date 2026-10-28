#!/usr/bin/env python3

from ultralytics import YOLO
import rclpy
from rclpy.lifecycle import LifecycleNode, State, TransitionCallbackReturn
from rcl_interfaces.msg import ParameterDescriptor, FloatingPointRange, SetParametersResult
import os
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from yolov8_msgs.msg import InferenceWithConfidence
from yolov8_msgs.msg import Yolov8Inference
import logging # Used to turn get_logger().info() if YOLO into get_logger().warn()

bridge = CvBridge()

class LifecycleCameraSubscriber(LifecycleNode):

    def __init__(self):
        super().__init__('yolo_node')

        self.yolov8_inference = Yolov8Inference()
        self.subscription = None
        self.yolov8_pub = None
        self.img_pub = None
        self.model = None

        # Desable get_logger().info() from YOLO
        logging.getLogger('ultralytics').setLevel(logging.WARNING)

        # Declare parameters
        self.declare_parameter(
            'yolo_weight_path',
            'None',
            descriptor=ParameterDescriptor(
                description='Yolo weight path used for cone detection'
            )
        )       
              
        self.declare_parameter(
            'confidence_threshold',
            0.8,
            descriptor=ParameterDescriptor(
                description='Minimum confidence (0.0 to 1.0) for a cone detection to be accepted',
                floating_point_range=[FloatingPointRange(
                    from_value=0.0,
                    to_value=1.0,
                    step=0.0
                )]
            )
        )

        self.get_logger().info("Yolo node initialized (Unconfigured)")

    def on_configure(self, state: State) -> TransitionCallbackReturn:
        try:
            self.get_logger().info("Configuring Yolo Node") 

            # Initialize parameters
            self.weigth_path = os.path.expanduser(self.get_parameter('yolo_weight_path').value)
            self.confidence_threshold = self.get_parameter('confidence_threshold').value

            # Intialize Yolo
            self.model = YOLO(self.weigth_path)

            # Implement params callback
            self.add_on_set_parameters_callback(self.params_callback)

            self.yolov8_pub = self.create_lifecycle_publisher(Yolov8Inference, "inference", 1)
            self.img_pub = self.create_lifecycle_publisher(Image, "inferenceimg", 1)

            self.subscription = self.create_subscription(
                Image,
                'image',
                self.camera_callback,
                10)

            return TransitionCallbackReturn.SUCCESS
        except Exception as e:
            self.get_logger().error(f"Error when configuring: {e}")
            return TransitionCallbackReturn.ERROR

    def params_callback(self, params):
        for p in params:
            if p.name == "yolo_weight_path":
                if not os.path.isfile(p.value):
                    return SetParametersResult(
                                successful=False,
                                reason='The weight path received does not match a file'
                            )
                self.weigth_path = os.path.expanduser(p.value)
                self.model = YOLO(self.weigth_path)
                self.get_logger().info(f"Model weight changed to {os.path.basename(self.weigth_path)}")
            elif p.name == "confidence_threshold":
                self.confidence_threshold = p.value
                self.get_logger().info(f"Threshold: {self.confidence_threshold}")
        return SetParametersResult(
            successful=True,
            reason='All params setted'
        )

    def on_activate(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info("Activating Yolo Node")
        super().on_activate(state)
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info("Deactivating Yolo Node")
        super().on_deactivate(state)
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info("Cleaning up Yolo Node")

        self.destroy_subscription(self.subscription)
        self.destroy_lifecycle_publisher(self.yolov8_pub)
        self.destroy_lifecycle_publisher(self.img_pub)

        self.subscription = None
        self.yolov8_pub = None
        self.img_pub = None
        self.model = None

        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info("Yolo Node Shutdown")
        self.destroy_subscription(self.subscription)
        self.destroy_lifecycle_publisher(self.yolov8_pub)
        self.destroy_lifecycle_publisher(self.img_pub)
        return TransitionCallbackReturn.SUCCESS

    def camera_callback(self, data):
        if self.img_pub is None or not self.img_pub.is_activated:
            return

        confidence = self.confidence_threshold

        img = bridge.imgmsg_to_cv2(data, "bgr8")

        results = self.model(img, conf=confidence, device=0)

        self.yolov8_inference.header = data.header

        for r in results:
            boxes = r.boxes
            for box in boxes:
                self.inference_result = InferenceWithConfidence()
                b = box.xyxy[0].to('cpu').detach().numpy().copy()  # get box coordinates in (top, left, bottom, right) format
                c = box.cls
                self.inference_result.class_name = self.model.names[int(c)]
                self.inference_result.top = int(b[0])
                self.inference_result.left = int(b[1])
                self.inference_result.bottom = int(b[2])
                self.inference_result.right = int(b[3])
                self.inference_result.confidence = float(box.conf)
                self.yolov8_inference.yolov8_inference.append(self.inference_result)

        annotated_frame = results[0].plot()
        img_msg = bridge.cv2_to_imgmsg(annotated_frame)

        self.img_pub.publish(img_msg)
        self.yolov8_pub.publish(self.yolov8_inference)
        self.yolov8_inference.yolov8_inference.clear()

def main(args=None):
    rclpy.init(args=args)

    node = LifecycleCameraSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
