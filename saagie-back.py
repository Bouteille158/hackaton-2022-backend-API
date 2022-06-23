from saagieapi import SaagieApi
from flask import Flask, send_file
from flask_cors import CORS, cross_origin
import json
from jsonmerge import Merger

app = Flask(__name__)
CORS(app)
merger = Merger({})

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

saagie = SaagieApi.easy_connect(url_saagie_platform="https://demo-workspace.a4.saagie.io/projects/platform/2/",
                   user="ESTIAM_G17_amine.abbes",
                   password="Saagie.Hakathon")

@app.route("/projectList")
def getProjects():
    projects = saagie.projects.list()
    #print(projects)
    return projects

@app.route("/project/<projectId>")
def getProjectInfo(projectId):
    #print(projectId)
    projectInfo = saagie.projects.get_info(projectId)
    #print(projectInfo)
    return projectInfo

@app.route("/project/<projectId>/jobs")
def getProjectJobs(projectId):
    #print(projectId)
    projectJobs = saagie.jobs.list_for_project(project_id=projectId)
    #print(projectJobs)
    return projectJobs

@app.route("/project/<projectId>/getBackup")
def getJobsBackup(projectId):
    project = getProjectInfo(projectId)
    jobs = getProjectJobs(projectId)
    data = merger.merge(project, jobs)
    #print(data)
    with open('backup.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return send_file('backup.json', as_attachment=True)

@app.route("/project/restore")
def restoreProject():
    print("")

if __name__ == "__main__":
    app.run(debug=True)