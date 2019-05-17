from flask import Flask, jsonify, abort

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


if __name__ == '__main__':
    app.run(debug=True)
