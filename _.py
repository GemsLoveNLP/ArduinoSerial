import serial
import time

# Initialize serial connection
arduino = serial.Serial('COM9', 9600, timeout=1)  # Update COM port as needed
time.sleep(2)  # Allow time for Arduino to initialize

def read_sensor_value():
    """Retrieve the value of the sensor on pin 6."""
    arduino.write(b'READ_SENSOR\n')
    time.sleep(0.1)
    data = arduino.readline().decode().strip()
    return int(data) if data.isdigit() else None

def control_servo_7(angle):
    """Command servo on pin 7 to move to a specific angle."""
    command = f'SERVO7:{angle}\n'
    arduino.write(command.encode())
    time.sleep(0.1)
    response = arduino.readline().decode().strip()
    return response

def control_servo_8(angle):
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

def main():
    # Example logic
    for _ in range(30):

        sensor_value = int(read_sensor_value())
        distance = int(read_ultrasonic_distance())

        print("Sensor Value: ", sensor_value)
        print("UltraS Value: ", distance)

        mode = distance < 30 and distance > 5 # in reular range => False, close => True

        if mode:
            if sensor_value == 0:
                print(control_servo_7(0))
            else:
                print(control_servo_7(90))

        else:
            if sensor_value == 0:
                print(control_servo_8(0))
            else:
                print(control_servo_8(90))

        time.sleep(1)
        print()

if __name__ == '__main__':
    main()
