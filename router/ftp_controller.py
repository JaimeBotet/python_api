from flask import Blueprint, request, jsonify
import sys
# sys.path.append("/home/api-pyrepasat/www/repasat_api_py/scripts") # prod
sys.path.append('C:\\Users\\User\\Desktop\\Projects\\FTP_API_PY\\scripts') # dev
from ftp_utils import download_file, upload_file, transfer_file, read_file
import subprocess
import os

ftp_blueprint = Blueprint('ftp_blueprint', __name__, url_prefix='/ftp')

@ftp_blueprint.route('/test', methods=['GET'])
def test_fn():
	return 'This is test!'

@ftp_blueprint.route('/read', methods=['POST'])
def read_ftp_file():
	# ftp data from the common server
	ftp = {
		"host": request.form.get('ftpHost'),
		"user": request.form.get('ftpUser'),
		"pass": request.form.get('ftpPass'),
		"remoteFile": request.form.get('remoteFile')
	}

	try:
		result = read_file(ftp['host'], ftp['user'], ftp['pass'], ftp['remoteFile'])
		return jsonify({"message": "File read successfully", "result" : result})
	except subprocess.CalledProcessError as e:
		return jsonify({"error": "File read failed", "details": str(e)})

@ftp_blueprint.route('/transfer', methods=['POST'])
def transfer_ftp_file():
	# ftp data from the common server
	ftpSrc = {
		"host": request.form.get('ftpSrcHost'),
		"user": request.form.get('ftpSrcUser'),
		"pass": request.form.get('ftpSrcPass'),
		"remoteFile": request.form.get('srcRemoteFile')
	}

	ftpDst = {
		"host": request.form.get('ftpDstHost'),
		"user": request.form.get('ftpDstUser'),
		"pass": request.form.get('ftpDstPass'),
		"remoteFile": request.form.get('dstRemoteFile')
	}

	try:
		result = transfer_file(ftpSrc, ftpDst)
		return jsonify({"message": "Transfer executed successfully", "result" : result})
	except subprocess.CalledProcessError as e:
		return jsonify({"error": "Transfer failed", "details": str(e)})

@ftp_blueprint.route('/download', methods=['POST'])
def download_ftp_file():
	# Validate and process parameters
	ftpHost = request.form.get('ftpHost')
	ftpUser = request.form.get('ftpUser')
	ftpPass = request.form.get('ftpPass')
	remoteFile = request.form.get('remoteFile')

	try:
		result = download_file(ftpHost, ftpUser, ftpPass, remoteFile, '')
		return jsonify({"message": "File download successfully", "result" : result})
	except subprocess.CalledProcessError as e:
		return jsonify({"error": "Download failed", "details": str(e)})

@ftp_blueprint.route('/upload', methods=['POST'])
def upload_ftp_file():
	# ftp data from the common server
	ftp = {
		"host": request.form.get('ftpHost'),
		"user": request.form.get('ftpUser'),
		"pass": request.form.get('ftpPass')
	}

	if 'localFile' not in request.files:
		return jsonify({'error': 'No file'})
	
	file = request.files['localFile']

	if file.filename == '':
		return jsonify({'error': 'No selected file'})

	try:
		result = upload_file(ftp['host'], ftp['user'], ftp['pass'], file)
		return jsonify({"message": "File uploaded successfully", "result" : result})
	except subprocess.CalledProcessError as e:
		return jsonify({"error": "Upload failed", "details": str(e)})