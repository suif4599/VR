#include<Wire.h>

class Rocker {
  protected:
    int GND, VCC, VAX, VAY, SW;
    char buffer[25];
  public:
    Rocker(int VAX, int VAY, int SW, int GND = -999, int VCC = -999) {
      this->GND = GND;
      this->VCC = VCC;
      this->VAX = VAX;
      this->VAY = VAY;
      this->SW = SW;
      if (GND != -999) {
        pinMode(GND, OUTPUT);
        digitalWrite(GND, 0);
      };
      if (VCC != -999) {
        pinMode(VCC, OUTPUT);
        digitalWrite(VCC, 1);
      };
      pinMode(VAX, INPUT);
      pinMode(VAY, INPUT);
      pinMode(SW, INPUT);
    };
    void send(void) {
      int x = analogRead(this->VAX);
      int y = analogRead(this->VAY);
      int sw = analogRead(this->SW);
      sprintf(buffer, "Rocker: %d, %d, %d", x, y, sw);
      Serial.println(buffer);
    };
};

class MPU6050 {
  /* Note:
   * Vcc = 3V3
   * SDA = A4
   * SCL = A5
   */
  protected:
    int MPU6050_addr;
    char buffer[64];
  public:
    MPU6050(int addr) {
      this->MPU6050_addr = addr;
    };
    void init() {
      Wire.begin();
      Wire.beginTransmission(this->MPU6050_addr);
      Wire.write(0x6B);
      Wire.write(0);
      Wire.endTransmission(true);
    };
    void send() {
      int16_t AccX, AccY, AccZ, TempRaw, GyroX, GyroY, GyroZ;
      Wire.beginTransmission(this->MPU6050_addr);
      Wire.write(0x3B);
      Wire.endTransmission(false);
      Wire.requestFrom(this->MPU6050_addr, 14, true);
      AccX = Wire.read() << 8 | Wire.read();
      AccY = Wire.read() << 8 | Wire.read();
      AccZ = Wire.read() << 8 | Wire.read();
      TempRaw = Wire.read() << 8 | Wire.read();
      GyroX = Wire.read() << 8 | Wire.read();
      GyroY = Wire.read() << 8 | Wire.read();
      GyroZ = Wire.read() << 8 | Wire.read();
      float Temp = TempRaw / 340.00 + 36.53;
      sprintf(buffer, "MPU6050: %d, %d, %d, %d, %d, %d, ", AccX, AccY, AccZ, GyroX, GyroY, GyroZ);
      Serial.print(buffer);
      Serial.println(Temp);
    };
};

MPU6050 mpu(0x68);
Rocker rocker(A1, A2, A3);
void setup() {
  mpu.init();
  Serial.begin(57600);
};

void loop() {
  mpu.send();
  rocker.send();
  delay(10);
};
