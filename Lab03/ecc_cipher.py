import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.ecc import Ui_MainWindow


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/ecc/generate_keys"
        try:
            res = requests.get(url)
            data = res.json()

            msg = QMessageBox()
            msg.setText(data["message"])
            msg.exec_()
        except Exception as e:
            print(e)

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/ecc/sign"

        payload = {
            "message": self.ui.txt_info.toPlainText()
        }

        res = requests.post(url, json=payload)
        data = res.json()

        self.ui.txt_sign.setText(data["signature"])

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/ecc/verify"

        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText()
        }

        res = requests.post(url, json=payload)
        data = res.json()

        msg = QMessageBox()

        if data["is_verified"]:
            msg.setText("Verified Successfully")
        else:
            msg.setText("Verified FAIL")

        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())