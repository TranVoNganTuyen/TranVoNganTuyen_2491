import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow
import requests


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        plain_text = self.ui.txt_plain_text.toPlainText().strip()
        key = self.ui.txt_key.text().strip()

        if not plain_text:
            QMessageBox.warning(self, "Warning", "Please enter plain text")
            return

        if not key:
            QMessageBox.warning(self, "Warning", "Please enter key")
            return

        url = "http://127.0.0.1:5000/api/caesar/encrypt"

        payload = {
            "plain_text": plain_text,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)
            print("Encrypt status:", response.status_code)
            print("Encrypt response:", response.text)

            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setPlainText(data["encrypted_text"])

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Success")
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Error", "Error while calling API")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Request error: {e}")

    def call_api_decrypt(self):
        cipher_text = self.ui.txt_cipher_text.toPlainText().strip()
        key = self.ui.txt_key.text().strip()

        if not cipher_text:
            QMessageBox.warning(self, "Warning", "Please enter cipher text")
            return

        if not key:
            QMessageBox.warning(self, "Warning", "Please enter key")
            return

        url = "http://127.0.0.1:5000/api/caesar/decrypt"

        payload = {
            "cipher_text": cipher_text,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)
            print("Decrypt status:", response.status_code)
            print("Decrypt response:", response.text)

            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setPlainText(data["decrypted_text"])

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Success")
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Error", "Error while calling API")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Request error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())