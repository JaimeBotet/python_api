from ftplib import FTP
import sys
import os

host = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
remote_file = sys.argv[4]
remote_dir = os.path.dirname(remote_file)
file_name =  os.path.basename(remote_file)
REPASAT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../priv_uploads/temp/ftp', remote_dir)
# command: python C:/xampp/htdocs/repasat/utils/ftp/downloadFile.py 82.98.147.243 ftp-alpha FLKu7y02.8w% e_168/foto_graffiti_before_2.png

ftp = FTP(host)
ftp.login(username, password)
ftp.cwd('repasat/download_ftp/' + remote_dir)


downloaded_file_path = ''
error_log = []

local_file = os.path.join(REPASAT_DIR, file_name)

try :
	directory = os.path.dirname(local_file)
	if not os.path.exists(directory):
		os.makedirs(directory)

	with open(local_file, 'wb') as f:
		ftp.retrbinary('RETR ' + file_name, f.write)
	downloaded_file_path = local_file
	ftp.delete(file_name)

except Exception as e:
	error_log.append('Error al descargar el archivo {}: {}'.format(file_name, str(e)))

ftp.quit()

print(downloaded_file_path)
print("===END_FILES===")

for error in error_log:
    print(error)