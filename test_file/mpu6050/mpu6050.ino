#include <Wire.h>
#include <MPU6050.h>

// Create an MPU6050 object
MPU6050 mpu;

// Sensitivity factors for the MPU6050 (assuming ±2g for accelerometer and ±250°/s for gyroscope)
const float accelScale = 16384.0; // 16384 counts per g for ±2g
const float gyroScale = 131.0;    // 131 counts per °/s for ±250°/s
const float MY_DEG_TO_RAD = 3.14159 / 180.0;  // Conversion factor from degrees to radians
const float GRAVITY = 9.81;  // Earth's gravity in m/s²

void setup() {
  // Start serial communication
  Serial.begin(9600);

  // Initialize the MPU6050
  Wire.begin();
  mpu.initialize();

  // Check if the MPU6050 is connected properly
  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed");
    while (1);  // Halt if connection fails
  }

  Serial.println("MPU6050 initialized");
}

void loop() {
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

  // Print the results to the serial monitor
  Serial.print("Gyro X: ");
  Serial.print(gx_rad, 5);  // 5 decimal places for better precision
  Serial.print(" rad/s | Gyro Y: ");
  Serial.print(gy_rad, 5);
  Serial.print(" rad/s | Gyro Z: ");
  Serial.print(gz_rad, 5);
  Serial.print(" rad/s | ");
  
  Serial.print("Accel X: ");
  Serial.print(ax_m_s2, 4);  // 4 decimal places for precision
  Serial.print(" m/s² | Accel Y: ");
  Serial.print(ay_m_s2, 4);
  Serial.print(" m/s² | Accel Z: ");
  Serial.print(az_m_s2, 4);
  Serial.println(" m/s²");

  // Delay for a bit before the next reading
  delay(500);
}
