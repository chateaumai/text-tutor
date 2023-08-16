import fitz
from typing import Dict


def get_bookmarks(filepath: str) -> Dict[str, int]:
    # WARNING! One page can have multiple bookmarks!
    bookmarks = {}
    with fitz.open(filepath) as doc:
        toc = doc.get_toc()  # [[lvl, title, page, …], …]
        for level, title, page in toc:
            bookmarks[title] = page
    return bookmarks

def crop(file_name):
    path = "/Users/aaronmai/Desktop/TextTutor/text_tutor/backend/uploads/" + file_name
    doc = fitz.open(path)

    for i in range(len(doc)):

        if i < 9:
            continue

        page = doc[i]
        cropbox = page.rect
        cropbox.y1 -= 20
        page.set_cropbox(cropbox)
    # Save the modified PDF
    doc.saveIncr()
    return path

    #chapters = table_of_contents.keys()
    #chapter_list = list(chapters)
    #print(chapter_list) //jsut a list of the chapters
    #print(table_of_contents['1.1 Populations, Samples, and Processes']) # returns 21, starts at 21
    #print(table_of_contents) # prints chapter names, and starting page number
