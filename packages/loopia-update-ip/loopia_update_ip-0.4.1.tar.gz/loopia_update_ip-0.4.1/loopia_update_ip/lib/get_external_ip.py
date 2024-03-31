import urllib.request


def get_external_ip() -> str:
    try:
        # Using http://icanhazip.com to get external ip
        return urllib.request.urlopen('http://icanhazip.com').read().decode().strip("\n")
    except:
        print("ERROR: External IP could not be retrieved, check connection.")
        return ''
