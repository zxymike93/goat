import platform

from selenium import webdriver


if 'Ubuntu' in platform.platform():
    browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
else:
    browser = webdriver.Firefox(executable_path='/Applications/geckodriver')

# 打开网站
browser.get('http://localhost:8000')

# To-Do is browser title
assert 'To-Do' in browser.title

# entry

# entry: "buy something"
# update >> shows "1. buy something"

# entry: "buy more"
# update >> shows "2. buy more"

# check

browser.quit()
