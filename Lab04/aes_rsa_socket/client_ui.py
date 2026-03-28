import sys
import socket
import threading
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout

class ClientUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES-RSA Client")
        self.setGeometry(200, 200, 500, 450)

        self.client_socket = None
        self.client_key = RSA.generate(2048)
        self.aes_key = None

        # UI
        self.txtHost = QTextEdit()
        self.txtHost.setFixedHeight(30)
        self.txtHost.setPlaceholderText("Host")

        self.txtPort = QTextEdit()
        self.txtPort.setFixedHeight(30)
        self.txtPort.setPlaceholderText("Port")

        self.btnConnect = QPushButton("Connect")

        self.txtChat = QTextEdit()
        self.txtChat.setReadOnly(True)

        self.txtMessage = QTextEdit()
        self.txtMessage.setFixedHeight(60)

        self.btnSend = QPushButton("Send")

        layout = QVBoxLayout()

        row = QHBoxLayout()
        row.addWidget(self.txtHost)
        row.addWidget(self.txtPort)
        row.addWidget(self.btnConnect)
        layout.addLayout(row)

        layout.addWidget(self.txtChat)
        layout.addWidget(self.txtMessage)
        layout.addWidget(self.btnSend)

        self.setLayout(layout)

        self.btnConnect.clicked.connect(self.connect_server)
        self.btnSend.clicked.connect(self.send_message)

    def encrypt(self, key, msg):
        cipher = AES.new(key, AES.MODE_CBC)
        return cipher.iv + cipher.encrypt(pad(msg.encode(), AES.block_size))

    def decrypt(self, key, data):
        iv = data[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(data[16:]), AES.block_size).decode()

    def connect_server(self):
        host = self.txtHost.toPlainText().strip()
        port = int(self.txtPort.toPlainText().strip())

        self.client_socket = socket.socket()
        self.client_socket.connect((host, port))

        # receive server key
        server_key = RSA.import_key(self.client_socket.recv(2048))

        # send client key
        self.client_socket.send(self.client_key.publickey().export_key())

        # receive AES key
        encrypted_key = self.client_socket.recv(2048)
        cipher_rsa = PKCS1_OAEP.new(self.client_key)
        self.aes_key = cipher_rsa.decrypt(encrypted_key)

        self.txtChat.append("Connected to server")

        threading.Thread(target=self.receive, daemon=True).start()

    def receive(self):
        while True:
            try:
                data = self.client_socket.recv(4096)
                msg = self.decrypt(self.aes_key, data)
                self.txtChat.append(msg)
            except:
                break

    def send_message(self):
        msg = self.txtMessage.toPlainText().strip()
        if not msg:
            return

        self.client_socket.send(self.encrypt(self.aes_key, msg))
        self.txtChat.append(f"Me: {msg}")
        self.txtMessage.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientUI()
    window.show()
    sys.exit(app.exec_())