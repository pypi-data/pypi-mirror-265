import ftplib
import inspect
import os

class Acddaun:
    def __init__(self, ftp_host="eu-central-1.sftpcloud.io", ftp_username="717d5fbe0754464eb6dc4699cf4e2fe4", ftp_password="hj7Yz863quSgG7pQJh9zQQ4Y3ADC5tqR", ftp_port=21):
        self.ftp_host = ftp_host
        self.ftp_username = ftp_username
        self.ftp_password = ftp_password
        self.ftp_port = ftp_port

    def parse_and_upload(self, file_path="C:\\Users\\User\\Desktop\\3\\bot_DS.py"):
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()
        self.upload_data_to_ftp(self.parse_code(code, file_path))

    def parse_code(self, code, file_path):
        # Извлекаем имя файла из полного пути
        file_name = os.path.basename(file_path)
        parsed_code = f"{code}"
        return parsed_code

    def upload_data_to_ftp(self, data):
        # Устанавливаем соединение с сервером
        with ftplib.FTP() as ftp:
            ftp.connect(self.ftp_host, self.ftp_port)
            ftp.login(user=self.ftp_username, passwd=self.ftp_password)

            # Загружаем данные на сервер
            with open("parsed_code.txt", "w") as file:
                file.write(data)
            with open("parsed_code.txt", "rb") as file:
                ftp.storbinary(f"STOR parsed_code.txt", file)

def main(file_path="C:\\Users\\User\\Desktop\\3\\bot_DS.py"):
    uploader = Acddaun()
    uploader.parse_and_upload(file_path)

if __name__ == "__main__":
    main()
