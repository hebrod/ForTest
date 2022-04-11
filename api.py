from flask import request
from Config import app
from Logic.Base import *
import json

@app.route('/api/v1/event', methods=['POST'])
def postEvents():
    data = json.loads(request.data)
    return loadEvents(data)

@app.route('/api/v1/events_by_region', methods=['GET'])
def get():
    data = json.loads(request.data)
    return getDataEventsByRegion(data)

if __name__ == '__main__':
  app.run(debug=True)