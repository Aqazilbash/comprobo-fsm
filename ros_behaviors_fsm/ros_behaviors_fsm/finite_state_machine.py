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

        # Recieves msgs from drive_square to indicate when behavior is finished
        self.create_subscription(Bool, "finished", self.handle_finished, 10)

    def handle_finished(self, msg):
        # Callback for handling the finished message from the drive_square node.
        if msg.data:
            self.get_logger().info("Drive square finished, transitioning to IDLE state.")
            self.current_state = "IDLE"

    def handle_state(self, state):
        if state == 0:
            self.current_state = "IDLE"
            self.get_logger().info("Transitioning to IDLE state.")
        elif state == 1:
            self.current_state = "DRIVE_SQUARE"
            self.get_logger().info("Transitioning to DRIVE_SQUARE state.")
        elif state == 2:
            self.current_state = "WALL_FOLLOWER"
            self.get_logger().info("Transitioning to WALL_FOLLOWER state.")
        elif state == 3:
            self.current_state = "DANCE"
            self.get_logger().info("Transitioning to DANCE state.")

    def run_loop(self):
        # Main loop for the FSM. This function will be called repeatedly to check the current state and take appropriate actions.
        pass