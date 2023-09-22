from flask import Flask, request, render_template, redirect, session, jsonify
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS
import os
from dotenv import load_dotenv
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ..backend import text_split, handle_upload, file_loader, existing_index, agent

load_dotenv()
FLASK_KEY = os.environ.get('FLASK_KEY')

app = Flask(__name__, static_folder='static')
app.secret_key = FLASK_KEY
pdfs = UploadSet('pdfs', DOCUMENTS)

#to get the correct path to store a textbook
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_PATH = os.path.join(BASE_DIR, 'backend/uploads')
app.config['UPLOADED_PDFS_DEST'] = UPLOADS_PATH
configure_uploads(app, pdfs)

#feels like a better way to do this
docsearch_storage = {}
retriever_storage = {}
doc_storage = {}

@app.route('/')
def hello_world():
    return redirect('/upload')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'pdf' in request.files:
            filename = pdfs.save(request.files['pdf'])
            
            #getting texts
            page_contents, title = file_loader.load_file(filename)
            documents = text_split.process_documents(page_contents)
            #docsearch = handle_upload.get_docsearch(documents, upload_id)

            #storing texts in database
            retriever = handle_upload.hybrid_search(documents)
            docsearch = existing_index.get_docsearch_from_existing()

            session.clear()
            upload_id = uuid.uuid4().hex

            session['upload_id'] = upload_id
            doc_storage[upload_id] = documents
            docsearch_storage[upload_id] = docsearch
            retriever_storage[upload_id] = retriever

            session['title'] = title

            return redirect('/chat')
        else:
            return 'Failed to upload'
    else:
        return render_template('upload.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'history' not in session:
        session['history'] = []

    upload_id = session['upload_id']
    docsearch = docsearch_storage.get(upload_id)
    retriever = retriever_storage.get(upload_id)
    title = session.get('title', 'Text Tutor')


    if request.method == 'POST':
        question = request.form.get('question')
        ans = agent.decide_retriever(question, docsearch, retriever)
        session['history'].append({
            'question': question,
            'answer': ans
        })
        session.modified = True
        return jsonify({'answer': ans})
    
    else:
        return render_template('chat.html', history=session['history'], title=title)



if __name__ == '__main__':
    extra_dirs = ['templates/', 'static/']
    app.run(port=8000, debug=True, extra_files=extra_dirs)

