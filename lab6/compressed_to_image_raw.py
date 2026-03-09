import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge, CvBridgeError
import cv2
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image


class CompressedImageConverter(Node):
    def __init__(self):
        super().__init__('compresed_to_image_raw')
        self.logger = self.get_logger()
        self.first_frame_published = False
        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            CompressedImage,
            '/camera/image/compressed',
            self.image_callback,
            10,
        )

        self.publisher = self.create_publisher(Image, '/camera/image_raw', 10)

    def image_callback(self, msg):
        # This if statement is to simply check if we have received at least one
        # frame and published an image_raw once (we don't need to print it for
        # every frame received). It would help in the future, to debug, should
        # networking issues arise. When you run this node, you should look for
        # that info message in your terminal to verify that the subscriber
        # received at least a message (and therefore there is no issue with
        # networking).
        if not self.first_frame_published:
            self.logger.info('Started converting compressed image to image raw ...')
            self.first_frame_published = True

        try:
            cv_image = self.bridge.compressed_imgmsg_to_cv2(msg)

            image_message = self.bridge.cv2_to_imgmsg(cv_image, 'bgr8')

            self.publisher.publish(image_message)

        except CvBridgeError as e:
            print(f'Could not convert image: {e}')


def main():
    rclpy.init(args=None)
    image_converter = CompressedImageConverter()
    rclpy.spin(image_converter)


if __name__ == "__main__":
    main()
