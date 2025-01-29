import serial
import time
import math
import platform

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

class Arduino:

    def __init__(self, com='/dev/ttyUSB0', baud=9600, timeout=1):
        # Initialize serial connection
        ser = serial.Serial(com, baud, timeout=timeout)  # Update COM port as needed
        time.sleep(2)  # Allow time for Arduino to initialize
        self.ser = ser

    def write(self,string):
        self.ser.write(string.encode())

    def read(self):
        return self.ser.readline().decode().strip()

    def read_sensor_value(self): # button on Pin6
        """Retrieve the value of the sensor on pin 6."""
        self.write('READ_SENSOR\n')
        time.sleep(0.1)
        data = self.read()
        return int(data) if data.isdigit() else None

    def control_servo_7(self,angle): # Servo on Pin7
        """Command servo on pin 7 to move to a specific angle."""
        command = f'SERVO7:{angle}\n'
        self.write(command)
        time.sleep(0.1)
        response = self.read()
        return response

    def control_servo_8(self,angle): #Servo on Pin8
        """Command servo on pin 8 to move to a specific angle."""
        command = f'SERVO8:{angle}\n'
        self.write(command)
        time.sleep(0.1)
        response = self.read()
        return response

    def read_ultrasonic_distance(self):
        """Read the distance from the ultrasonic sensor in centimeters."""
        self.write('READ_ULTRASONIC\n')
        time.sleep(0.1)
        data = self.read()
        return int(data) if data.isdigit() else None

    def read_mpu6050(self):
        """Retrieve accelerometer and gyroscope data from the MPU6050."""
        self.write('READ_MPU6050\n')
        time.sleep(0.1)
        data = self.read()
        if data:
            try:
                ax, ay, az, gx, gy, gz = map(float, data.split(","))
                return imu_reading(ax,ay,az,gx,gy,gz)
            except ValueError:
                return None
        return None

    def tilted(self, threshold=10):
        read = self.read_mpu6050()
        if read is not None:
            tiltx, tilty = read.get_angle()
            return abs(tiltx) >= threshold or abs(tilty) >= threshold
        return

def main():

    system = platform.system()
    if system == "Windows":
        com = "COM9"
    elif system == "Linux":
        com = "/dev/ttyUSB0"

    arduino = Arduino(com=com)

    # Example logic
    for _ in range(30):

        tilt = arduino.tilted()
        distance = int(arduino.read_ultrasonic_distance())

        print("Sensor Value: ", tilt)
        print("UltraS Value: ", distance)

        mode = distance < 30 and distance > 5 # in reular range => False, close => True

        if mode:
            if tilt:
                print(arduino.control_servo_7(0))
            else:
                print(arduino.control_servo_7(90))

        else:
            if tilt:
                print(arduino.control_servo_8(0))
            else:
                print(arduino.control_servo_8(90))

        time.sleep(1)
        print()

if __name__ == '__main__':
    main()
