import requests
import urllib.request
import http.client

def fetch_url():
    resp1 = requests.get("https://example.com")
    resp2 = requests.post("https://example.com/api", data={"foo":"bar"})
    resp3 = urllib.request.urlopen("https://example.com")
    conn = http.client.HTTPConnection("example.com")
    conn.request("GET", "/")
    print(resp1.status, resp2.status)

if __name__ == "__main__":
    fetch_url()
