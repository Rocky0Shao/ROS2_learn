import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32
from std_srvs.srv import Trigger

class Controller(Node):

    def __init__(self):
        super().__init__('controller')
        self.subscription = self.create_subscription(
            Int32,
            'speed',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.cli = self.create_client(Trigger, 'reset_vehicle')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Wait to reset speed...')
        self.req = Trigger.Request()

    def listener_callback(self, msg):
        # Match the type: change Int64 to Int32 in your imports and sub!
        if msg.data > 80:
            self.get_logger().info(f'Speed {msg.data} too high! Resetting...')
            self.call_reset_service()

    def call_reset_service(self):
        self.future = self.cli.call_async(self.req)
        


def main(args=None):
    rclpy.init(args=args)

    controller = Controller()

    rclpy.spin(controller)


    controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
