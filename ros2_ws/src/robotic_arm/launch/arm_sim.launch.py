#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from ros_ign_gazebo_interfaces.srv import SpawnEntity
import os

class SpawnArm(Node):
    def __init__(self):
        super().__init__('spawn_arm')
        self.cli = self.create_client(SpawnEntity, '/spawn_entity')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /spawn_entity service...')
        
        # Load SDF file
        pkg_path = os.path.expanduser('~/arm_description/src/arm_assembly_urdf_sldasm')
        sdf_path = os.path.join(pkg_path, 'urdf', 'arm_assembly.sdf')
        with open(sdf_path, 'r') as f:
            sdf_model = f.read()
        
        self.spawn_model(sdf_model)

    def spawn_model(self, sdf_model):
        req = SpawnEntity.Request()
        req.name = "arm_assembly"
        req.xml = sdf_model
        req.robot_namespace = "arm"
        req.initial_pose.position.x = 0.0
        req.initial_pose.position.y = 0.0
        req.initial_pose.position.z = 0.0

        self.future = self.cli.call_async(req)
        rclpy.spin_until_future_complete(self, self.future)
        if self.future.result() is not None:
            self.get_logger().info("Spawned arm successfully!")
        else:
            self.get_logger().error("Failed to spawn arm.")

def main(args=None):
    rclpy.init(args=args)
    node = SpawnArm()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
