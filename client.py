import requests

# get available boards
r = requests.get("http://localhost:5000")
print(r.json())

BOARDID = ""
# get quick methods for BOARDID
r = requests.get(f"http://localhost:5000/{BOARDID}/quick")

# call quick method
r = requests.put(f"http://localhost:5000/{BOARDID}/quick/bootToEDL")
print(r.status_code)
print(r.json())
