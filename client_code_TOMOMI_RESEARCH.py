import socket
import threading
import json
import time
import random

# ClientConnection Class

class ClientConnection:
    def __init__(self, server_ip, port):
        '''
        :param server_ip: IP address
        :param port: Port Number
        '''
        self.server_ip = server_ip
        self.port = port
        self.socket = None
        self.monitor_thread = None
        self.monitoring = False

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_ip, self.port))

    def disconnect(self):
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
            self.monitor_thread = None
        if self.socket:
            self.socket.close()
            self.socket = None

    def send_command(self, command, arg=None):
        if not self.socket:
            raise Exception("Not connected to the server.")
        data = {"command": command}
        if arg is not None:
            data["arg"] = arg
        message = json.dumps(data).encode()
        self.socket.send(message)
        res = self.socket.recv(1024).decode()
        response = json.loads(res)['message']
        return response

    def read(self):
        return {
            "server_ip": self.server_ip,
            "port": self.port
        }

    def analyze_response(self, command, response):
        if command in ['GET_READY_STATUS', 'ZERO_RETURN']:
            return "OK" if response == 1 else "NG"

        elif command in ['CARRY_DRIVER_BIT', 'ROTATE', 'REVERSE', 'INSPECTION_FINISHED OK', 'INSPECTION_FINISHED NG']:
            if response == 1:
                return "Normal"
            elif response == 0:
                return "Error"
            elif response == -1:
                return "Emergency Stop"

        elif command == 'GET_STATUS':
            return response  # This is already a dictionary with the system status

        else:
            return None  # For any other unexpected command


    def check_response(self, command, response, error_message):
        action = self.analyze_response(command, response)
        if action in ["NG", "Error", "Emergency Stop"]:
            print(error_message)
            return False
        return True


    def monitor_status(self):
        while self.monitoring:
            status = self.send_command('GET_STATUS')
            print(f'System status: {status}') #システム状態を出力
            time.sleep(1)  # Ensure server is not overloaded

    def start_monitoring(self):
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_status)
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
            self.monitor_thread = None

# Sample usage:
# client = ClientConnection("192.168.0.100", 6543)
# client.connect()
# client.start_monitoring()
# ... other operations
# client.stop_monitoring()
# client.disconnect()

# Original functions and variables
def capture_image():
    # カメラから画像を取得するコードをここに書く
    # ここでは、ダミーの画像データを返す
    return 'dummy image data'


def ai_anomaly_detection(image_data):
    # AIによる異常検知のコードをここに書く
    # 10回に1回の確率でFalseを返す
    if random.randint(1, 10) == 1:
        return False
    return True


# システムの状態を格納するグローバル変数とロック
system_status = {
    'out_of_work': False,
    'error_occurred': False,
    'alarm_triggered': False,
    'emergency': False,
    'message' : None
}
status_lock = threading.Lock()

#Main Program

if __name__ == '__main__':

    # Initialize the client connection
    client = ClientConnection("192.168.0.195", 6543)
    client.connect()
    client.start_monitoring() #start monitoring

    # --------------------------------------------------------
    # Main Program
    # --------------------------------------------------------
    # 1. 初期化プロセス
    # 1.1.機構側のReady状態確認
    response = client.send_command('GET_READY_STATUS')
    if not client.check_response('GET_READY_STATUS', response, "Initialization failed. Exiting..."):
        client.disconnect()
        exit()

    # 1.2.ロボットの初期化
    response = client.send_command('ZERO_RETURN')
    if not client.check_response('ZERO_RETURN', response, "Robot initialization failed. Exiting..."):
        client.disconnect()
        exit()

    # ... その他の計測プロセスなど ...
    # --------------------------------------------------------
    # 2. 計測プロセス
    # ワークがなくなるまで計測プロセスを繰り返す

    while True:
        with status_lock:
            if system_status['out_of_work']:
                break

            AI_result = True
            response = client.send_command('CARRY_DRIVER_BIT')
            if not client.check_response('CARRY_DRIVER_BIT', response, "Error during CARRY_DRIVER_BIT. Exiting..."):
                break

            loop_control = False
            # 制御用の変数　
            # loop_control = Falseの場合、撮像とAI検査を続けます。
            # loop_control = Trueの場合、ループを終了します。
            for _ in range(2):
                for _ in range(6):
                    # 撮像＆AI検査
                    image_data = capture_image()
                    AI_result = ai_anomaly_detection(image_data)
                    #AI結果がOKの場合
                    response = client.send_command('INSPECTION_FINISHED_OK')
                    # NGの場合ループの外に出る。
                    if not AI_result:
                        response = client.send_command('INSPECTION_FINISHED_NG')
                        if not client.check_response('INSPECTION_FINISHED_NG', response,
                                                     "AI inspection failed. Exiting..."):
                            loop_control = True
                            break
                    # 2.2. モーターの回転指示
                    response = client.send_command('ROTATE')
                    if not client.check_response('ROTATE', response, "Error during ROTATE. Exiting..."):
                        loop_control = True
                        break


                # 2.3. ワークの反転指示
                response = client.send_command('REVERSE')
                if not client.check_response('REVERSE', response, "Error during REVERSE. Exiting..."):
                    loop_control = True
                    break
            # 2.4. ワーク排出with判定結果
            response = client.send_command('INSPECTION_FINISHED', AI_result)
            if not client.check_response('INSPECTION_FINISHED', response,
                                         "Error during INSPECTION_FINISHED. Exiting..."):
                break

    client.stop_monitoring() #stop monitoring
    client.disconnect() #接続close



