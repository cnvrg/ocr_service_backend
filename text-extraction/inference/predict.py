import os
import PyPDF2

os.environ["USE_TORCH"] = "1"
import torch
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import base64
from operator import itemgetter
import binascii

if torch.cuda.is_available():
    predictor = ocr_predictor(pretrained=True).cuda()
else:
    predictor = ocr_predictor(pretrained=True)


def stitch(page):
    out_txt = ""
    for block in page["blocks"]:
        for line in block["lines"]:
            for word in line["words"]:
                out_txt += word["value"] + " "
    return out_txt


def _process_file(file_path, todo, output):
    if str(file_path).lower().endswith(".pdf"):
        doc = DocumentFile.from_pdf(file_path)
    else:
        doc = DocumentFile.from_images(file_path)
    if len(todo) == 1:
        out = predictor([doc[todo[0]]])
    else:
        out = predictor(list((itemgetter(*todo)(doc))))
    export = out.export()

    for page, pagenumber in zip(export["pages"], todo):
        output[pagenumber] = stitch(page)
    return output


def predict(data):
    print(f"{data=}")
    prediction = {}
    for count, filepdf in enumerate(data["pdf"]):
        print(f"{filepdf=}")
        """ 
        try:
            decoded = base64.b64decode(filepdf)  # decode the input file
            savepath = "file.pdf"
            f = open("file.pdf", "wb")
            f.write(decoded)
            f.close()
            filename = "file.pdf"
            pdfFileObj = open(filename, "rb")
        except binascii.Error:
        """
        filename = filepdf
        pdfFileObj = open(filepdf, "rb")

        # The pdfReader variable is a readable object that will be parsed.
        # pdfReader = PyPDF2.PdfFileReader(pdfFileObj) #PendingDeprecationWarning
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        # Discerning the number of pages will allow us to parse through all the pages.
        # num_pages = pdfReader.numPages   #PendingDeprecationWarning
        num_pages = len(pdfReader.pages)
        count = 0
        output = {}
        # The while loop will read each page.
        while count < num_pages:
            # pageObj = pdfReader.getPage(count)
            # output[count] = pageObj.extractText()
            pageObj = pdfReader.pages[count]
            output[count] = pageObj.extract_text()
            count += 1

        todoocr = []

        for page in output.keys():
            if output[page] == "":
                todoocr.append(page)

        if len(todoocr) != 0:
            print("running ocr for page numbers: ", todoocr)
            print("page index starts at 0")
            output = _process_file(filename, todoocr, output)
        prediction[count] = output

    return prediction
