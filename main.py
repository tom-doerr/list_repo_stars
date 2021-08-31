#!/usr/bin/env python3

'''
List the repositories and the stars for each repository of a certain GithHub profile.
Does not require a login.
Show the repositories with the most stars in order.
'''

import requests
import sys

if len(sys.argv) < 2:
    print("Usage: {} <github-profile>".format(sys.argv[0]))
    sys.exit(1)

r = requests.get("https://api.github.com/users/{}/repos".format(sys.argv[1]))
# Make multiple requests to get all repositories.
# API limit: https://developer.github.com/v3/#rate-limiting
l = []
while "next" in r.links:
    l.append(r)
    r = requests.get(r.links["next"]["url"])

l.append(r)

if r.status_code != 200:
    print("Error: {}".format(r.json()))
    sys.exit(2)

json_list = [e.json() for e in l]

# Combine all elements in json to one element.
repos = sum(json_list, [])

for repo in sorted(repos, key=lambda x: x['stargazers_count'], reverse=True):
    print("{} - {} stars".format(repo['name'], repo['stargazers_count']))


