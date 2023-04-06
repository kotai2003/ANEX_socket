import socket
import threading
import json

#サーバー設定
HEADER = 64
PORT = 6543 #宮島様設定
SERVER = "192.168.0.195" #サーバーのIPアドレス
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# コマンドリスト
## サーバー側：機構
server_commands = {"計測開始": "START_INSPECTION",
                   "回転終了": "TURN_ENDED"}

## クライアント側: AI
client_commands = {"運転状態取得": "GET_STATUS",
                   "計測終了":"INSPECTION_FINISHED",
                   "回転開始": "TURN60",
                   "エラー通知": "ERROR_OCCURED"}


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server :
    server.connect(ADDR)

    while True:
        # コマンドを入力
        command = input("Enter command: ")

        # コマンドをjson形式に変換
        data = {"command": command}
        message = json.dumps(data).encode()

        # サーバーに送信
        server.sendall(message)

        # サーバーからの応答を受信
        data = server.recv(1024).decode()
        print("Received from server: {}".format(data))


        # 受信したデータ (=command)をチェックし、関連するアクションを取る。
        if data == server_commands["計測開始"]:
            # 関連するアクションを取る。例えば、計測を終了する。
            print('Starting Inspection')

        elif data == server_commands["回転終了"]:
            # 関連するアクションを取る。例えば、計測を終了する。
            print('Rotation End Checked.')





