# pip install pygithub

from github import Github
g = Github("user","password")
user = g.get_user()
repo = user.create_repo("createdWithPython")
