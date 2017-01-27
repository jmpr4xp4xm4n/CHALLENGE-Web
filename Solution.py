#!/usr/bin/env python

import base64
import re
import httplib
import webbrowser

def httpRequest(token = None):
    conn = httplib.HTTPConnection("www.dnegel-serv.com")
    request_string = "/challenges/1/"
    method = "HEAD"
    if token is not None:
        method = "GET"
        request_string += "?token=%s" % (token)
    conn.request(method, request_string)
    return conn.getresponse()

resp = httpRequest()
location = resp.getheader("location")
match = re.search(".*?token=(?P<token>[A-Za-z0-9+/=]+)", location)
token = match.group("token")
decoded_token = base64.b64decode(token)
inject = "user=admin|a=b"
original = "user=anonymous"
org_len = len(original)

res = ""
for i in range(0, len(decoded_token), 1):
    if i < org_len:
        res += chr(ord(decoded_token[i]) ^ ord(original[i]) ^ ord(inject[i]))
    else:
        res += decoded_token[i]

admin_token = base64.b64encode(res)
webbrowser.open("http://www.dnegel-serv.com/challenges/1/?token=%s" % (admin_token))
