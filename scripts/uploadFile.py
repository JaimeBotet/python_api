from ftplib import FTP
import sys
import os

host = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
remote_file = sys.argv[4]
remote_dir = os.path.dirname(remote_file)
file_name =  os.path.basename(remote_file)
directories = remote_dir.split('/')
REPASAT_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../priv_uploads/temp/ftp', directories[0])
# command: python C:/xampp/htdocs/repasat/utils/ftp/uploadFile.py 82.98.147.243 ftp-alpha FLKu7y02.8w% e_168/2/5/4/4/2/0/foto_graffiti_before_2.png

uploaded_file_path = ''
error_log = []

ftp = FTP(host)
ftp.login(username, password)
ftp.cwd('repasat/upload_ftp/')

for directory in directories:
	try:
		ftp.cwd(directory)
	except Exception as e:
		if '550' in str(e):
			ftp.mkd(directory)
			ftp.cwd(directory)
		else:
			error_log.append("Error al cambiar al directorio {}: {}".format(directory, str(e)))
	
local_file = os.path.join(REPASAT_DIR, file_name)
try:
	with open(local_file, 'rb') as f:
		ftp.storbinary('STOR ' + file_name, f)
	uploaded_file_path = os.path.join(remote_dir, file_name)
	os.remove(local_file)

except Exception as e:
	error_log.append('Error al subir el archivo {}: {}'.format(local_file, str(e)))
	

ftp.quit()

print(uploaded_file_path)
print("===END_FILES===")

for error in error_log:
    print(error)