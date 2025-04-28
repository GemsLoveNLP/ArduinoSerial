import serial
import time
import math

# Initialize serial connection
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Update COM port as needed
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

def control_servo_6(angle): # Servo on Pin6
    """Command servo on pin 6 to move to a specific angle."""
    command = f'SERVO6:{angle}\n'
    arduino.write(command.encode())
    time.sleep(0.01)
    response = arduino.readline().decode().strip()
    return response

def control_servo_7(angle): # Servo on Pin7
    """Command servo on pin 7 to move to a specific angle."""
    command = f'SERVO7:{angle}\n'
    arduino.write(command.encode())
    time.sleep(0.01)
    response = arduino.readline().decode().strip()
    return response

def control_servo_8(angle): #Servo on Pin8
    """Command servo on pin 8 to move to a specific angle."""
    command = f'SERVO8:{angle}\n'
    arduino.write(command.encode())
    time.sleep(0.01)
    response = arduino.readline().decode().strip()
    return response

def control_servo_9(angle): #Servo on Pin9
    """Command servo on pin 9 to move to a specific angle."""
    command = f'SERVO9:{angle}\n'
    arduino.write(command.encode())
    time.sleep(0.01)
    response = arduino.readline().decode().strip()
    return response

def read_ultrasonic_distance():
    """Read the distance from the ultrasonic sensor in centimeters."""
    arduino.write(b'READ_ULTRASONIC\n')
    time.sleep(0.01)
    data = arduino.readline().decode().strip()
    return int(data) if data.isdigit() else None

def read_mpu6050():
    """Retrieve accelerometer and gyroscope data from the MPU6050."""
    arduino.write(b'READ_MPU6050\n')
    time.sleep(0.01)
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

def control_servos_setup(angle):
    for i in range(6, 10):
        # Calculate new local angle
        local_angle = angle
        if local_angle < 0:
            local_angle = 0
        elif local_angle > 180:
            local_angle = 180
        local_angle = int(local_angle)
        # command the servo to move to the new angle
        command = f'SERVO{i}:{local_angle}\n'
        arduino.write(command.encode())
        time.sleep(0.001)
        response = arduino.readline().decode().strip()
        print(response)

def calculate_piecewise_linear_params(y_points, x_points=[0,90,180]):
    if len(x_points) != 3 or len(y_points) != 3:
        raise ValueError("Exactly three points are required.")
    
    # First segment (low x to mid x)
    slope1 = (y_points[1] - y_points[0]) / (x_points[1] - x_points[0])
    intercept1 = y_points[0] - slope1 * x_points[0]
    
    # Second segment (mid x to high x)
    slope2 = (y_points[2] - y_points[1]) / (x_points[2] - x_points[1])
    intercept2 = y_points[1] - slope2 * x_points[1]
    
    return (slope1, intercept1), (slope2, intercept2)


def control_servos(angle):
    """Command all servos to move to a specific angle."""
    # Note:
    # Servo 6: Top Right (Red) -> 92 degrees
    # Servo 7: Bottom Right -> 90 degrees
    # Servo 8: Bottom Left -> 95 degrees
    # Servo 9: Top Left -> 98 degrees
    # angle += 90 (to make 0 degrees the center)
    x = [(12,81,150),
         (22,92,163),
         (13,82,150),
         (24,92,160)]
    coefs = [calculate_piecewise_linear_params(y_points=tup) for tup in x]
    new_angles = [coef1[0]*angle + coef1[1] 
                  if angle < 90 else 
                  coef2[0]*angle + coef2[1] 
                  for coef1, coef2 in coefs]
    print(new_angles)
    for i in range(6, 10):
        local_angle = new_angles[i-6]
        if local_angle < 0:
            local_angle = 0
        elif local_angle > 180:
            local_angle = 180
        local_angle = int(local_angle)
        # command the servo to move to the new angle
        command = f'SERVO{i}:{local_angle}\n'
        arduino.write(command.encode())
        time.sleep(0.001)
        response = arduino.readline().decode().strip()
        print(response)

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

# mid point is 105, 

# for TIANKONGRC -> 24, 90, 153:: 20.7 mm thick disc

def main():

    dt = 1

    while True:

        angle = input("Enter the angle: ")
        if not angle.isnumeric():
            return
        print(control_servos(int(angle)))
        time.sleep(dt)  

        # num = input("servo code: ")
        # exec(f"control_servo_{num}(0)")

        # num = input("servo code: ")
        # exec(f"control_servo_{num}(90)")

        # input("enter: ")

        # control_servo_6(0)
        # time.sleep(0.5)
        # control_servo_7(0)
        # time.sleep(0.5)
        # control_servo_8(0)
        # time.sleep(0.5)
        # control_servo_9(0)
        # time.sleep(0.5)


        # input("enter: ")
        # control_servo_6(90)
        # time.sleep(0.5)
        # control_servo_7(90)
        # time.sleep(0.5)
        # control_servo_8(90)
        # time.sleep(0.5)
        # control_servo_9(90)
        # time.sleep(0.5)

# current servo config -> 93 degree = 0 degree

if __name__ == '__main__':
    main()