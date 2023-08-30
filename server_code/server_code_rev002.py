import socket
import threading
import json
import random

'''
Server Code
(c) 2023 TOMOMI RESEARCHm INC.
'''

# 01.サーバー設定
HEADER = 64
PORT = 6543  # 宮島様設定
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

state_kiko = True  # 機構の状態変数（True: OK, False: NG）

# 02.通信立ち上げ
# 02.01. Socket Making : socket()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 02.02. Address & Port : bind()
server_socket.bind(ADDR)


# 機構側制御の関数
def check_kikou_ready_state():
    # 機構側のReady状態確認するコードをここに書く
    # 返り値
    # 0 : Ready状態　False
    # 1 : Ready状態  True
    # ここでは、Ready状態　Trueと仮定して1を返す
    print('機構側のReady状態確認する')
    return True


def initialize_robot():
    # ロボットの初期化コードをここに書く
    # ここでは、初期化が成功したと仮定してTrueを返す
    print('機構側を初期化した。')
    return True


def transport_work():
    # ワークの搬送コードをここに書く
    print('ワークを搬送した。')
    return True


def rotate_work():
    # ステージの回転コードをここに書く
    print('回転ステージを60度回転した。')
    return True


def reverse_work():
    # ワークの反転コードをここに書く
    print('ワークを反転した。')
    return True


def eject_work(inspection_result):
    # ワークの排出コードをここに書く
    if inspection_result == 'OK':
        # OK側に排出
        pass
    elif inspection_result == 'NG':
        # NG側に排出
        pass
    print('ワークを排出した。')
    return True



def detect_out_of_work():
    # 100回に1回の確率でFalseを返す
    if random.randint(1, 100) == 1:
        result = True #ワーク切れ
        message = "Out of Work"
    else:
        result = False
        message = None

    return result, message

def detect_error_occured():
    # 100回に1回の確率でFalseを返す
    if random.randint(1, 100) == 1:
        result = True  # ワーク切れ
        message = "Some Error Occurred!"
    else:
        result = False
        message = None

    return result, message

def detect_alarm_triggered():
    # 100回に1回の確率でFalseを返す
    if random.randint(1, 100) == 1:
        result = True  # ワーク切れ
        message = "Alarm Triggered Now!"
    else:
        result = False
        message = None

    return result, message

def detect_emergency():
    # 100回に1回の確率でFalseを返す
    if random.randint(1, 100) == 1:
        result = True  # ワーク切れ
        message = "Emergency Detected !"
    else:
        result = False
        message = None

    return result, message

def monitor_status():
    global state_kiko  # グローバル変数を参照するための宣言

    # ワーク切れ状態、エラー発生状態、アラーム状態のチェックをここに書く

    state_out_of_work, message1 = detect_out_of_work() #ワークアウトを検出
    state_error_occurred, message2 = detect_error_occured() #エラー発生を検出
    state_alarm_triggered, message3 = detect_alarm_triggered() #アラームを検出
    state_emergency, message4 = detect_emergency() #Emergencyを検出

    # いずれかの状態変数がFalseであれば、state_kikoをFalseに設定
    if not state_out_of_work or not state_error_occurred or not state_alarm_triggered or not state_emergency:
        state_kiko = False
    else:
        state_kiko = True

    final_message = None
    # message1からmessage4までの変数をチェック
    for message in (message1, message2, message3, message4):
        if message is not None:
            final_message = message
            break

    # 返り値
    # 状態をdictonaryとして返す。
    print('機構の状態をチェックした。')
    return {
        'out_of_work': state_out_of_work,
        'error_occurred': state_error_occurred,
        'alarm_triggered': state_alarm_triggered,
        'emergency': state_emergency,
        'message': final_message
    }


# 下請け関数の定義
# 1. クライアントとの接続処理
# 2. コマンドの解析し、関連する処理を実行
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        # クライアントからのメッセージを受け取る
        data = conn.recv(HEADER).decode(FORMAT)
        if not data:
            print("Clent Disconnected.")
            break
        print("Received data:", data)

        # Parse the received data as JSON
        received_json = json.loads(data)

        # 受信したデータ (=command)をチェックし、関連するアクションを取る。
        # --------------------------------------------------------
        # 1. 初期化プロセス
        # 1.1.機構側のReady状態確認
        if received_json['command'] == 'GET_READY_STATUS':
            result = check_kikou_ready_state()
            if result:
                response = 1
            else:
                response = 0
        # 1.2.ロボットの初期化
        elif received_json['command'] == 'ZERO_RETURN':
            result = initialize_robot()
            if result:
                response = 1
            else:
                response = 0
        # --------------------------------------------------------
        # 2. 計測プロセス
        # 2.1.ワーク搬送指示
        elif received_json['command'] == 'CARRY_DRIVER_BIT':
            result = initialize_robot()
            if result:
                response = 1
            else:
                response = 0
        # 2.2. モーターの回転指示
        elif received_json['command'] == 'ROTATE':
            result = rotate_work()
            if result:
                response = 1
            else:
                response = 0
        # 2.3. ワークの反転指示
        elif received_json['command'] == 'REVERSE':
            result = reverse_work()
            if result:
                response = 1
            else:
                response = 0
        # 2.4. ワーク排出with判定結果
        elif received_json['command'] == 'INSPECTION_FINISHED':
            # コマンドの引数を確認　OKかNGか
            if received_json['arg'] == 'OK':
                result = eject_work(inspection_result='OK')
                if result:
                    response = 1
                else:
                    response = 0
            elif received_json['arg'] == 'NG':
                result = eject_work(inspection_result='NG')
                if result:
                    response = 1
                else:
                    response = 0
        # --------------------------------------------------------
        # 3. 状態監視プロセス
        # 3.1.状態監視
        elif received_json['command'] == 'GET_STATUS':
            response = monitor_status()

        # --------------------------------------------------------
        # 4. 例外処理
        else:
            response = 'Invalid command'
        # --------------------------------------------------------

        # responseをクライアントに送信
        conn.sendall(json.dumps({'message': response}).encode())


# クライアントへの対応処理　
def accept_client():
    # 03.03 クライアントからの接続を待つ : listen()
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]{threading.activeCount() - 1}")


if __name__ == "__main__":
    accept_client()
