""" This node uses the laser scan measurement pointing straight ahead from
    the robot and compares it to a desired set distance.  The forward velocity
    of the robot is adjusted until the robot achieves the desired distance """

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
#from rclpy.parameter import Parameter
#from rcl_interfaces.msg import SetParametersResult
from rclpy.qos import qos_profile_sensor_data
from threading import Thread, Event
from time import sleep

class WallFollowingNode(Node):
    """ This class wraps the basic functionality of the node """
    def __init__(self):
        super().__init__('wall_following')
        #self.wall_follower = Event()
        # the run_loop adjusts the robot's velocity based on latest laser data
        self.create_timer(0.1, self.run_loop)
        self.create_subscription(LaserScan, 'scan', self.process_scan, qos_profile=qos_profile_sensor_data)
        self.vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        # distance_to_obstacle is used to communicate laser data to run_loop
        self.distance_to_obstacle = float('inf')
        # Kp is the constant or to apply to the proportional error signal
        self.Kp = 0.4
        # target_distance is the desired distance to the obstacle in front
        self.target_distance = 0.6
        self.target_near = 0.5
        self.target_far = 0.7
        self.close = False
        self.follower_state = "FORWARD"
        self.pc_front = None
        self.pc_turn = None
        #self.run_loop_thread = Thread(target=self.run_loop)
        #self.run_loop_thread.start()

    def run_loop(self):
        msg = Twist()
        self.close_enough()
        if self.follower_state == "FORWARD":
            self.drive_forward()
            print("run loop forward")
        elif self.follower_state == "ROTATE":
            self.determine_side()
            print("run loop rotate")
        #elif self.follower_state == "APPROACH":
        else:
            # use proportional control to set the velocity
            self.drive_approach()
            print("run loop approaching")
            
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
        print("drive func")

    def process_scan(self, msg):
        if msg.ranges[0] != 0.0:
            # checking for the value 0.0 ensures the data is valid.
            self.distance_to_obstacle = msg.ranges[0]
            self.distance_left = msg.ranges[90]
            self.distance_right = msg.ranges[270]
            self.distance_left_front = msg.ranges[45]
            self.distance_left_back = msg.ranges[135]
            self.distance_right_front = msg.ranges[315]
            self.distance_right_back = msg.ranges[225]
            
            self.distance_left_avg = sum(msg.ranges[45:135]) / 90
            self.distance_right_avg = sum(msg.ranges[225:315]) / 90

    def determine_side(self):
        msg = Twist()
        
        self.error_left = self.distance_left_front - self.distance_left_back
        self.error_right = self.distance_right_front - self.distance_right_back

        if abs(self.error_left) <= 0.2 or abs(self.error_right) <= 0.2: #needs to see if wall alignment is alr true
            self.follower_state = "FORWARD"
            print(f"wall aligned probably L: {self.error_left} R: {self.error_right}")
        elif self.distance_left_avg and self.distance_left_avg < self.distance_right_avg:
            self.pc_turn = -(self.Kp * self.error_left)
            #msg.angular.z = 0.3
            self.drive(linear=0.0, angular=0.3)
            print(f"wall on left L: {self.distance_left_avg} R: {self.distance_right_avg}")
        elif self.distance_right_avg and self.distance_right_avg < self.distance_left_avg:
            self.pc_turn = self.Kp * self.error_right
            #msg.angular.z = 0.3
            self.drive(linear=0.0, angular=0.3)
            print(f"wall on right L: {self.distance_left_avg} R: {self.distance_right_avg}")
        else:
            self.drive(linear=0.0, angular=0.3)
            #return

    def drive_forward(self):
        msg = Twist()
        #self.follower_state = "FORWARD"
        #self.drive(0.1, 0.0)
        #msg.linear.x = 0.4
        #self.vel_pub.publish(msg)
        
        if self.close == True:
            self.follower_state = "ROTATE"
            print("switch forward to rotate")
        elif self.distance_to_obstacle <= 1.5:
            self.follower_state = "APPROACH"
            print("switch forward to approach")
        else:
            self.drive(linear=0.4, angular=0.0)
            print("drive forward func")

    def drive_approach(self):
        msg = Twist()
        if self.close == True:
            self.follower_state = "ROTATE"
            print("switch approach to rotate")
        else:
            self.pc_front = self.Kp*(self.distance_to_obstacle - self.target_distance)
            self.follower_state = "APPROACH"
            self.drive(linear=self.pc_front, angular=0.0)
            #self.vel_pub.publish(msg)
            print(f"approach func {msg.linear.x}")
            #self.follower_state = "ROTATE"
            #print("switch approach to rotate (approach func)")

    def close_enough(self):
        if 0.5 < self.distance_to_obstacle < 0.7:
            self.close = True
        else: 
            self.close = False

        
def main(args=None):
    rclpy.init(args=args)
    node = WallFollowingNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
