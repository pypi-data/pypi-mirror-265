import threading
from views.Landing import Landing, Api
from services.Listener import Listener
import os
import socket

class Launcher:
    def __init__(self):
        Launcher.validar_puerto()
        user_home = os.path.expanduser("~")
        port = 30505
        api_landing = Api()
        api_landing._port_api = port
        listener = threading.Thread(target=Listener, args=(port, api_landing,))
        listener.start()
        Landing(api_landing, debug=False)
        listener.join()

    @staticmethod
    def validar_puerto():
        port = 30505
        cmd = f"netstat -aon | findstr :{port}"
        output = os.popen(cmd)
        output_read = output.read()
        output.close()
        if output_read:
            lines = output_read.split('\n')
            for line in lines:
                if f":{port}" in line:
                    pid = int(line.strip().split()[-1])
                    if pid:
                        print(f"El proceso que está utilizando el puerto {port} es {pid}")
                        os.system(f"taskkill /F /PID {pid}")
                    else:
                        print(f"El puerto {port} está en uso pero no se pudo determinar el proceso asociado.")
                    return
            print(f"No se encontró ningún proceso utilizando el puerto {port}.")
        else:
            print(f"El puerto {port} no está en uso.")

if __name__ == '__main__':
    Launcher()
