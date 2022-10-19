from flask import Flask
  

app = Flask(__name__)
  

@app.route('/', methods = ['GET'])
def get_file():
    return {'data': 'get'}
  

@app.route('/', methods = ['POST'])
def upload_file():
    return {'data': 'post'}


@app.route('/', methods = ['DELETE'])
def delete_file():
    return {'data': 'DELETE'}
  
  
if __name__ == '__main__':
    app.run(debug = True)
