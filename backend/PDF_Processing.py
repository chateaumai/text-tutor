import fitz
from typing import Dict

#not used
def get_bookmarks(filepath: str) -> Dict[str, int]:
    bookmarks = {}
    with fitz.open(filepath) as doc:
        toc = doc.get_toc()  # [[lvl, title, page, …], …]
        for level, title, page in toc:
            bookmarks[title] = page
    return bookmarks

def crop(file_name):
    path = "/Users/aaronmai/Desktop/TextTutor/text_tutor/backend/uploads/" + file_name
    doc = fitz.open(path)
    doc_metadata = doc.metadata
    title = doc_metadata.get("title")

    for i in range(len(doc)):

        page = doc[i]
        cropbox = page.rect
        cropbox.y1 -= 20
        page.set_cropbox(cropbox)
    # Save the modified PDF
    doc.saveIncr()
    return path, title

    #chapters = table_of_contents.keys()
    #chapter_list = list(chapters)
    #print(chapter_list) //jsut a list of the chapters
    #print(table_of_contents['1.1 Populations, Samples, and Processes']) # returns 21, starts at 21
    #print(table_of_contents) # prints chapter names, and starting page number
