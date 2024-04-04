import PyPDF2, os

def main():
    your_target_folder = "./"

    if os.path.exists("CombinedFirstPages1.pdf"):
        os.remove("CombinedFirstPages1.pdf")
    else:
        pass

    pdf_files = []

    for dirpath, _, filenames in os.walk(your_target_folder):

        _.clear() #remove subpastas e seus arquivos

    #    print(dirpath)
    #    print(_)
    #    for n in filenames:
    #        print(n)

        for items in filenames:

            file_full_path = os.path.abspath(os.path.join(dirpath, items))

            if file_full_path.lower().endswith(".pdf"):
                pdf_files.append(file_full_path)

            else:
                pass

    pdf_files.sort(key=str.lower)
    pdfWriter = PyPDF2.PdfWriter()

    for files_address in pdf_files:
        pdfFileObj = open(files_address, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)

        pageObj = pdfReader.pages[0]
        pdfWriter.add_page(pageObj)

    with open("CombinedFirstPages1.pdf", "wb") as output:
        pdfWriter.write(output)

    print('done1')
