from langchain.document_loaders import PyMuPDFLoader
import PDF_Processing

def load_file(file_name):

    loader = PyMuPDFLoader(file_name)
    data = loader.load()

    page_contents = [doc.page_content for doc in data]
    table_of_contents = PDF_Processing.get_bookmarks("modified.pdf")
    return data, page_contents, table_of_contents