from docx import Document
from docx.shared import Pt

def add(new):
    document = Document('./dictionary/Dictionary.docx')

    core_properties = document.core_properties
    core_properties.author = "Dictionary"

    last_modified_by = document.core_properties
    last_modified_by.last_modified_by = "Dictionary"
    
    a = []
    for i in document.paragraphs:
        if i != '':
            a.append(i.text)
    a.append(new)
    a.sort()

    for k in document.paragraphs:
        delete_paragraph(k)
    
    for j in a:
        par = document.add_paragraph()
        run = par.add_run(j)
        font = run.font
        font.size = Pt(18)

    document.save('./dictionary/Dictionary.docx')

def remove_i_paragraph(paragraph):
    document = Document('./dictionary/Dictionary.docx')

    core_properties = document.core_properties
    core_properties.author = "Dictionary"

    last_modified_by = document.core_properties
    last_modified_by.last_modified_by = "Dictionary"

    for i in document.paragraphs:
        if i.text == paragraph:
            delete_paragraph(i)
            break

    document.save('./dictionary/Dictionary.docx')

def delete_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)
    p._p = p._element = None

def get_words():
    document = Document('./dictionary/Dictionary.docx')

    a = []
    for i in document.paragraphs:
        if i != '':
            a.append(i.text)
    return a