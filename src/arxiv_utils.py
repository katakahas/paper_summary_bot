import urllib.request


def load_pdf(url):
    save_path = "paper.pdf"
    url = url.replace("abs", "pdf")
    try:
        pdf = urllib.request.urlopen(url).read()
        with open(save_path, "wb") as out:
            out.write(pdf)
    except urllib.error.HTTPError as err:
        print(err.code)
    except urllib.error.URLError as err:
        print(err.reason)
    return save_path
