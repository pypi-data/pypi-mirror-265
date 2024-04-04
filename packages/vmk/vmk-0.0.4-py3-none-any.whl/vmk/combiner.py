import os
import PyPDF2


class Combiner:
    writer: PyPDF2.PdfWriter
    files: list[str]

    def __init__(self) -> None:
        self.writer = PyPDF2.PdfWriter()
        self.files = []
    
    def open_folder(self, folder: str):
        for dirpath, _, filenames in os.walk(folder):
            for file in filenames:
                file_full_path = os.path.abspath(os.path.join(dirpath, file))
                self.add_file(file_full_path)

        self.files.sort(key=str.lower)

    def write_pdf(self, out: str):
        if os.path.exists(out):
            os.remove(out)

        self.writer.write(out)

    def assemble(self):
        for file_paths in self.files:
            pdf_file = open(file_paths, 'rb')
            reader = PyPDF2.PdfReader(pdf_file)

            pageObj = reader.pages[0]
            self.writer.add_page(pageObj)

    def add_file(self, path: str) -> None:
        if not path.lower().endswith(".pdf"):
            print('Warning: attempted to add non-PDF file', path, '- skipping')
            return
        
        self.files.append(path)
    
    def combine_pdfs_in_folder(self, folder: str, out: str):
        self.open_folder(folder)
        self.assemble()
        self.write_pdf(out)
