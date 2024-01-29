from ftplib import FTP
import os
import io

def read_file(host, username, password, remote_file):
	try:
		ftp = FTP(host)
		ftp.login(username, password)
		remote_dir = os.path.dirname(remote_file)
		file_name = os.path.basename(remote_file)
		ftp.cwd('www/alpha/repasat/ftp/' + remote_dir)

		file = {
			"name": file_name,
			"ext": os.path.splitext(file_name)[1],
			"size": ftp.size(file_name) # size in bytes
		}

		ftp.quit()

		return file

	except Exception as e:
		return str(e)
	
def transfer_file(ftpSrc, ftpDst):
	error_log = []
	result = {
		"status": "OK",
		"file": None,
		"errors": None
	}
	remote_dir_src = os.path.dirname(ftpSrc["remoteFile"])
	file_name_src = os.path.basename(ftpSrc["remoteFile"])

	remote_dir_dst = os.path.dirname(ftpDst["remoteFile"])
	file_name_dst = os.path.basename(ftpDst["remoteFile"])

	try:
		ftp_src = FTP(ftpSrc["host"])
		ftp_src.login(ftpSrc["user"], ftpSrc["pass"])
		ftp_src.set_pasv(True)
		ftp_src.sendcmd('TYPE I')
		ftp_src.cwd('www/alpha/repasat/ftp/' + remote_dir_src)

		ftp_dst = FTP(ftpDst["host"])
		ftp_dst.login(ftpDst["user"], ftpDst["pass"])
		ftp_dst.set_pasv(True)
		ftp_dst.sendcmd('TYPE I')
		ftp_dst.cwd('upload_ftp/')
		dst_directories = remote_dir_dst.split('/')

		for directory in dst_directories:
			try:
				ftp_dst.cwd(directory)
			except Exception as cdException:
				if '550' in str(cdException):
					try:
						ftp_dst.mkd(directory)
						ftp_dst.cwd(directory)
					except Exception as mkdException:
						error_log.append("Error when creating directory {}: {}".format(directory, str(mkdException)))
				else:
					error_log.append("Error when switching directory {}: {}".format(directory, str(cdException)))
					break

		try:
			from_Sock = ftp_src.transfercmd("RETR {}".format(file_name_src))
			to_Sock = ftp_dst.transfercmd("STOR {}".format(file_name_dst))
			state = 0
			while True:
				data = from_Sock.recv(8192)
				print("Received data:", len(data)) 
				if not data:
					break
				state += len(data)
				to_Sock.sendall(data)

		except Exception as transferException:
			error_log.append("Error transfering file {}: {}".format(file_name_dst, str(transferException)))

		finally:
			result['file'] = {
				"name": file_name_dst,
				"dir": remote_dir_dst,
				"size": state
			}

			# do we delete the file from ftp_src?
			# ftp_src.delete(file_name_src)
			from_Sock.close()
			to_Sock.close()

	except Exception as e:
		error_log.append("Error with FTP: {}".format(str(e)))

	finally:
		ftp_src.quit()
		ftp_dst.quit()


	if len(error_log) > 0:
		result['errors'] = error_log
		result['status'] = "NOK"

	return result	

def download_file(host, username, password, remote_file, local_directory):
	try:
		ftp = FTP(host)
		ftp.login(username, password)
		remote_dir = os.path.dirname(remote_file)
		file_name = os.path.basename(remote_file)
		ftp.cwd('repasat/download_ftp/' + remote_dir)

		local_file = os.path.join(local_directory, file_name)
		if not os.path.exists(local_directory):
			os.makedirs(local_directory)

		with open(local_file, 'wb') as f:
			ftp.retrbinary('RETR ' + file_name, f.write)
		ftp.delete(file_name)
		ftp.quit()

		return local_file

	except Exception as e:
		return str(e)

def upload_file(host, username, password, file):
	try:
		ftp = FTP(host)
		ftp.login(username, password)

		try:
			file_name = file.filename
			file_content = file.read()
			file_like_object = io.BytesIO(file_content)
			ftp.storbinary('STOR ' + file_name, file_like_object)

		except Exception as e:
			return 'Error al subir el archivo {}: {}'.format(file.filename, str(e))

		ftp.quit()

		return file_name


	except Exception as e:
		return str(e)
	
