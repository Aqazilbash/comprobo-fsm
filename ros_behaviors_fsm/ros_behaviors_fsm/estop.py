import rclpy  # convenience python library for interacting with ROS2
from tf_transformations import euler_from_quaternion
from rclpy.node import Node  # generic Node class for interacting with ROS2
from neato2_interfaces.msg import Bump  # local package call for a Bump type message format
from geometry_msgs.msg import Twist  # ROS package call for a Twist type message format
from nav_msgs.msg import Odometry
import sleep
import math
from math import pi

def convert_pose_to_xy_and_theta(pose):
    """Convert pose (geometry_msgs.Pose) to a (x,y,yaw) tuple"""
    orientation_tuple = (
        pose.orientation.x,
        pose.orientation.y,
        pose.orientation.z,
        pose.orientation.w,
    )
    angles = euler_from_quaternion(orientation_tuple)
    return (pose.position.x, pose.position.y, angles[2])

class EmergencyStopNode(Node):
    """This is a node which stops the motors when the bump sensor is triggered.
    
    The class should allow the vehicle to move forward at a slow rate, until the
    bump sensor is triggered, in which case the robot should stop.
    
    Publishers Needed:
        - Twist cmd_vel message; which commands vehicle velocity
    Subscribers Needed:
        - Bump bump message handling; which listens for the bump sensor data
        - Odometry pose message, which reads the position of the robot.
    """
    def __init__(self):
        """Initializes the class."""
        super().__init__("emergency_stop_node") # node names should be unique
        # Create a timer that runs the robot motors
        self.create_timer(0.1, self.run_loop)
        self.body_pos = None
        self.num_turns = 0

        self.pos = [0, 0, 0]
        self.rotation = pi

        # Create a state that stores the bumper information
        self.bump_state = False

        '''
        Create a subscriber to the bump sensor.
        Method create_subscription takes a message type, the message topic name, the callback function, and a filter queue.
        A subscriber, once initialized, will immediately start listening to the ROS2 network and sending messages over
        the specified topic to the callback function.
        '''
        self.sub = self.create_subscription(Bump, "/bump", self.process_bump, 10)

        '''
        Create a publisher for the motors.
        Method create_publisher takes a message type, the message topic name, and a filter queue.
        A publisher will not publish anything once initialized, it must be called.
        '''
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        # Initialize subscriber for odom
        self.subscription = self.create_subscription(
            Odometry, "odom", self.get_odom, 10
        )


    def process_bump(self, msg):
        """Callback for handling a bump sensor input."
        Input: 
            msg (Bump): a Bump type message from the subscriber.
        """
        # Set the bump state to True if any part of the sensor is pressed
        self.bump_state = (msg.left_front == 1 or \
                           msg.right_front == 1 or \
                           msg.left_side == 1 or \
                           msg.right_side == 1)

    def get_odom(self, msg):
        """Callback for handling odometry position
        Input:
            msg (Odometry): an Odometry type message from the subscriber.
        """
        self.pos = convert_pose_to_xy_and_theta(msg.pose.pose)

    def run_loop(self):
        """Keeps the robot moving unless a bump is registered. If a bump is registered, turn around and drive away"""
        # Create a Twist message to describe the robot motion
        if self.body_pos is None:
            self.body_pos = self.pos

        vel = Twist()

        rel_pos = [a - b for a, b in zip(self.pos, self.body_pos)]

        if self.segment_start_pos is None:
            self.segment_start_pos = self.pos  # mark starting point

        dx = self.pos[0] - self.segment_start_pos[0]
        dy = self.pos[1] - self.segment_start_pos[1]
        traveled = math.hypot(dx, dy)
        dist = 0.5 # distance to drive away from wall (m)

        # If the bump sensor is triggered, stop the vehicle
        if self.bump_state == True:
            #vel.linear.x = 0.0
            print("bumped")
            vel.linear.x = -0.1
            sleep(0.5)
            vel.linear.x = 0
            while abs(rel_pos[2]) - self.rotation < 0.001:
                vel.angular.z = -0.2
            vel.angular.z = 0
            while(traveled < dist - 0.02):
                vel.linear.x = 0.2
        else:
            vel.linear.x = 0.0

        # Publish the Twist message to cmd_vel target
        self.publisher.publish(vel)

def main(args=None):
    """Initialize our node, run it, cleanup on shut down"""
    print("hi",flush=True)
    rclpy.init(args=args)  # Initialize ROS2 network
    node = EmergencyStopNode()  # Create our node
    rclpy.spin(node)  # Run our node
    rclpy.shutdown()  # If interrupted, gracefully shutdown the ROS2 network

if __name__ == '__main__':
    main()