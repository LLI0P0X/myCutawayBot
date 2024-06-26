from PyPDF2 import PdfReader, PdfWriter
import config


def mix2PdfTo1(pdf1Name, pdf2Name, nPage):
    pdfR1 = PdfReader(open(pdf1Name, "rb"))
    pdfR2 = PdfReader(open(pdf2Name, "rb"))

    # if nPage < len(pdfR2.pages):
    #     raise f'ошибка длины файла {pdf2Name}'
    pdfW1 = PdfWriter()

    for page in pdfR1.pages[:5]:
        pdfW1.add_page(page)

    for page in pdfR2.pages[nPage:]:
        pdfW1.add_page(page)

    out = pdf2Name.split('\\')[-1]
    pdfW1.write(open(f"{config.path}\\out\\{out}", "wb"))


if __name__ == "__main__":
    mix2PdfTo1('..\\secrets\\Леткин.pdf', '..\\temp\\Леткин.pdf', 5)
