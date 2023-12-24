from flask import Flask, render_template, request, redirect
from datetime import datetime
from uuid import uuid4
import json

app = Flask(__name__)

def load():
    try:
        with open('data.json') as f:
            return json.load(f)
    except:
        return []

def save(tasks):
    with open('data.json', 'w') as f:
        json.dump(tasks, f, indent=4)

@app.get('/')
def home():
    COLORS = 'red orange yellow blue'.split()
    tasks = load()
    for task in tasks:
        task['color'] = COLORS[int(task['priority'])]
    data = dict(
        date=datetime.now().date().isoformat(),
        tasks=tasks,
    )
    return render_template('home.html', data=data)

@app.post('/')
def new_task():
    task = dict(
        text=request.form['text'],
        priority=request.form['priority'],
        state='pending',
        id=str(uuid4()).replace('-', ''),
    )
    tasks = load() + [task]
    save(tasks)
    return redirect('/')

@app.get('/mark/<state>/<id>/')
def mark(state, id):
    tasks = load()
    selected_task = None
    for task in tasks:
        if task['id'] == id:
            selected_task = task
    if selected_task:
        x = tasks.index(selected_task)
        selected_task.update(state=state)
        tasks[x] = selected_task
        save(tasks)
    return redirect('/')

app.run(debug=True)