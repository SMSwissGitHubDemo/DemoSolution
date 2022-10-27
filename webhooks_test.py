from flask import Flask
from flask import request
from flask import json  #importing json cause that’s what we’re going to be working with
from github import Github
import requests
import logging

app = Flask(__name__)

# NOTE: Really bad practice to hardcode access token. Okay for simple demo 
on test repos. 
myGHT = "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"
myAuth = "Bearer " + myGHT
g = Github(myGHT)

logging.basicConfig(filename='myLogfile', level=logging.INFO)

logging.info('Hello from webhook test3')



@app.route('/')
def root():
  return 'Hello World! Testing webhooks.'

@app.route('/hooktest', methods=['POST'])  # ‘/hooktest’ specifies which 
link will it work on 
def hook_root():

  logging.info('Got a request with content type and Event type: %s  %s ', 
request.headers['content-type'], request.headers['X-GitHub-Event'])
  if request.headers['X-GitHub-Event'] == "repository":  # calling json 
objects
#    y = json.loads(request.json())
    logging.info('Action is %s ', request.json["action"])
    if request.json["action"] == "created":
       logging.info('Got a repo create request')
       newrepoid = request.json["repository"]["id"]
       newreponame = request.json["repository"]["name"]
       newurl = request.json["repository"]["owner"]["url"]
       newfullurl = f"{newurl}/{newreponame}" 
       # Now let's add advanced security policy
       datastr = "\"security_and_analysis\": \{\"advanced_security\": \{ 
         \"status\": \"enabled\"  \} \}"
       response = requests.patch(
           newfullurl, 
           headers = {
             'Accept': 'applicationvnd.github+json', 
             'Authorization' : myAuth
           },
           json = {
             'security_and_analysis' : {
                'advanced_security' : {
                  'status' : 'enabled' }
             }
          }
       )
       return 'We received a new repo webhook. Add advanced security 
checking'
#   Common return statement
    return(json.dumps(request.json))
#      TODO: Add error logic
# Default case 
  return json.dumps(request.json)

if __name__ == '__main__':
  app.run(debug=True)
