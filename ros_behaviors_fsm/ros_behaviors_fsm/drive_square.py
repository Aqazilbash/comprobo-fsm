"""
Draw Square
--------
This node encapsulates implements a simple time-based approach to driving the
robot in a square.  The system makes use of a a special ``estop`` topic that
can trigger the robot to automatically stop when the value is true is received
on that topic.
"""
import rclpy
from rclpy.node import Node
from threading import Thread, Event
from time import sleep
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
import math

class DrawSquare(Node):
    """A class that implements a node to pilot a robot in a square.
    """

    def __init__(self):
        super().__init__('draw_square_with_estop')
        self.e_stop = Event()
        # create a thread to handle long-running component
        self.vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.create_subscription(Bool, 'estop', self.handle_estop, 10)
        self.run_loop_thread = Thread(target=self.run_loop)
        self.run_loop_thread.start()


    def handle_estop(self, msg):
        """Handles messages received on the estop topic.

        Args:
            msg (std_msgs.msg.Bool): the message that takes value true if we
            estop and false otherwise.
        """ 
        if msg.data:
            self.e_stop.set()
            self.drive(linear=0.0, angular=0.0)

    def run_loop(self):
        """Executes the main logic for driving the square.  This function does
        not return until the square is finished or the estop is pressed.
        """
        # the first message on the publisher is often missed
        self.drive(0.0, 0.0)
        sleep(1)
        for _ in range(4):
            if not self.e_stop.is_set():
                print("driving forward")
                self.drive_forward(1)
            if not self.e_stop.is_set():
                print("turning left")
                self.turn_left()
        print('done with run loop')

    def drive(self, linear, angular):
        """Drive with the specified linear and angular velocity.

        Args:
            linear (_type_): the linear velocity in m/s
            angular (_type_): the angular velocity in radians/s
        """        
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.vel_pub.publish(msg)

    def turn_left(self):
        """Execute a 90 degree left turn
        """
        angular_vel = 0.3
        if not self.e_stop.is_set():
            self.drive(linear=0.0, angular=angular_vel)
            sleep(math.pi / angular_vel / 2)
            self.drive(linear=0.0, angular=0.0)

    def drive_forward(self, distance):
        """Drive straight for the specified distance.

        Args:
            distance (_type_): the distance to drive forward.  Only positive
            values are supported.
        """
        forward_vel = 0.1
        if not self.e_stop.is_set():
            self.drive(linear=forward_vel, angular=0.0)
        sleep(distance / forward_vel)
        self.drive(linear=0.0, angular=0.0)

def main(args=None):
    rclpy.init(args=args)
    node = DrawSquare()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()