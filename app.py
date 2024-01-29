import sys
# sys.path.append("/home/api-pyrepasat/www/repasat_api_py")
from flask import Flask
from router.ftp_controller import ftp_blueprint

app = Flask(__name__)
app.register_blueprint(ftp_blueprint)

@app.route('/')
def index():
    return '<h1>Hello world</h1>'

# default local: http://127.0.0.1:5000/
# else: app.run(host='0.0.0.0', port=8080, debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# application = app

# if __name__ == '__main__':
#     app.run(debug=True)
    # app.run()