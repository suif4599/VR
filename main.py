from game.sensor import MySerial, Rocker, RockerViewer, MPU6050



ser = MySerial("COM3", 57600)
rocker = Rocker(ser)
mpu = MPU6050(ser)
@mpu
def print_data(self):
    print(f"{mpu.AccX: .2f}, {mpu.AccY: .2f}, {mpu.AccZ: .2f}, {mpu.GyroX: .2f}, {mpu.GyroY: .2f}, {mpu.GyroZ: .2f}, {mpu.Temp: .2f}")
    print(f"{mpu.theta / 3.1415 * 180 : .0f}, {mpu.phi / 3.1415 * 180 : .0f}")

view = RockerViewer(rocker)
view.mainloop()