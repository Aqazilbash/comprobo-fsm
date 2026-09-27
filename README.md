Comprobo FSM - Maddy, Alex, Mik
## How To Run
Run the following commands concurrently:
ros2 run ros_behaviors_fsm emergency_stop_node
ros2 run ros_behaviors_fsm draw_square_node
ros2 run ros_behaviors_fsm wall_follower_node
ros2 run ros_behaviors_fsm dance_node
Then run:
ros2 run ros_behaviors_fsm fsm_node