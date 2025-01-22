#include <Servo.h>

// Pin definitions
const int trigPin = 12;
const int echoPin = 13;
const int sensorPin = 6;
const int servoPin7 = 7;
const int servoPin8 = 8;

// Servo objects
Servo servo7;
Servo servo8;

void setup() {
    Serial.begin(9600);
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    servo7.attach(servoPin7);
    servo8.attach(servoPin8);
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        command.trim();

        if (command.startsWith("READ_SENSOR")) {
            int sensorValue = digitalRead(sensorPin);
            Serial.println(sensorValue);
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
        else if (command.startsWith("READ_ULTRASONIC")) {
            long duration, distance;
            digitalWrite(trigPin, LOW);
            delayMicroseconds(2);
            digitalWrite(trigPin, HIGH);
            delayMicroseconds(10);
            digitalWrite(trigPin, LOW);

            duration = pulseIn(echoPin, HIGH);
            distance = duration * 0.034 / 2;
            Serial.println(distance);
        }
    }
}
