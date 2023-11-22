from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

password = 'sparta'
cxn_str = f'mongodb+srv://test:{password}@cluster0.nrbqjbm.mongodb.net/'
client = MongoClient(cxn_str)

db = client.dbsparta_sertification
tasks_collection = db.tasks

@app.route('/')
def index():
    tasks = tasks_collection.find()  # Use find on the collection
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    if request.method == 'POST':
        task_title = request.form['title']
        tasks_collection.insert_one({'title': task_title})
    return redirect(url_for('index'))

@app.route('/delete/<task_id>')
def delete_task(task_id):
    print(f"Deleting task with ID: {task_id}")
    tasks_collection.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
