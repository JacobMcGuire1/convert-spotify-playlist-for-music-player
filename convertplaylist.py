from requests_html import HTMLSession
import base64

session = HTMLSession()
client_id = "a8ff171bc7ce4489bba3203ed2c61210"
client_secret = "13648f46871d4e1ea186f54c401e5b3a"

headers = {"Authorization" : base64.b64encode(bytes("Basic " + client_id + ":" + client_secret))}
payload = {"grant_type" : "client_credentials"}

r = session.post("https://accounts.spotify.com/api/token", headers=headers, data=payload)

print(r.text)

with open('workfile.html', 'w') as f:
    f.write(r.text)

