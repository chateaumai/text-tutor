from file_loader import load_file
from processing import process_documents
from query import get_query_result

file_name = "modified.pdf"
data, page_contents, table_of_contents = load_file(file_name)

texts = process_documents(page_contents)

query = "How do I compute a 10% trimmed mean?"

result = get_query_result(texts, query)
print(result)

