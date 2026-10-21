import urllib.request
import urllib.parse
query = "smart cities approaches"
encoded = urllib.parse.quote(query)
url = f"https://api.openalex.org/works?search={encoded}&per-page=5"
print(url)
try:
    with urllib.request.urlopen(url) as response:
        print(response.read().decode('utf-8')[:100])
except Exception as e:
    print(e)
