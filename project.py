from flask import Flask
from flask import request
from flask import render_template
from flask import current_app
from flask import send_from_directory
from alignment import globalalignmentrunner, localalignmentrunner, affinealignmentrunner, affinelogalignmentrunner
from dfa import runWithString
from upgma import runner
from kmp import knuth
from neighborjoining import neighborrunner
import os

UPLOAD_FOLDER = 'tmp'
app = Flask(__name__,static_folder='./static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dfa', methods=['GET', 'POST'])
def dfa():
    error = None
    if request.method == 'POST':
        try:
            seqone = request.form['seqone']
            image, embedder = runWithString(seqone)
            return render_template('dfa.html', error=error, seqone = "", imagen = image, embedder = embedder)
        except Exception as e:
            return render_template('dfa.html', error="An error occurred processing your input."+str(e), seqone = "", imagen = "", embedder = "")
    else:
        return render_template('dfa.html', error=error, seqone = "", imagen = "", embedder = "")

@app.route('/kmp', methods=['GET', 'POST'])
def kmp():
    error = None
    if request.method == 'POST':
        try:
            pattern = request.form['pattern']
            search = request.form['search']
            highlights, lister, failure = knuth(search, pattern)
            return render_template('kmp.html', error=error, search = search, pattern = pattern, highlights = highlights, failure = failure, lister = lister)
        except Exception as e:
            print(e)
            return render_template('kmp.html', error="An error occurred processing your KMP input."+str(e), search = "", pattern = "", highlights = "", failure = "", lister = "")
    else:
        return render_template('kmp.html', error=error, search = "", pattern = "", highlights = "", failure = "", lister = "")

@app.route('/upgma', methods=['GET', 'POST'])
def upgma():
    error = None
    if request.method == 'POST':
        try:
            if not request.files.get('matter', None):
                dister = request.files['dister']
                saveloc = "tmp/"+dister.filename
                dister.save(saveloc)
                secname = dister.filename.split(".")[0]
                output, embedder = runner(saveloc, secname, False)
                return render_template('upgma.html', error=error, imagen = output, embedder = embedder)
            else:
                dister = request.files['matter']
                saveloc = "tmp/"+dister.filename
                dister.save(saveloc)
                secname = dister.filename.split(".")[0]
                output, embedder = runner(saveloc, secname, True)
                return render_template('upgma.html', error=error, imagen = output, embedder = embedder)
        except Exception as e:
            print(e)
            return render_template('upgma.html', error="An error occurred processing your input."+str(e), imagen = "", embedder = "")
    else:
        return render_template('upgma.html', error=error, imagen = "", embedder = "")

@app.route('/neighbor', methods=['GET', 'POST'])
def neighbor():
    error = None
    if request.method == 'POST':
        try:
            if not request.files.get('matter', None):
                dister = request.files['dister']
                saveloc = "tmp/"+dister.filename
                dister.save(saveloc)
                secname = dister.filename.split(".")[0]
                output, embedder = neighborrunner(saveloc, secname, False)
                return render_template('neighbor.html', error=error, imagen = output, embedder = embedder)
            else:
                dister = request.files['matter']
                saveloc = "tmp/"+dister.filename
                dister.save(saveloc)
                secname = dister.filename.split(".")[0]
                output, embedder = neighborrunner(saveloc, secname, True)
                return render_template('neighbor.html', error=error, imagen = output, embedder = embedder)
        except Exception as e:
            print(e)
            return render_template('neighbor.html', error="An error occurred processing your input.  " + str(e), imagen = "", embedder = "")
    else:
        return render_template('neighbor.html', error=error, imagen = "", embedder = "")

@app.route('/tmp/<path:filename>', methods=['GET', 'POST'])
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
            saveloc = "tmp/"+f.filename
            print(saveloc)
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
            return render_template('alignment.html', error="Error processsing your input" + str(e),
                                   seqone = "", seqtwo = "", indel = -1, indelcont = -2, indellog = 2, aligner = "local",
                               optimization = "distance")
    else:
        return render_template('alignment.html', error=error, seqone = "", seqtwo = "", indel = -1, indelcont = -2, indellog = 2, aligner = "local",
                               optimization = "distance")

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
