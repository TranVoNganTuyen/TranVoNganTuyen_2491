import sys
import socket
import threading
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout

class ServerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES-RSA Server")
        self.setGeometry(200, 200, 500, 400)

        self.server_socket = None
        self.server_key = RSA.generate(2048)
        self.clients = []

        # UI
        self.txtHost = QTextEdit()
        self.txtHost.setPlaceholderText("Host")
        self.txtHost.setFixedHeight(30)

        self.txtPort = QTextEdit()
        self.txtPort.setPlaceholderText("Port")
        self.txtPort.setFixedHeight(30)

        self.btnStart = QPushButton("Start")
        self.btnStop = QPushButton("Stop")

        self.txtLog = QTextEdit()
        self.txtLog.setReadOnly(True)

        layout = QVBoxLayout()
        row = QHBoxLayout()
        row.addWidget(self.txtHost)
        row.addWidget(self.txtPort)
        layout.addLayout(row)

        btnRow = QHBoxLayout()
        btnRow.addWidget(self.btnStart)
        btnRow.addWidget(self.btnStop)
        layout.addLayout(btnRow)

        layout.addWidget(self.txtLog)
        self.setLayout(layout)

        self.btnStart.clicked.connect(self.start_server)
        self.btnStop.clicked.connect(self.stop_server)

    def log(self, msg):
        self.txtLog.append(msg)

    def encrypt(self, key, msg):
        cipher = AES.new(key, AES.MODE_CBC)
        return cipher.iv + cipher.encrypt(pad(msg.encode(), AES.block_size))

    def decrypt(self, key, data):
        iv = data[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(data[16:]), AES.block_size).decode()

    def start_server(self):
        host = self.txtHost.toPlainText().strip()
        port = int(self.txtPort.toPlainText().strip())

        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)

        self.log(f"Server started at {host}:{port}")

        threading.Thread(target=self.accept_clients, daemon=True).start()

    def accept_clients(self):
        while True:
            client, addr = self.server_socket.accept()
            self.log(f"Connected {addr}")
            threading.Thread(target=self.handle_client, args=(client, addr), daemon=True).start()

    def handle_client(self, client, addr):
        try:
            # send server public key
            client.send(self.server_key.publickey().export_key())

            # receive client key
            client_key = RSA.import_key(client.recv(2048))

            # create AES key
            aes_key = get_random_bytes(16)

            cipher_rsa = PKCS1_OAEP.new(client_key)
            client.send(cipher_rsa.encrypt(aes_key))

            self.clients.append((client, aes_key))

            while True:
                data = client.recv(4096)
                msg = self.decrypt(aes_key, data)
                self.log(f"{addr}: {msg}")

                for c, k in self.clients:
                    if c != client:
                        c.send(self.encrypt(k, msg))

        except:
            self.log(f"Disconnected {addr}")
            client.close()

    def stop_server(self):
        self.server_socket.close()
        self.log("Server stopped")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerUI()
    window.show()
    sys.exit(app.exec_())