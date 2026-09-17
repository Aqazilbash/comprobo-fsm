import rclpy  # convenience python library for interacting with ROS2
from rclpy.node import Node  # generic Node class for interacting with ROS2
from neato2_interfaces.msg import Bump  # local package call for a Bump type message format
from geometry_msgs.msg import Twist  # ROS package call for a Twist type message format

class EmergencyStopNode(Node):
    """This is a node which stops the motors when the bump sensor is triggered.
    
    The class should allow the vehicle to move forward at a slow rate, until the
    bump sensor is triggered, in which case the robot should stop.
    
    Publishers Needed:
        - Twist cmd_vel message; which commands vehicle velocity
    Subscribers Needed:
        - Bump bump message handling; which listens for the bump sensor data
    """
    def __init__(self):
        """Initializes the class."""
        super().__init__("emergency_stop_node") # node names should be unique
        # Create a timer that runs the robot motors
        self.create_timer(0.1, self.run_loop)

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


    def run_loop(self):
        """Keeps the robot moving unless a bump is registered."""
        # Create a Twist message to describe the robot motion
        vel = Twist()

        # If the bump sensor is triggered, stop the vehicle
        if self.bump_state == True:
            vel.linear.x = 0.0
        else:
            vel.linear.x = 0.1

        # Publish the Twist message to cmd_vel target
        self.publisher.publish(vel)

def main(args=None):
    """Initialize our node, run it, cleanup on shut down"""
    rclpy.init(args=args)  # Initialize ROS2 network
    node = EmergencyStopNode()  # Create our node
    rclpy.spin(node)  # Run our node
    rclpy.shutdown()  # If interrupted, gracefully shutdown the ROS2 network

if __name__ == '__main__':
    main()