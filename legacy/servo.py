import serial
import time
import math

# Initialize serial connection
arduino = serial.Serial('COM9', 9600, timeout=1)  # Update COM port as needed
time.sleep(2)  # Allow time for Arduino to initialize

import math

class imu_reading:
    def __init__(self, ax, ay, az, wx, wy, wz, z=0):
        self.ax = ax
        self.ay = ay
        self.az = az
        self.wx = wx
        self.wy = wy
        self.wz = wz
        

    def get_angle(self):
        # Accelerometer-based pitch and roll (in radians)
        pitch_acc = math.atan2(self.ay, math.sqrt(self.ax**2 + self.az**2))
        roll_acc = math.atan2(-self.ax, math.sqrt(self.ay**2 + self.az**2))

        # Return the angles in degrees
        return (math.degrees(pitch_acc),math.degrees(roll_acc))  

    def __str__(self):
        return f"Accelerations (m/s**2): {self.ax}, {self.ay}, {self.az}\tVelocity (rad/s): {self.wx}, {self.wy}, {self.wz}"  

def read_sensor_value(): # button on Pin6
    """Retrieve the value of the sensor on pin 6."""
    arduino.write(b'READ_SENSOR\n')
    time.sleep(0.1)
    data = arduino.readline().decode().strip()
    return int(data) if data.isdigit() else None

def control_servo_7(angle): # Servo on Pin7
    """Command servo on pin 7 to move to a specific angle."""
    command = f'SERVO7:{angle}\n'
    arduino.write(command.encode())
    time.sleep(0.1)
    response = arduino.readline().decode().strip()
    return response

def control_servo_8(angle): #Servo on Pin8
    """Command servo on pin 8 to move to a specific angle."""
    command = f'SERVO8:{angle}\n'
    arduino.write(command.encode())
    time.sleep(0.1)
    response = arduino.readline().decode().strip()
    return response

def read_ultrasonic_distance():
    """Read the distance from the ultrasonic sensor in centimeters."""
    arduino.write(b'READ_ULTRASONIC\n')
    time.sleep(0.1)
    data = arduino.readline().decode().strip()
    return int(data) if data.isdigit() else None

def read_mpu6050():
    """Retrieve accelerometer and gyroscope data from the MPU6050."""
    arduino.write(b'READ_MPU6050\n')
    time.sleep(0.1)
    data = arduino.readline().decode().strip()
    if data:
        try:
            ax, ay, az, gx, gy, gz = map(float, data.split(","))
            return imu_reading(ax,ay,az,gx,gy,gz)
        except ValueError:
            return None
    return None

def tilted(threshold=10):
    read = read_mpu6050()
    if read is not None:
        tiltx, tilty = read.get_angle()
        return abs(tiltx) >= threshold or abs(tilty) >= threshold
    return

# def main():
#     # Example logic
#     for _ in range(30):

#         sensor_value = int(read_sensor_value())
#         distance = int(read_ultrasonic_distance())

#         print("Sensor Value: ", sensor_value)
#         print("UltraS Value: ", distance)

#         mode = distance < 30 and distance > 5 # in reular range => False, close => True

#         if mode:
#             if sensor_value == 0:
#                 print(control_servo_7(0))
#             else:
#                 print(control_servo_7(90))

#         else:
#             if sensor_value == 0:
#                 print(control_servo_8(0))
#             else:
#                 print(control_servo_8(90))

#         time.sleep(1)
#         print()

def main():

    dt = 2

    for i in range(10):
        print(control_servo_8(0))
        time.sleep(dt)
        print(control_servo_8(90))
        time.sleep(dt)
        print(control_servo_8(180))
        time.sleep(dt)

if __name__ == '__main__':
    main()