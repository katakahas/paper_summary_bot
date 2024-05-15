import os
from uuid import uuid4

import requests


def load_pdf(url: str) -> str:
    if not os.path.exists("pdfs/"):
        os.makedirs("pdfs/")
    save_path = f"pdfs/{str(uuid4())}.pdf"
    url = url.replace("abs", "pdf")
    try:
        response = requests.get(url=url)
        assert response.status_code == 200, "Failed to retrieve PDF file."
        pdf_bytes = response.content
        with open(save_path, "wb") as f:
            f.write(pdf_bytes)
        print("PDF file saved.")
    except BaseException as e:
        print(f"{e.__class__.__name__}: {e}")
    return save_path
