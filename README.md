# Subsea Robotics ROS Workspace

A ROS/ROS 2 workspace containing core navigation, control, and data processing packages for subsea autonomous vehicles.

## Packages

* **autonomous_docking**: Provides control, alignment, and sensor feedback logic for guiding a subsea vehicle into an underwater docking station.
* **gps_denied_fusion**: Implements sensor fusion algorithms (such as Extended Kalman Filters) to combine IMU, DVL, and depth sensor data for accurate underwater localization without GPS.
* **sonar_data_pipeline**: Manages the ingestion, filtering, and publishing data streams from acoustic and sonar sensors for obstacle detection and mapping.
