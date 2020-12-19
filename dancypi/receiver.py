from flask import Flask
from flask import request
app = Flask(__name__)
procs = []

@app.route('/scroll')
def scroll():
    stop(procs)
    proc = Popen([r"visualization", "scroll"], stdout=PIPE, stderr=STDOUT
                                )
    procs.append(proc)

@app.route('/spetrum')
def visualization():
    stop(procs)
    proc = Popen([r"visualization", "spectrum"], stdout=PIPE, stderr=STDOUT
                                )
    procs.append(proc)

@app.route('/energy')
def energy():
    stop(procs)
    proc = Popen([r"visualization", "energy"], stdout=PIPE, stderr=STDOUT
                                )
    procs.append(proc)


def stop(procs):
    for i in procs:
        i.kill() 
    