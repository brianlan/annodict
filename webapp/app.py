import os
import json

import requests
from flask import render_template, request, make_response
from eve import Eve

# from job_management import enqueue

app = Eve(root_path=os.path.dirname(os.path.realpath(__file__)))


@app.route("/all_annoclasses", methods=["GET"])
def all_annoclasses():
    return render_template('all_annoclasses.html')


@app.route("/all_categories", methods=["GET"])
def all_categories():
    return render_template('all_categories.html')


@app.route("/demo_toggle", methods=["GET"])
def demo_toggle():
    return render_template('demo_toggle.html')

@app.route("/demo_toggle2", methods=["GET"])
def demo_toggle2():
    return render_template('demo_toggle2.html')


@app.route("/create_job", methods=["GET"])
def create_job():
    return render_template('job_detail.html')


# @app.route("/enqueue_job", methods=["POST"])
# def enqueue_job():
#     job = request.get_data()
#     if job is None:
#         return make_response("No data was post to /enqueue_job", 400)
#     enqueue(json.loads(job.decode("utf-8")))
#     return make_response(f"Successfully enqueued job: {job}", 200)


@app.route("/task_status", methods=["POST"])
def task_status():
    """this endpoint receives status info that post from different tasks."""
    data = request.get_data()
    print(data)
    data = json.loads(data.decode("utf-8"))
    headers = {"Content-Type": "application/json"}
    resp = requests.get(f"http://127.0.0.1:5000/job/{data['job_id']}", headers=headers)
    job = resp.json()
    for task in job["tasks"]:
        if task['id'] == data['task_id']:
            task['labnew_task_ids'] = data['message']['labnew_task_ids']
            task['status'] = data['status']
            break
    requests.patch(f"http://127.0.0.1:5000/job/{data['job_id']}", json={"tasks": job["tasks"]}, headers=headers)
    return make_response(f"OK", 200)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
