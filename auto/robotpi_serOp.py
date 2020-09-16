import serial

class serOp():
    ser = serial.Serial(
            port="/dev/ttyUSB0",
            baudrate=115200,
            bytesize=8,
            parity='E',
            stopbits=1,
            timeout=2)
    isOpen = True

    def __int__(self):
        self.isOpen = True
        
    def open(self):
        self.ser.open()
        if(serOp.ser.isOpen):
            self.isOpen = True
            print ("open")
        else:
            self.isOpen = False

    def serial_listen(self):
        data = []
        while serOp.ser.inWaiting() > 0:
            k = serOp.ser.read()
            data.append(int.from_bytes(k, byteorder='big', signed=False))
        return data

    def serial_string(self):
        data = b''
        while serOp.ser.inWaiting() > 0:
            k = serOp.ser.read()
            data += k
        return data[5:-1]

    def write_serial(self, command):
        self.ser.write(command)


if __name__ == '__main__':
    from robotpi_Cmd import UPComBotCommand

    com = UPComBotCommand()
    ser = serOp()
    while True:
        test = [0] * 1
        test[0] = 2 & 0xFF
        send_data, _ = com.GenerateCmd(device=0x09, cmd=0x4B, len=0x00, data=None)
        print("origin data:", send_data)
        ser.write_serial(send_data)
        break
        recv_data = ser.serial_listen()
        if recv_data:
            #mv.wave_hands()
            for i in recv_data:
                print("data received:", hex(i))
            print("____")
            break

