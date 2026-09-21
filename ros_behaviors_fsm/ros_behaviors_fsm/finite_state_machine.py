import rclpy  # convenience python library for interacting with ROS2
from rclpy.node import Node  # generic Node class for interacting with ROS2
from std_msgs.msg import Bool

class FiniteStateMachine(Node):
    #This is a node which implements a finite state machine for controlling the robot's behavior.

    def __init__(self):
        # Initializes the class.
        super().__init__("finite_state_machine") # node name

        # Create a state that stores the current state of the FSM
        self.current_state = "IDLE"

        self.create_subscription(Bool, "finished", self.handle_finished, 10)

    def handle_finished(self, msg):
        # Callback for handling the finished message from the drive_square node.
        if msg.data:
            self.get_logger().info("Drive square finished, transitioning to IDLE state.")
            self.current_state = "IDLE"

    def run_loop(self):
        # Main loop for the FSM. This function will be called repeatedly to check the current state and take appropriate actions.
        if self.current_state == "IDLE":
            #let user choose a behavior to run
            pass
        elif self.current_state == "DRIVE_SQUARE":
            # Start the drive_square behavior
            self.get_logger().info("Starting drive square behavior.")

        elif self.current_state == "WALL_FOLLOWER":
            # Start the wall follower behavior
            self.get_logger().info("Starting wall follower behavior.")
            