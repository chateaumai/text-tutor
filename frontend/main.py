from flask import Flask, request, render_template, redirect, session
import pickle
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ..backend import text_split, handle_upload, query, file_loader, existing_index

'''from backend.processing import process_documents
from backend.handle_upload import get_docsearch
from backend.query import answer'''

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
pdfs = UploadSet('pdfs', DOCUMENTS)

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_PATH = os.path.join(BASE_DIR, 'backend/uploads')
print(UPLOADS_PATH)
app.config['UPLOADED_PDFS_DEST'] = UPLOADS_PATH
configure_uploads(app, pdfs)

#global data, page_contents, table_of_contents, texts

@app.route('/')
def hello_world():
    return '<h1>Hello World</h1>'

docsearch_storage = {}
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'pdf' in request.files:
            filename = pdfs.save(request.files['pdf'])
            print("getting page contents")
            page_contents = file_loader.load_file(filename)
            print("getting docs")
            documents = text_split.process_documents(page_contents)
            session.clear()
            upload_id = uuid.uuid4().hex
            print("getting docsearch")
            #docsearch = handle_upload.get_docsearch(documents, upload_id)
            print("after docsearch")
            docsearch = existing_index.get_docsearch_from_existing()
            docsearch_storage[upload_id] = docsearch
            session['upload_id'] = upload_id
            print("after save")
            '''serialized_docsearch = pickle.dumps(docsearch)
            session['docsearch'] = serialized_docsearch
            session['upload_id'] = upload_id

            ans = answer(query, docsearch)'''

            return redirect('/chat')
        else:
            return 'Failed to upload'
    else:
        return render_template('upload.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
#    docsearch = pickle.load(session['docsearch'])
    if 'history' not in session:
        session['history'] = []

    upload_id = session['upload_id']
    docsearch = docsearch_storage.get(upload_id)

    if request.method == 'POST':
        question = request.form.get('question')
        ans = query.answer(question, docsearch)
    #    print(ans)
        session['history'].append({
            'question': question,
            'answer': ans
        })
        session.modified = True
        return redirect('/chat')
    
    else:
        #ans = session['answer']
        return render_template('chat.html', history=session['history'])

    #POST the answer as query
    #GET the ans
    #loop this


if __name__ == '__main__':
   app.run(port=8000, debug=True)