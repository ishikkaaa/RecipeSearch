from urllib.parse import unquote
enc='hello%20world%20'
dec=unquote(enc)
print(dec)