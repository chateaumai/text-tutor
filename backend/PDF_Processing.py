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

doc = fitz.open("text-tutor/Probability_and_Statistics_for_Engineering_and_the_Sciences.pdf")

# Loop over the pages you want to modify
for i in range(len(doc)):
    # Skip pages 1-9
    if i < 9:
        continue

    page = doc[i]
    # Get the page cropbox
    cropbox = page.rect
    # Reduce the height of the cropbox by 20 units
    cropbox.y1 -= 20
    # Set the new cropbox
    page.set_cropbox(cropbox)
# Save the modified PDF
doc.save("modified.pdf")

#chapters = table_of_contents.keys()
#chapter_list = list(chapters)
#print(chapter_list) //jsut a list of the chapters
#print(table_of_contents['1.1 Populations, Samples, and Processes']) # returns 21, starts at 21
#print(table_of_contents) # prints chapter names, and starting page number
