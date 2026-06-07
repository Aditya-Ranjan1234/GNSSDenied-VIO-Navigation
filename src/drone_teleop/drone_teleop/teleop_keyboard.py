import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
import sys
import select
import termios
import tty

msg = """
SJTU Drone Teleop
---------------------------
Movement Controls (Hold to move, release to stop):
        W    
   A    S    D

W/S : Forward/Backward (0.6 m/s)
A/D : Left/Right Strafing (0.6 m/s)

Up/Down Arrows : Move Up/Down (0.5 m/s)
Left/Right Arrows : Yaw Left/Right (0.8 rad/s)

Space : Hover/Stop forcefully
T     : Takeoff
L     : Land
Q     : Quit

CTRL-C to quit
"""

move_bindings = {
    'w': (0.6, 0.0, 0.0, 0.0),
    's': (-0.6, 0.0, 0.0, 0.0),
    'a': (0.0, 0.6, 0.0, 0.0),
    'd': (0.0, -0.6, 0.0, 0.0),
    '\x1b[A': (0.0, 0.0, 0.5, 0.0), # Up arrow
    '\x1b[B': (0.0, 0.0, -0.5, 0.0), # Down arrow
    '\x1b[C': (0.0, 0.0, 0.0, -0.8), # Right arrow
    '\x1b[D': (0.0, 0.0, 0.0, 0.8), # Left arrow
}

class TeleopKeyboard(Node):
    def __init__(self):
        super().__init__('teleop_keyboard')
        self.cmd_vel_pub = self.create_publisher(Twist, '/simple_drone/cmd_vel', 10)
        self.takeoff_pub = self.create_publisher(Empty, '/simple_drone/takeoff', 10)
        self.land_pub = self.create_publisher(Empty, '/simple_drone/land', 10)
        
        # Publish at 20Hz
        self.timer = self.create_timer(1.0 / 20.0, self.timer_callback)
        
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.th = 0.0
        
        self.timeout_counter = 0
        self.stopped = True
        
        self.get_logger().info(msg)

    def timer_callback(self):
        twist = Twist()
        twist.linear.x = self.x
        twist.linear.y = self.y
        twist.linear.z = self.z
        twist.angular.z = self.th
        self.cmd_vel_pub.publish(twist)

def getKey(settings):
    tty.setraw(sys.stdin.fileno())
    # select with timeout 0.01 makes it non-blocking
    rlist, _, _ = select.select([sys.stdin], [], [], 0.01)
    if rlist:
        key = sys.stdin.read(1)
        if key == '\x1b':
            # Handle escape sequences (like arrow keys)
            rlist2, _, _ = select.select([sys.stdin], [], [], 0.01)
            if rlist2:
                key += sys.stdin.read(2)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main(args=None):
    # Save terminal settings
    settings = termios.tcgetattr(sys.stdin)

    rclpy.init(args=args)
    node = TeleopKeyboard()

    try:
        while rclpy.ok():
            key = getKey(settings)
            
            if key != '':
                node.timeout_counter = 0

            if key in move_bindings.keys():
                node.x = move_bindings[key][0]
                node.y = move_bindings[key][1]
                node.z = move_bindings[key][2]
                node.th = move_bindings[key][3]
                node.stopped = False
            elif key == ' ':
                node.x = 0.0
                node.y = 0.0
                node.z = 0.0
                node.th = 0.0
                node.stopped = True
            elif key == 't' or key == 'T':
                node.takeoff_pub.publish(Empty())
            elif key == 'l' or key == 'L':
                node.land_pub.publish(Empty())
            elif key == 'q' or key == 'Q' or key == '\x03':
                break
            else:
                # If no key is received, increment timeout
                node.timeout_counter += 1
                # Timeout of ~40 ticks roughly translates to ~0.4s 
                # to account for terminal auto-repeat delay.
                if node.timeout_counter > 40: 
                    node.x = 0.0
                    node.y = 0.0
                    node.z = 0.0
                    node.th = 0.0
                    if not node.stopped:
                        node.stopped = True
                
            # Process ROS callbacks (like the timer)
            rclpy.spin_once(node, timeout_sec=0)
            
    except Exception as e:
        print(f"Exception: {e}")

    finally:
        # Stop the drone before exiting
        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        node.cmd_vel_pub.publish(twist)
        
        # Restore terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()