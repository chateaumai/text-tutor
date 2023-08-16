from langchain.document_loaders import PyMuPDFLoader
from .PDF_Processing import crop

#get raw, crop, 
def load_file(file_name):
    path = crop(file_name)
    loader = PyMuPDFLoader(path)
    data = loader.load()

    page_contents = [doc.page_content for doc in data]
#    table_of_contents = get_bookmarks("modified.pdf")
#    return data, page_contents, table_of_contents
    return page_contents