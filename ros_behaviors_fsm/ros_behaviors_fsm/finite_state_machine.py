import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from neato2_interfaces.msg import Bump  # adjust to your actual bump msg type


class FiniteStateMachine(Node):
    def __init__(self):
        super().__init__('finite_state_machine')

        self.state = 'DRIVE_SQUARE'  # starting state, per diagram

        self.state_pub = self.create_publisher(String, '/fsm_state', 10)
        self.bump_sub = self.create_subscription(
            Bump, '/bump', self.bump_callback, 10)
        self.done_sub = self.create_subscription(
            String, '/state_done', self.done_callback, 10)

        # Broadcast state regularly so nodes starting late still sync up
        self.timer = self.create_timer(0.1, self.publish_state)

    def publish_state(self):
        msg = String()
        msg.data = self.state
        self.state_pub.publish(msg)

    def bump_callback(self, msg):
        if any([msg.left_front, msg.right_front,
                msg.left_side, msg.right_side]):
            if self.state != 'E_STOP':
                self.get_logger().info('Bump detected -> E_STOP')
                self.state = 'E_STOP'

    
    def done_callback(self, msg):
        # msg.data is the name of the state reporting itself done
        transitions = {
            'DRIVE_SQUARE': 'DANCE',
            'DANCE': 'WALL_FOLLOWING',
            'E_STOP': 'DANCE',
        }
        if msg.data == self.state and self.state in transitions:
            self.state = transitions[self.state]
            self.get_logger().info(f'Transitioning to {self.state}')


def main():
    rclpy.init()
    node = FiniteStateMachine()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()