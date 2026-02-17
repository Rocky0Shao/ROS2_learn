Project: The Autonomous Speed Governor
1. Project Goal
Create two nodes:

vehicle_node: Publishes random speeds (0-100) and hosts a "Reset" service.

governor_node: Subscribes to the speed. If speed > 80, it calls the "Reset" service to force the vehicle back to 0.

2. Technical Specifications
Package Setup
Package Name: speed_control

Build System: ament_python

Dependencies: rclpy, std_msgs, std_srvs

Node 1: vehicle_node.py
Publisher: Topic /speed, type std_msgs/msg/Int32, frequency 2Hz (0.5s).

Service Server: Name /reset_vehicle, type std_srvs/srv/Trigger.

Logic: * Maintain a class variable self.current_speed.

The timer callback publishes self.current_speed, then fluctuates it randomly.

The service callback sets self.current_speed = 0 and returns success=True.

Node 2: governor_node.py
Subscriber: Topic /speed, type std_msgs/msg/Int32.

Service Client: Name /reset_vehicle, type std_srvs/srv/Trigger.

Logic:

In the subscription callback: if msg.data > 80: self.call_reset_service().

Use client.call_async(request) to prevent the subscriber from hanging.

3. Implementation Steps (The 1-Hour Sprint)
Step 1: Create the Package (5 mins)
Bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python speed_control --dependencies rclpy std_msgs std_srvs
Step 2: The Vehicle Node (20 mins)
Define a timer that increments speed.

Define a service that resets speed.

Tip: Remember to import random.

Step 3: The Governor Node (20 mins)
Define the subscriber.

Define the client and the call_reset_service method.

Tip: Use self.get_logger().info() so you can see the "Speeding detected!" alert in the terminal.

Step 4: Config & Build (10 mins)
Add entry points to setup.py:

Python
'vehicle = speed_control.vehicle_node:main',
'governor = speed_control.governor_node:main',
Run colcon build --packages-select speed_control.

Step 5: Test (5 mins)
Terminal 1: ros2 run speed_control vehicle

Terminal 2: ros2 run speed_control governor

4. Success Criteria
You are finished when:

Vehicle logs: "Publishing Speed: 85"

Governor logs: "Speed too high! Sending reset request..."

Vehicle logs: "Service received! Resetting speed to 0."

Vehicle logs: "Publishing Speed: 0"