# imumaster

This library currently supports attitude estimation for inertial sensors in a common coordinate system. It utilizes the Extended Kalman Filter (EKF) algorithm to estimate orientation based on sensor data from a nine-axis sensor (accelerometer, gyroscope, magnetometer), providing the result of attitude estimation during the motion process of inertial sensors in the form of Euler angles and quaternions.

The IMU sensor and the ground coordinate system are both right-handed coordinate systems.

IMU sensor coordinate system definition: the x-axis points forward, the y-axis points left, and the z-axis points upward.
Ground coordinate system definition: the x-axis points north, the y-axis points west, and the z-axis points upward.

The IMU sensor and the ground coordinate system are defined as follows:

    IMU sensor coordinate system (xyz points towards):
    NWU (North, West, Up): x-axis points north, y-axis points west, and z-axis points upward.
    NED (North, East, Down): x-axis points north, y-axis points east, and z-axis points downward.
    ENU (East, North, Up): x-axis points east, y-axis points north, and z-axis points upward.

Euler angle definition:

    Roll: rotation around the x-axis.
    Pitch: rotation around the y-axis.
    Yaw: rotation around the z-axis.

Additionally, it provides general quaternion calculation functions such as addition, subtraction, multiplication, conjugation, inversion, norm calculation, and normalization.

# Attitude Estimation

## 1.download

    pip install imumaster

## 2.import

    import imumaster

## 3.example。
    
    >>> orientation = imumaster.Orientation(sample_rate=100, frame='ENU', method='EKF')
    >>> accel_data = np.array([0.06, 0.03, 0.99])
    >>> gyro_data = np.array([0.1, 0.2, 0.3])
    >>> mag_data = np.array([0.3, 0.1, 0.2])
    >>> q_estimation = orientation.EKF(accel_data, gyro_data, mag_data)
    >>> eulerangle = orientation.eulerangle(q_estimation)


