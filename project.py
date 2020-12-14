from flask import Flask
from flask import request
from flask import render_template
from flask import current_app
from flask import send_from_directory
from alignment import globalalignmentrunner, localalignmentrunner, affinealignmentrunner, affinelogalignmentrunner
from dfa import runWithString
import os

UPLOAD_FOLDER = 'uploads'
app = Flask(__name__,static_folder='./static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dfa', methods=['GET', 'POST'])
def dfa():
    error = None
    if request.method == 'POST':
        seqone = request.form['seqone']
        image = runWithString(seqone)
        return render_template('dfa.html', error=error, seqone = "", imagen = image)
    else:
        return render_template('dfa.html', error=error, seqone = "", imagen = "")

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

@app.route('/alignment', methods=['GET', 'POST'])
def align():
    error = None
    seqtwo = ""
    if request.method == 'POST':
        try:
            f = request.files['scoring']
            saveloc = "uploads/"+f.filename
            f.save(saveloc)
            seqx, seqy, score = "", "", 0

            seqone = request.form['seqone']
            seqtwo = request.form['seqtwo']
            indel = request.form['indel']
            aligner = request.form['aligner']
            indelcont = request.form['indelcont']
            indellog = request.form['indellog']
            optimization = request.form['optimization']
            
            if request.form['aligner'] == "local":
                seqx, seqy, score = localalignmentrunner(request.form['seqone'], request.form['seqtwo'], saveloc,
                                                      float(request.form['indel']))
            elif request.form['aligner'] == "global":
                seqx, seqy, score = globalalignmentrunner(request.form['seqone'], request.form['seqtwo'], saveloc,
                                                      float(request.form['indel']), request.form['optimization'])

            elif request.form['aligner'] == "affine":
                seqx, seqy, score = affinealignmentrunner(request.form['seqone'], request.form['seqtwo'], saveloc,
                                                      float(request.form['indel']), float(request.form['indelcont']),request.form['optimization'])

            elif request.form['aligner'] == "affinelog":
                seqx, seqy, score = affinelogalignmentrunner(request.form['seqone'], request.form['seqtwo'], saveloc,
                                                      float(request.form['indel']), float(request.form['indellog']), request.form['optimization'])

            return render_template('alignment.html', error=error, seqx = seqx, seqy = seqy, score = score,
                                   seqone = seqone, seqtwo = seqtwo, indel = indel, indelcont = indelcont, indellog = indellog, aligner = aligner, optimization = optimization)
        except KeyError as e:
            print(e)
            return render_template('alignment.html', error="Key Error: One of the letters in a sequence string does not appear in the matrix",
                                   seqone = seqone, seqtwo = seqtwo, indel = indel, indelcont = indelcont, indellog = indellog, aligner = aligner, optimization = optimization)
        except Exception as e:
            print(e)
            return render_template('alignment.html', error="Error processsing your input",
                                   seqone = seqone, seqtwo = seqtwo, indel = indel, indelcont = indelcont, indellog = indellog, aligner = aligner, optimization = optimization)
    else:
        return render_template('alignment.html', error=error, seqone = "", seqtwo = "", indel = -1, indelcont = -2, indellog = 2, aligner = "local",
                               optimization = "distance")

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
