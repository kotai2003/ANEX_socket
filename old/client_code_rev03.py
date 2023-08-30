import socket
import threading
import json
import time
import random

# サーバー設定
HEADER = 64
PORT = 6543  # 宮島様設定
SERVER = "192.168.0.100"  # サーバーのIPアドレス
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


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


def monitor_status(client_socket):
    # 監視スレッド専用のソケットを作成
    monitor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    monitor_socket.connect(ADDR)
    while True:
        # コマンドをjson形式に変換
        data = {"command": 'GET_STATUS'}
        received_message = json.dumps(data).encode()
        # サーバーに送信
        monitor_socket.sendall(received_message)
        # サーバーからの応答受信
        response01 = monitor_socket.recv(1024).decode()
        # print(response01)

        with status_lock:
            system_status.update(json.loads(response01)['message'])
            # print(json.loads(response01)['message'])


        print(f'System status: {system_status}')
        print(system_status['message'])
        time.sleep(1)  # サーバーが過負荷にならないように、適度にスリープします
    # サーバーとの接続を終了
    monitor_socket.close()


if __name__ == '__main__':
    # ソケットオブジェクトの作成
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # サーバーのホスト名とポートを指定して接続
    client_socket.connect(ADDR)

    # 監視スレッドを開始
    monitor_thread = threading.Thread(target=monitor_status, args=(client_socket,))
    monitor_thread.start()

    #--------------------------------------------------------
    # Main Program
    #--------------------------------------------------------
    # 1. 初期化プロセス
    # 1.1.機構側のReady状態確認
    message = json.dumps({"command": 'GET_READY_STATUS'}).encode()
    client_socket.send(message)
    res = client_socket.recv(1024).decode()
    response = json.loads(res)['message']
    print(f'Response from server: {response}')

    # 1.2.ロボットの初期化
    message = json.dumps({"command": 'ZERO_RETURN'}).encode()
    client_socket.send(message)
    res = client_socket.recv(1024).decode()
    response = json.loads(res)['message']
    print(f'Response from server: {response}')

    # ... その他の計測プロセスなど ...
    # --------------------------------------------------------
    # 2. 計測プロセス
    # ワークがなくなるまで計測プロセスを繰り返す

    number_of_work = 0

    while True:
        with status_lock:
            if system_status['out_of_work']:
                break

            AI_result = True
            # 2.1.ワーク搬送指示
            message = json.dumps({"command": 'CARRY_DRIVER_BIT'}).encode()
            client_socket.send(message)
            res = client_socket.recv(1024).decode()
            response = json.loads(res)['message']
            # print(f'Response from server: {response}')

            done = False  # 制御用の変数
            for _ in range(2):
                for _ in range(6):
                    # 撮像＆AI検査
                    image_data = capture_image()
                    AI_result = ai_anomaly_detection(image_data)

                    # NGの場合ループの外に出る。
                    if not AI_result:
                        done = True
                        break

                    # 2.2. モーターの回転指示
                    message = json.dumps({"command": 'ROTATE'}).encode()
                    client_socket.send(message)
                    res = client_socket.recv(1024).decode()
                    response = json.loads(res)['message']
                    # print(f'Response from server: {response}')

                # 2.3. ワークの反転指示
                message = json.dumps({"command": 'REVERSE'}).encode()
                client_socket.send(message)
                res = client_socket.recv(1024).decode()
                response = json.loads(res)['message']
                # print(f'Response from server: {response}')

                if done:  # 外側のループも終了
                    break

            # 2.4. ワーク排出with判定結果
            message = json.dumps({"command": 'INSPECTION_FINISHED',
                                  "arg": AI_result}).encode()
            client_socket.send(message)
            res = client_socket.recv(1024).decode()
            response = json.loads(res)['message']
            # print(f'Response from server: {response}')

    # サーバーとの接続を終了
    client_socket.close()
