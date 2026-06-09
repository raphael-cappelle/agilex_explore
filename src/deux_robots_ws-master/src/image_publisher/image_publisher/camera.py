#!/usr/bin/python3
import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class Camera(Node):
    def __init__(self):
        super().__init__("image_publisher")
        self.bridge = CvBridge()
        
        # Les jetson nano et les raspberry pi n'utilisent pas les même pipelines pour accéder à la caméra
        if self.is_jetson_nano():
            self.cap = cv2.VideoCapture("nvarguscamerasrc sensor-id=0  ! video/x-raw(memory:NVMM), width=3264, height=2464, format=(string)NV12, framerate=(fraction)20/1 ! nvvidconv flip-method=0 ! video/x-raw, width=640, height=480, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
        else:
            self.cap = cv2.VideoCapture(0)

        self.pub = self.create_publisher(Image, "/image_raw", 10)

    def is_jetson_nano(self):
        try:
            # Les jetson nano ont un fichier "model" qui donne le nom de la carte
            with open('/proc/device-tree/model', 'r') as f:
                model = f.read().lower()
                return 'nvidia jetson' in model
        except FileNotFoundError:
            # Ce fichier n'est pas présent sur les raspberry pi
            return False

    def run(self):
        while True:
            try:
                r, frame = self.cap.read()
                if not r:
                    return
                self.pub.publish(self.bridge.cv2_to_imgmsg(frame, "bgr8"))

            except CvBridgeError as e:
                print(e)

def main(args=None):
    rclpy.init(args=args)

    node = Camera()
    print("Publishing...")
    node.run()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()