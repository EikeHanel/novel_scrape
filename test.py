from bs4 import BeautifulSoup

test = "<p><strong>hello</strong></p>"

soup = BeautifulSoup(test, 'html.parser')
soup.extend(soup.find_all(string=True, recursive=True))
print(str(soup))
print(test)