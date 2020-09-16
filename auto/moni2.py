import os
import binascii as bina
from robotpi_serOp import serOp
from robotpi_Cmd import UPComBotCommand
import subprocess
import threading
import platform
import psutil
import json

class Monitor:
    def __init__(self):

        self.ser = serOp()
        self.com = UPComBotCommand()
        self.process = ''
        self.InT = self.InThread('')

    class InThread(threading.Thread):
        def __init__(self, name):
            self.superclass = Monitor()
            threading.Thread.__init__(self)
            self.name = name
            if 'Windows' in platform.platform():
                self.interpreter_path = 'C:/anaconda3/bin/pythonw.exe'
            else:
                self.interpreter_path = '/home/avi/anaconda3/bin/python3.6'
            self.program_name = ''
            self.program_on_desk = None
            self.pid = None

        def run(self):
            # self.start_operation(self.name)
            if self.pid is not None:
                self.superclass.stop()
                self.pid = None
            self.program_name = self.name + '.py'
            self.program_on_desk = subprocess.Popen([self.interpreter_path, self.program_name])
            self.pid = self.program_on_desk.pid
            with open('program_on_desk.json', 'w')as f:
                p = {}
                p['name'] = self.program_name
                p['pid'] = self.pid
                json.dump(p, f)
            print("starting at:", self.pid)
            self.program_on_desk.wait()

            return

        def get_thread(self, thread_name):
            pass


    def stop(self):
        with open('program_on_desk.json', 'r') as load_f:
            txt = json.load(load_f)
            pid = txt['pid']

            print("stopping", pid)
            os.system('kill -9 '+ str(pid))
            self.process = ''


        # def start_operation(self, name):
        #     if self.pid is not None:
        #         self.stop()
        #         self.pid = None
        #     self.program_name = name + '.py'
        #     self.program_on_desk = subprocess.Popen([self.interpreter_path, self.program_name])
        #     self.pid = self.program_on_desk.pid
        #     self.program_on_desk.wait()
        #     return

        def search_running(self):
            if self.pid is not None:
                p = psutil.Process(self.pid)
                return p.status()
            else:
                return

    def check_operation(self, data):
        if len(data) <6:
            return False
        check = data[2]
        check = check+data[3]
        check = check+data[4]
        for i in range(data[4]):
            check = check+data[5+i]
        if data[-1] == (~check) & 0xFF:
            return True
        else:
            return False

    def exe_command(self, data):
        thr = None
        if hex(data[2])[2:] != '9':
            print("Not a command for Pi.")
            return
        elif hex(data[3])[2:] == '47': # 运行程序
            b = b''
            for i in range(data[4]):
                h = hex(data[5+i])[2:]
                b += bina.a2b_hex(h)
                res = str(b)[2:-1]

            print("run %s please." % res)
            self.InThread.program_on_desk = res
            thr = self.InThread(res)
            self.process = res
            thr.start()


        elif hex(data[3])[2:] == '48': # 停止特定程序
            print("Stop a python scripts.")
            if data[4] == 0:
                return
            else:
                self.stop()

        elif hex(data[3])[2:] == '49': # 查看哪个程序在运行
            print("Which program is running?")
            return self.InThread.search_running()

        elif hex(data[3])[2:] == '4b':  # 查询有哪些可用的Demo
            names, len_names = self.search_demos()
            command, _ = self.com.GenerateCmd(device=int(data[2]), cmd=int(data[3]), len=len_names, data=names)
            # command, _ = com.GenerateCmd(device=int(data[2]), cmd=71, len=len_names, data=names)
            self.ser.write_serial(command)
            print("Demo names are returned.")
        return

    def search_demos(self):
        py_files = ''
        for i in os.listdir(os.getcwd()):
            if os.path.isfile(i):
                all_files = i.split('.')
                if all_files[-1] == 'py':
                    if len(all_files) == 4:
                        py_files += all_files[0]
                        py_files += '.'
                        py_files += all_files[1]
                        py_files += '.'
                        py_files += all_files[2]
                        if self.process +'.py' == i:
                            py_files += '-1'
                        else:
                            py_files += '-0'
                        py_files += ','

        files = py_files[:-1]
        file = []
        for i in range(len(files)):
            file.append(ord(files[i]))
        file_length = len(file)
        return file, file_length


if __name__ == '__main__':
    monitor = Monitor()
    # thr = monitor.InThread('barcode_scanner_video')
    # thr.start()
    # import time
    # time.sleep(10)
    # thr.stop()
    # print("OK")

    while True:
        data = None
        data = monitor.ser.serial_listen()
        # test = [0] * 1
        # test[0] = 1 & 0xFF
        # data, _ = monitor.com.GenerateCmd(device=0x09, cmd=0x47, len=0x01, data=test)
        # print("origin data:", data)

        if data:
            #mv.wave_hands()
            for i in data:
                print("data received:", hex(i))
            if monitor.check_operation(data):
                print("check OK.")
                monitor.exe_command(data)
            else:
                print("check False.")
        # break
#
#
