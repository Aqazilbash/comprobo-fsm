import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class DanceNode(Node):
    STATE_NAME ='DANCE'

    def __init__(self):
        super().__init__('dance')

        self.active = False

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.done_pub = self.create_publisher(String, '/state_done', 10)
        self.state_sub = self.create_subscription(
            String, '/fsm_state', self.state_callback, 10)

        # Dance move sequence: (linear.x, angular.z, duration_sec)
        self.moves = [
            (0.5, 0.0, 0.5),   # forward
            (-0.5, 0.0, 0.5),  # backward
            (0.0, 2.0, 0.5),   # spin left
            (0.0, -2.0, 0.5),  # spin right
            (0.5, 0.0, 0.5),   # forward
            (-0.5, 0.0, 0.5),  # backward
            (0.0, -2.0, 0.5),   # spin right
            (0.0, 2.0, 0.5),  # spin left
        ]
        self.move_index = 0
        self.move_elapsed = 0.0

        self.timer_period = 0.1
        self.timer = self.create_timer(self.timer_period, self.run_loop)

    def state_callback(self, msg):
        was_active = self.active
        self.active = (msg.data == self.STATE_NAME)
        if self.active and not was_active:
            # just became active, reset dance from the start
            self.move_index = 0
            self.move_elapsed = 0.0

    def run_loop(self):
        if not self.active:
            return

        lin_x, ang_z, duration = self.moves[self.move_index]

        twist = Twist()
        twist.linear.x = lin_x
        twist.angular.z = ang_z
        self.cmd_pub.publish(twist)

        self.move_elapsed += self.timer_period
        if self.move_elapsed >= duration:
            self.move_index += 1
            self.move_elapsed = 0.0
            if self.move_index >= len(self.moves):
                #self.move_index = 0  # loop the dance, or...
                self.report_done()  # ...or report done if it should end

    def report_done(self):
        msg = String()
        msg.data = self.STATE_NAME
        self.done_pub.publish(msg)

def main():
    rclpy.init()
    node = DanceNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()