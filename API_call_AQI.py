import requests

if __name__ == '__main__':
    userToken = "432b190616bb37f141bd0e2613086ece65ea8a78"
    request = requests.get("https://api.waqi.info/feed/paris/?token=432b190616bb37f141bd0e2613086ece65ea8a78")
    data = request.json()