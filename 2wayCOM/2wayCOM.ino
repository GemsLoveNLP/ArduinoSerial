#include <Wire.h>
#include <Servo.h>
#include "MPU6050.h"

// Pin definitions
const int trigPin = 12;
const int echoPin = 13;
const int sensorPin = 6;
const int servoPin6 = 6;
const int servoPin7 = 7;
const int servoPin8 = 8;
const int servoPin9 = 9;

// // Sensitivity factors for the MPU6050 (assuming ±2g for accelerometer and ±250°/s for gyroscope)
const float accelScale = 16384.0; // 16384 counts per g for ±2g
const float gyroScale = 131.0;    // 131 counts per °/s for ±250°/s
const float MY_DEG_TO_RAD = 3.14159 / 180.0;  // Conversion factor from degrees to radians
const float GRAVITY = 9.81;  // Earth's gravity in m/s²

// Servo objects
Servo servo6;
Servo servo7;
Servo servo8;
Servo servo9;

// // MPU6050 object
MPU6050 mpu;

void setup() {
    Serial.begin(9600);

    // Set up ultrasonic sensor pins
    // pinMode(trigPin, OUTPUT);
    // pinMode(echoPin, INPUT);

    // Attach servos
    servo6.attach(servoPin6);
    servo7.attach(servoPin7);
    servo8.attach(servoPin8);
    servo9.attach(servoPin9);

    // Initialize MPU6050
    Wire.begin();
    mpu.initialize();
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        command.trim();

        if (command.startsWith("READ_SENSOR")) {
            int sensorValue = digitalRead(sensorPin);
            Serial.println(sensorValue);
        }
        else if (command.startsWith("SERVO6:")) {
            int angle = command.substring(7).toInt();
            servo6.write(angle);
            Serial.println("Servo 6 moved");
        }
        else if (command.startsWith("SERVO7:")) {
            int angle = command.substring(7).toInt();
            servo7.write(angle);
            Serial.println("Servo 7 moved");
        } 
        else if (command.startsWith("SERVO8:")) {
            int angle = command.substring(7).toInt();
            servo8.write(angle);
            Serial.println("Servo 8 moved");
        }
        else if (command.startsWith("SERVO9:")) {
            int angle = command.substring(7).toInt();
            servo9.write(angle);
            Serial.println("Servo 9 moved");
        } 
        // else if (command.startsWith("READ_ULTRASONIC")) {
        //     long duration, distance;
        //     digitalWrite(trigPin, LOW);
        //     delayMicroseconds(2);
        //     digitalWrite(trigPin, HIGH);
        //     delayMicroseconds(10);
        //     digitalWrite(trigPin, LOW);

        //     duration = pulseIn(echoPin, HIGH);
        //     distance = duration * 0.034 / 2;
        //     Serial.println(distance);
        // } 
        else if (command.startsWith("READ_MPU6050")) {
            // Variables to store raw accelerometer and gyroscope values
            int16_t ax, ay, az, gx, gy, gz;

            // Read the accelerometer and gyroscope values
            mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

            // Convert the raw accelerometer values to 'g' (gravitational units)
            float ax_g = ax / accelScale;
            float ay_g = ay / accelScale;
            float az_g = az / accelScale;

            // Convert the accelerometer values to m/s²
            float ax_m_s2 = ax_g * GRAVITY;
            float ay_m_s2 = ay_g * GRAVITY;
            float az_m_s2 = az_g * GRAVITY;

            // Convert the raw gyroscope values to 'rad/s' (radians per second)
            float gx_rad = gx / gyroScale * MY_DEG_TO_RAD;  // Convert from °/s to rad/s
            float gy_rad = gy / gyroScale * MY_DEG_TO_RAD;
            float gz_rad = gz / gyroScale * MY_DEG_TO_RAD;

            // Send data as a comma-separated string
            Serial.print(ax_m_s2); Serial.print(",");
            Serial.print(ay_m_s2); Serial.print(",");
            Serial.print(az_m_s2); Serial.print(",");
            Serial.print(gx_rad); Serial.print(",");
            Serial.print(gy_rad); Serial.print(",");
            Serial.println(gz_rad);
        }
    }
}
