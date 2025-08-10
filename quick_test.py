import urllib.request

url = "http://hackme1.vulnmachines.com/idor/"
try:
    response = urllib.request.urlopen(url, timeout=10)
    content = response.read()
    print(f"Status: {response.status}")
    print(f"Size: {len(content)}")
    if len(content) != 10918:
        print("Not default Apache!")
        print(content[:500])
except Exception as e:
    print(f"Error: {e}")