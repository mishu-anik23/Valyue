from flask import Flask, jsonify, abort
from signalgen import *

app = Flask(__name__)


tasks = [
    {
        'id': 1,
        'title': u'Nibble Encode',
        'subtasks': u'Normal Encode,'
                    u'High Speed Encode,'
                    u'Encoding Shared Nibbles,'
                    u'Encode Frame for single & double signals',
        'byTDD': True,
        'ToDo': False
    },
    {
        'id': 2,
        'title': u'Nibble Decode',
        'subtasks': u'Normal Decode,'
                    u'Decoding Shared Nibbles,'
                    u'Add MSN & LSN in func param',
        'byTDD': True,
        'ToDo': False
    },
]


@app.route('/finished/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/finished/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.route('/gentest', methods=['GET'])
def gentest():
    sg = signal_generator(min=1, step=0.5, max=10)
    return jsonify({'genlist': list(sg)})
#app.add_url_rule('/', 'gentest', gentest)



if __name__ == '__main__':
    app.run(debug=True)
