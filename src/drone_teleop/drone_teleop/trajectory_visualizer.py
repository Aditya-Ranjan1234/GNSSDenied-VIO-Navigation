#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker


class TrajectoryVisualizer(Node):
    def __init__(self):
        super().__init__('trajectory_visualizer')

        # Publishers
        self.gt_marker_pub = self.create_publisher(
            Marker, '/drone/gt_trajectory', 10
        )

        self.vio_marker_pub = self.create_publisher(
            Marker, '/drone/vio_trajectory', 10
        )

        # Marker initialization
        self.gt_marker = Marker()
        self.gt_marker.header.frame_id = 'world'
        self.gt_marker.ns = 'gt_trajectory'
        self.gt_marker.id = 0
        self.gt_marker.type = Marker.LINE_STRIP
        self.gt_marker.action = Marker.ADD
        self.gt_marker.pose.orientation.w = 1.0
        self.gt_marker.scale.x = 0.05  # Line width
        self.gt_marker.color.r = 1.0  # Red
        self.gt_marker.color.g = 0.0
        self.gt_marker.color.b = 0.0
        self.gt_marker.color.a = 1.0

        self.vio_marker = Marker()
        self.vio_marker.header.frame_id = 'world'
        self.vio_marker.ns = 'vio_trajectory'
        self.vio_marker.id = 1
        self.vio_marker.type = Marker.LINE_STRIP
        self.vio_marker.action = Marker.ADD
        self.vio_marker.pose.orientation.w = 1.0
        self.vio_marker.scale.x = 0.05
        self.vio_marker.color.r = 0.0  # Green
        self.vio_marker.color.g = 1.0
        self.vio_marker.color.b = 0.0
        self.vio_marker.color.a = 1.0

        # Subscribers
        self.create_subscription(
            PoseStamped,
            '/simple_drone/gt_pose',
            self.gt_pose_callback,
            10
        )

        self.create_subscription(
            PoseStamped,
            '/ov_msckf/poseimu',
            self.vio_pose_callback,
            10
        )

        self.timer = self.create_timer(0.1, self.timer_callback)

        self.gt_positions = []
        self.vio_positions = []

    def gt_pose_callback(self, msg):
        self.gt_positions.append(msg.pose.position)

        # Keep only last 1000 points
        if len(self.gt_positions) > 1000:
            self.gt_positions.pop(0)

    def vio_pose_callback(self, msg):
        self.vio_positions.append(msg.pose.position)

        if len(self.vio_positions) > 1000:
            self.vio_positions.pop(0)

    def timer_callback(self):
        # Update GT Marker
        self.gt_marker.header.stamp = self.get_clock().now().to_msg()
        self.gt_marker.points = self.gt_positions
        self.gt_marker_pub.publish(self.gt_marker)

        # Update VIO Marker
        self.vio_marker.header.stamp = self.get_clock().now().to_msg()
        self.vio_marker.points = self.vio_positions
        self.vio_marker_pub.publish(self.vio_marker)


def main(args=None):
    rclpy.init(args=args)

    trajectory_visualizer = TrajectoryVisualizer()

    try:
        rclpy.spin(trajectory_visualizer)
    except KeyboardInterrupt:
        pass
    finally:
        trajectory_visualizer.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
