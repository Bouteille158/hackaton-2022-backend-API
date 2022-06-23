from saagieapi import SaagieApi
from flask import Flask, send_file
import json
from jsonmerge import Merger

app = Flask(__name__)

schema = {
    "properties": {
        "bar": {
            "mergeStrategy": "append"
        }
    }
}
merger = Merger(schema)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

saagie = SaagieApi.easy_connect(url_saagie_platform="https://demo-workspace.a4.saagie.io/projects/platform/2/",
                   user="ESTIAM_G17_amine.abbes",
                   password="Saagie.Hakathon")

@app.route("/projectList")
def getProjects():
    projects = saagie.projects.list()
    print(projects)
    return projects

@app.route("/project/<projectId>")
def getProjectInfo(projectId):
    print(projectId)
    projectInfo = saagie.projects.get_info(projectId)
    print(projectInfo)
    return projectInfo

@app.route("/project/<projectId>/jobs")
def getProjectJobs(projectId):
    print(projectId)
    projectJobs = saagie.jobs.list_for_project(project_id=projectId)
    print(projectJobs)
    return projectJobs

@app.route("/project/<projectId>/getBackup/")
def getJobsBackup(projectId):
    project = getProjectInfo(projectId)
    jobs = getProjectJobs(projectId)
    data = merger.merge(project, jobs)
    print(data)
    with open('backup.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return send_file('backup.json', as_attachment=True)

'''
@app.route("/project/<projectId>/createJob")
def createJob(projectId):
    res = saagie.jobs.create(job_name="my job",
                   project_id="projectId",
                   file="/tmp/test.py",
                   description='My description',
                   category='Extraction',
                   technology='python',
                   technology_catalog='Saagie',
                   runtime_version='3.9',
                   command_line='python {file}',
                   release_note='First release',
                   extra_technology='',
                   extra_technology_version='',
                   cron_scheduling='0 0 * * *',
                   schedule_timezone='Europe/Paris',
                   resources={"cpu": {"request": 0.5, "limit": 2.6}, "memory": {"request": 1.0}},
                   emails=['email1@saagie.io', 'email2@saagie.io'],
                   status_list=["FAILED", "KILLED"]
                   )
    return res
'''

'''
# Create a project named 'Project_test' on the saagie platform
project_dict = saagie.projects.create(name="Project_test",
                                     group="<saagie-group-with-proper-permissions>",
                                     role='Manager',
                                     description='A test project')

# Save the project id
project_id = project_dict['createProject']['id']

# Create a python job named 'Python test job' inside this project
job_dict = saagie.jobs.create(job_name="Python test job",
                              project_id=project_id,
                              file='<path-to-local-file>',
                              description='Amazing python job',
                              category='Processing',
                              technology_catalog='Saagie',
                              technology='python',
                              runtime_version='3.8',
                              command_line='python {file} arg1 arg2',
                              release_note='',
                              extra_technology='')

# Save the job id
job_id = job_dict['data']['createJob']['id']

# Run the python job and wait for its completion
saagie.jobs.run_with_callback(job_id=job_id, freq=10, timeout=-1)
'''

if __name__ == "__main__":
    app.run(debug=True)