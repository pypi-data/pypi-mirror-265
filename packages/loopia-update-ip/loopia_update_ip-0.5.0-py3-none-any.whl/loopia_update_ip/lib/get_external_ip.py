import urllib.request


def get_external_ip() -> str:
    try:
        # Using http://icanhazip.com to get external ip
        return urllib.request.urlopen('http://icanhazip.com').read().decode().strip("\n")
    except Exception as e:
        print(f"ERROR: External IP could not be retrieved, check connection. \n Error message: {e}")
        return ''
