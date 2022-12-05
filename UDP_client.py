import threading
import socket
import json
MAX_BYTES = 65535
server_addr = ('127.0.0.1',6000) # Remote server address
# 執行緒send_message()：取得使用者的輸入訊息字串，傳送到Server
def send_message():
    print('執行緒send_message開始')
    while(True):
        # 取得使用者輸入的聊天訊息
        msgtext = input('請輸入聊天訊息：')
        # 建立Message Request訊息的dict物件
        msgdict = {
            "type": 3,
            "nickname": nickname,
            "message": msgtext
        }
        # 轉成JSON字串，再轉成bytes
        msgdata = json.dumps(msgdict).encode('utf-8')
        print(msgdata)
        # 將Enter Request送到Server
        sock.sendto(msgdata, server_addr)
# 執行緒recv_message()：接收來自Server傳來的訊息，
# 依據訊息中的type欄位所代表的訊息型態作對應的處理    
def recv_message():
    print('執行緒recv_message開始')
    while(True):
        # 接收來自Server傳來的訊息
        data, address = sock.recvfrom(MAX_BYTES)
        msgdict = json.loads(data.decode('utf-8'))
        # 依照type欄位的值做對應的動作
        ## Message Response(4)：這是之前Message Request的回應訊息
        if msgdict['type'] == 4:
            # 不需做任何處理
            print('Get Message Response from server.') # 除錯用
            pass 
        ## Message Transfer(5)：這是其他Client所發布的訊息
        if msgdict['type'] == 5:
            print('Get Message Transfer from server.') # 除錯用
            # 以「nickname: message content」的格式印出
            print(msgdict['nickname'] + ': ' + msgdict['message'])
# 請使用者輸入他的nickname
nickname = input('請輸入你留言時的綽號/別名：')
# 建立一個UDP socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# 準備Enter Request訊息的dict物件
msgdict = {
    "type": 1,
    "nickname": nickname
}
# 轉成JSON字串，再轉成bytes
data = json.dumps(msgdict).encode('utf-8')
# 將Enter Request送到Server
sock.sendto(data, server_addr)
# 等待並接收Server傳回來的訊息，若為Enter Response則繼續下一步，否則繼續等待
is_entered = False
while not is_entered:
    data, address = sock.recvfrom(MAX_BYTES)
    msgdict = json.loads(data.decode('utf-8'))
    if msgdict['type'] == 2:
        is_entered = True
        print('成功進入伺服器!!!')
# 建立兩個threads：send_message與recv_message
thread_send_message = threading.Thread(target=send_message)
thread_recv_message = threading.Thread(target=recv_message)
thread_send_message.start()
thread_recv_message.start()
thread_send_message.join()
thread_recv_message.join()
print('程式結束')



