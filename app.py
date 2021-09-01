from flask import Flask
from flask_cors import CORS, cross_origin
from flask import jsonify
from flask import request
from flask import abort
from flask_pymongo import PyMongo

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'
mongo = PyMongo(app)


# get all tasks
@app.route('/tasks', methods=['GET'])
def get_all_job():
    job = mongo.db.jobs
    output = []
    for j in job.find():
        if isinstance(j.get('task',), int):
            output.append({'task':j['task'], 'time':j['time']})
    return jsonify({'result' : output})


# get one task
@app.route('/tasks/<number>', methods=['GET'])
def get_one_job(number):
    job = mongo.db.jobs
    j = job.find_one({'task': int(number)})
    if j:
      output = {'task':j['task'], 'time':j['time']}
    else:
      abort(404)
    return jsonify({'result' : output})


# create task
@app.route('/tasks', methods=['POST'])
def add_job():
    job = mongo.db.jobs
    task = int(request.json['task'])
    time = int(request.json['time'])
    if job.find_one({'task': task}):
        abort(400)
    job_id = job.insert({'task':task, 'time':time})
    new_job = job.find_one({'_id': job_id })
    output = {'task': new_job['task'], 'time': new_job['time']}
    return jsonify({'result' : output}), 201


# update task
@app.route('/tasks/<task>', methods=['PUT'])
def update_job(task):
    task_new = int(request.json.get('task',))
    time_new = int(request.json.get('time',))
    job = mongo.db.jobs
    j = job.find_one({'task': int(task)})
    if j:
        query = {'task':j['task'], 'time':j['time']}
        newvalues = { "$set": { "task":task_new, "time":time_new } }
        job.update_one(query, newvalues)
        output = []
        for j in job.find():
            if isinstance(j.get('task',), int):
                output.append({'task':j['task'], 'time':j['time']})
        return jsonify({'result' : output}), 201
    else:
        abort(400)


# delete task
@app.route('/tasks/<task>', methods=['DELETE'])
def delete_job(task):  
    task_new = int(request.json.get('task',))
    time_new = int(request.json.get('time',))
    job = mongo.db.jobs
    j = job.find_one({'task': int(task)})
    if j is None:
        abort(400)
    query = {'task':j['task'], 'time':j['time']}
    job.delete_one(query)
    output = []
    for j in job.find():
        if isinstance(j.get('task',), int):
            output.append({'task':j['task'], 'time':j['time']})
    return jsonify({'result' : output}), 201


# get data for monitor
@app.route('/data/', methods=['GET'])
def get_data():
    job = mongo.db.jobs
    output = []
    for j in job.find(): 
        if isinstance(j.get('task',), int):
            output.append({'task':j['task'], 'time':j['time']})
    sortedlist = sorted(output, key=lambda k: k['task'])
    newlist = [{'task':'task'+str(i['task']), 'time':i['time']} for i in sortedlist]

    del newlist[0]
    return jsonify({'result' : newlist})


# create default (zero) task
job = mongo.db.jobs
j = job.find_one({'task':0, 'time':5})
if j is None:
    job.insert({'task':0, 'time':5})
    print('task 0 created...')
  


if __name__ == '__main__':
    
    app.run(debug=True, host="127.0.0.1", port=5000,)


