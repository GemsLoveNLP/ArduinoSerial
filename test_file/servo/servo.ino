#include <Servo.h> // Include the Servo library

Servo myServo; // Create a Servo object

void setup() {
  myServo.attach(8);        // Attach the servo to pin 9
  myServo.write(90);        // Set the servo to its middle position (90°)
  Serial.begin(9600);       // Initialize serial communication at 9600 baud
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the command until newline
    command.trim(); // Remove any whitespace

    // Convert the command to an integer
    int angle = command.toInt();

    // Ensure the angle is in the valid range
    if (angle >= -90 && angle <= 90) {
      int servoAngle = map(angle, -90, 90, 0, 180); // Map -90° to 90° to 0° to 180°
      myServo.write(servoAngle);                   // Move the servo to the desired angle
      Serial.print("Moved to: ");
      Serial.println(angle);                       // Feedback for debugging
    } else {
      Serial.println("Invalid angle: must be between -90 and 90"); // Feedback for invalid input
    }
  }
}
