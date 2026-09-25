import rclpy
from rclpy.node import Node
from threading import Thread, Event
from time import sleep
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool
import math

class DrawSquare(Node):
    """A class for a square drawing node. This node subscribes to the estop topic and publishes to a cmd_vel topic.
    """

    def __init__(self):
        super().__init__('draw_square')
        self.e_stop = Event()
        # create a thread to handle long-running component
        self.vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.create_publisher(Bool, 'finished', 10) #msg to tell fsm that task is finished

        self.create_subscription(Bool, 'estop', self.handle_estop, 10)
        self.create_subscription(Odometry, 'odom', self.handle_odom, 10)

        self.run_loop_thread = Thread(target=self.run_loop)
        self.run_loop_thread.start()

        self.x_position_distance = 1.0 #meters
        self.y_position_distance = 0.0 #meters
        self.z_position_distance = 0.0 #meters
        self.x_orientation_distance = 0.0 #degrees
        self.y_orientation_distance = 0.0 #degrees
        self.z_orientation_distance = 90 #degrees


    def handle_estop(self, msg):
        """Handles messages received on the estop topic.

        Args:
            msg (std_msgs.msg.Bool): the message that takes value true if we
            estop and false otherwise.
        """ 
        if msg.data:
            self.e_stop.set()
            self.drive(linear=0.0, angular=0.0)

    def handle_odom(self, msg):
        """Handles messages received on the odom topic.

        Args:
            msg (nav_msgs.msg.Odometry): the message that contains the odometry
            information.
        """
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.z = msg.pose.pose.position.z 
        self.qx = msg.pose.pose.orientation.x
        self.qy = msg.pose.pose.orientation.y
        self.qz = msg.pose.pose.orientation.z

        #self.get_logger().info(f"odom: x={self.x}, y={self.y}, qx={self.qx}, qy={self.qy}, qz={self.qz}")

    def distance_goal(self, position, orientation):
        """Calculates the desired distance to a goal position and orientation.

        Args:
            position (tuple): the goal position as a tuple (x, y, z)
            orientation (tuple): the goal orientation as a tuple (qx, qy, qz)
        """
        current_position = (self.x, self.y, self.z)
        current_orientation = (self.qx, self.qy, self.qz)

        new_position = []
        for i in position:
            desired_position = position[i] - current_position[i]
            new_position.append(desired_position)

        new_orientation = []
        for i in orientation:
            desired_orientation = orientation[i] - current_orientation[i]
            new_orientation.append(desired_orientation)

        return new_position, new_orientation

    def run_loop(self):
        """Executes the main logic for driving the square.  This function does
        not return until the square is finished or the estop is pressed.
        """
        goal_reached = self.distance_goal((self.x_position_distance, 
                                           self.y_position_distance, 
                                           self.z_position_distance), 
                                          (self.x_orientation_distance, 
                                           self.y_orientation_distance, 
                                           self.z_orientation_distance))
        # the first message on the publisher is often missed
        self.drive(0.0, 0.0)
        sleep(1)
        print(goal_reached)
        for _ in range(4):
            while not self.e_stop.is_set() and not goal_reached:

                print("driving forward")
                self.drive_forward(0.5)
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
        self.drive(linear=0.0, angular=angular_vel)
        sleep(math.pi / angular_vel / 2)
        self.drive(linear=0.0, angular=0.0)

    def drive_forward(self, distance):
        """Drive straight for the spefcified distance.

        Args:
            distance (_type_): the distance to drive forward.  Only positive
            values are supported.
        """
        forward_vel = 0.1

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
