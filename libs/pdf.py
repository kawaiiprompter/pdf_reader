import pdfminer
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

def read_pdf_using_lib(filepath):
    resource_manager = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(resource_manager, laparams=laparams)
    interpreter = PDFPageInterpreter(resource_manager, device)

    pdf_path = filepath
    papers = {}
    with open(pdf_path, 'rb') as file:
        for i_page, page in enumerate(PDFPage.get_pages(file)):
            _, _, p_width, p_height = page.mediabox
            interpreter.process_page(page)
            layout = device.get_result()
            for element in layout:
                if isinstance(element, pdfminer.layout.LTTextBoxHorizontal):
                    if i_page not in papers:
                        papers[i_page] = []
                    papers[i_page].append({
                        "type": "text",
                        "page": i_page,
                        "text": element.get_text(),
                        "bbox": element.bbox,
                        "width": element.width
                    })
                    pass
                elif isinstance(element, pdfminer.layout.LTFigure):
                    papers[i_page].append({
                        "type": "figure",
                        "page": i_page,
                        "bbox": element.bbox,
                        "width": element.width
                    })
                    pass
                elif isinstance(element, pdfminer.layout.LTLine):
                    pass
                elif isinstance(element, pdfminer.layout.LTCurve):
                    pass
                else:
                    print(element.__class__)
                    
    return papers, [p_width, p_height]


def read_pdf(filepath):
    papers, [p_width, p_height] = read_pdf_using_lib(filepath)
    # 順番
    sentence = []
    for i_page in papers.keys():
        for p in papers[i_page]:
            if p["type"] == "text":
                x0, y0, x1, y1 = p["bbox"]
                mask1 = p["width"] > int((p_height // 2) * 0.5)
                mask2 = len(p["text"]) > 50
                mask = mask1 and mask2
                if mask:
                    text = p["text"].replace("-\n","").replace("\n", " ")
                    sentence.append(text)
    return sentence
