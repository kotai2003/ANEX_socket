import socket
import threading
import json

#サーバー設定
HEADER = 64
PORT = 6543 #宮島様設定
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#01. Socket Making : socket()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#02. Address & Port : bind()
server.bind(ADDR)

# コマンドリスト
## サーバー側：機構
server_commands = {"計測開始": "START_INSPECTION",
                   "回転終了": "TURN_ENDED"}

## クライアント側: AI
client_commands = {"運転状態取得": "GET_STATUS",
                   "計測終了":"INSPECTION_FINISHED",
                   "回転開始": "TURN60",
                   "エラー通知": "ERROR_OCCURED"}


# 下請け関数の定義
# 1. クライアントとの接続処理
# 2. コマンドの解析し、関連する処理を実行

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        #クライアントからのコマンドを受信する
        data = conn.recv(HEADER).decode(FORMAT)
        if not data:
            print("Clent Disconnected.")
            break
        print("Received data:", data)

        #Parse the received data as JSON
        received_json = json.loads(data)


        #受信したデータ (=command)をチェックし、関連するアクションを取る。
        if received_json['command'] == client_commands["運転状態取得"]:
            # クライアント側に'OK’メッセージを返す
            conn.sendall(json.dumps({'message': 'OK'}).encode())
        elif received_json['command'] == client_commands["回転開始"]:
            # 関連するアクションを取る。例えば、ロボットを60度で回す。
            print('Rotating the robot by 60 degrees')
            # その後、クライアント側に"START_INSPECTION" を送る。
            conn.sendall(json.dumps({'command': server_commands["計測開始"]}).encode())
        elif received_json['command'] == client_commands["計測終了"]:
            # 関連するアクションを取る。例えば、計測を終了する。
            print('Stopping the inspection')
            # クライアント側に'OK’メッセージを返す
            conn.sendall(json.dumps({'message': 'Message Received'}).encode())

        elif received_json['command'] == client_commands["エラー通知"]:
            # 関連するアクションを取る。例えば、エラーを処理する。
            print('Handling the error')
            # クライアント側に'OK’メッセージを返す
            conn.sendall(json.dumps({'message': 'Message Received'}).encode())

    # Close the connection
    conn.close()



# クライアントへの対応処理　

def accept_client():
    # 03. Waiting the connection : listen()
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]{threading.activeCount() -1}")


if __name__ == "__main__":

    accept_client()








