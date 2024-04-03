import time
import threading
import logging

import click
import dotenv
import serial
import genlib.ansiec as ansiec
import genlib.slip as slip
import genlib.udp as udp

class Serial2Udp(serial.Serial):
    def __init__(self, sport, baudrate, ip, group, iport, mcast, log_name):
        try:
            super().__init__(sport, baudrate, timeout=0.001)
        except serial.serialutil.SerialException as e:
            self.running = False
            print(f"Serial port({sport}) not found.")
        else:
            self.running = True
            
            if mcast:
                self.__sock = udp.MulticastSender(group, iport)
            else:
                self.__sock = udp.UDPClient(ip, iport)
                
            self.__slip = slip.Slip()
            
            self.__is_stop = False
            self.__log_name = log_name  
            
            self.__recv_thread = threading.Thread(target=self.__serial2inet, daemon=True)
            self.__send_thread = threading.Thread(target=self.__inet2serial, daemon=True)
            self.__recv_thread.start()
            self.__send_thread.start()
                
    def __serial2inet(self):
        while not self.__is_stop:
            try:
                for payload in self.__slip.decode(self.read(self.in_waiting)):
                    logging.getLogger(self.__log_name).info(payload)
                    self.__sock.sendTo(payload)
            except serial.serialutil.SerialException:
                print(f"Serial port({self.port}) is disconnected.")
                self.running = False
                self.__is_stop = True

            time.sleep(100/1000000.0) #usleep

    def __inet2serial(self):
        while not self.__is_stop:
            message = self.__sock.recvFrom()
            if message:
                logging.getLogger(self.__log_name).info(message.payload)
                self.write(self.__slip.encode(message.payload))
                time.sleep(0.01) #Minimized deley (10ms)

    def close(self):
        self.__is_stop = True
        self.__send_thread.join()
        self.__recv_thread.join()

def alarm():
    print("Serial Internet Bridge is now running.")
    print("Pressing the <Ctrl>c key terminates the program.")        

config = dotenv.find_dotenv(filename=".xkit", usecwd=True)
if config:
    dotenv.load_dotenv(dotenv_path=config)

@click.command()
@click.option(
    "--sport",
    envvar="SERIAL_PORT",
    required=True,
    type=click.STRING,
    help="Name of serial port for connected board.",
    metavar="SPORT",
)
@click.option(
    "--baud",
    envvar="SERIAL_BAUD",
    default=115200,
    type=click.INT,
    help="Baud rate for the serial connection (default 115200)",
    metavar="BAUD",
)
@click.option(
    "--ip",
    envvar="HOST_IP",
    default='127.0.0.1',
    type=click.STRING,
    help="UDP Server Addrress (default '127.0.0.1')",
    metavar="IP",
)
@click.option(
    "--group",
    envvar="MCAST_GROUP",
    default='239.8.7.6',
    type=click.STRING,
    help="UDP Multicast Group (default '239.8.7.6')",
    metavar="GROUP",
)
@click.option(
    "--iport",
    envvar="HOST_PORT",
    default=7321,
    type=click.INT,
    help="UDP Server or Multicast Group Port (default 7321).",
    metavar="IPORT",
)
@click.option(
    "--mcast",
    envvar="MCAST",
    default=False,
    type=click.BOOL,
    help="Enable Multicast (default False)",
    metavar="MCAST",
)
@click.option(
    "--log",
    envvar="LOG",
    default='None',
    type=click.STRING,
    help="Data Logging (default none)",
    metavar="LOG",
)
def main(sport, baud, ip, group, iport, mcast, log): 
    logger = logging.getLogger('stream')
    logger.setLevel(logging.INFO)
    logger = logging.getLogger('file')
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(ansiec.ANSIEC.FG.BRIGHT_YELLOW + '[%(asctime)s]' + ansiec.ANSIEC.FG.BRIGHT_CYAN + '%(funcName)s: ' + ansiec.ANSIEC.OP.RESET + '%(message)s')
    formatter_file = logging.Formatter('[%(asctime)s]%(funcName)s: %(message)s')
    log_name = ''
        
    if log.lower() == 'none':
        logger.setLevel(logging.NOTSET)
    elif log.lower() == 'stream':
        log_name = 'stream'
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger = logging.getLogger(log_name)
        logger.addHandler(handler)
        alarm()
    else:
        log_name = 'file'
        handler = logging.FileHandler(log)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter_file)
        logger = logging.getLogger(log_name)
        logger.addHandler(handler)
        alarm()
            
    s2u = Serial2Udp(sport, baud, ip, group, iport, mcast, log_name)
    
    while s2u.running:
        time.sleep(0.001)

if __name__ == "__main__":   
    main()