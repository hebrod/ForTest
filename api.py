from flask import request
from Config import app
from Logic.Base import *
import json

@app.route('/api/v1/event', methods=['POST'])
def postEvent():
    data = json.loads(request.data)
    return loadEvent(data)

if __name__ == '__main__':
  app.run(debug=True)