import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped

class PathVisualizer(Node):
    def __init__(self):
        super().__init__('path_visualizer')
        
        # Publishers for paths that RViz can easily display
        self.vins_path_pub = self.create_publisher(Path, '/vins_path', 10)
        self.gt_path_pub = self.create_publisher(Path, '/gt_path', 10)
        
        # Internal state to store paths
        self.vins_path = Path()
        self.gt_path = Path()
        
        # Subscribe to OpenVINS Odometry
        self.create_subscription(Odometry, '/ov_msckf/odomimu', self.vins_cb, 10)
        
        # Handle both types of Ground Truth just in case (Odometry or PoseStamped)
        self.create_subscription(PoseStamped, '/simple_drone/gt_pose', self.gt_pose_cb, 10)
        self.create_subscription(Odometry, '/simple_drone/odom', self.gt_odom_cb, 10)
        
        self.get_logger().info("Path visualizer started. Publishing to /vins_path and /gt_path")

    def vins_cb(self, msg: Odometry):
        pose_stamped = PoseStamped()
        pose_stamped.header = msg.header
        pose_stamped.pose = msg.pose.pose
        
        self.vins_path.header = msg.header
        self.vins_path.poses.append(pose_stamped)
        
        # Limit history to prevent lag
        if len(self.vins_path.poses) > 2000:
            self.vins_path.poses.pop(0)
            
        self.vins_path_pub.publish(self.vins_path)
        
    def gt_pose_cb(self, msg: PoseStamped):
        self.gt_path.header = msg.header
        self.gt_path.poses.append(msg)
        
        if len(self.gt_path.poses) > 2000:
            self.gt_path.poses.pop(0)
            
        self.gt_path_pub.publish(self.gt_path)

    def gt_odom_cb(self, msg: Odometry):
        pose_stamped = PoseStamped()
        pose_stamped.header = msg.header
        pose_stamped.pose = msg.pose.pose
        
        self.gt_path.header = msg.header
        self.gt_path.poses.append(pose_stamped)
        
        if len(self.gt_path.poses) > 2000:
            self.gt_path.poses.pop(0)
            
        self.gt_path_pub.publish(self.gt_path)

def main(args=None):
    rclpy.init(args=args)
    node = PathVisualizer()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()