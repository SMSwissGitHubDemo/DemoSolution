# DemoSolution

This repository contains the sample code and slides describing the soluton to the customer problem - how to ensure static security testing of code updates.
GitHub's advanced security features provide the checks the customer wants (vulnerability, secrets), and can be configured to run on pushes (commits)

This solution is based on the example in https://geekyhumans.com/receive-github-webhooks-in-python/ but is heavily edited to correct errors and add the response to Repository Created events. 

This solution uses 
 - python (easy for customers to read, and fast to update and test), 
 - Flask, an environment to quickly set up http localhost servers, and 
  - ngrok, to externalize localhost to the internet  

Setup: 
(Set up basic python environment using yum, and flask using home-brew)
Add installs for these packages:
For processing POST JSON packages:
pip install PyGithub    for  Github requests
pip install prettytable. In case we want to output in human friendly way 
pip install requests    for http requests that are to covered by PyGithub (including the patch repo request to ad advanced security) 

Set up ngrok as per the ngrok.org website, and sign up for ngrok (free!). You will get an auth token at that point - save it for later in the setup.  
with a few errata: 
 - python virtual environment does not set up easily, and I found that I could ignore that for this simple demo. 
 - ngrok setup had a few hiccups getting the .zip file to the target server, but I could work around them by downloading to my laptop, then using scp to     the target server. To add the ngrok auth token to the config file, use the command:
  - ngrok authtoken {token from ngrok website when you registered) For Linux, I used a slightly different command than the ngrok website: 
     ngrok authtoken {token from ngrok website}   

Clone this repository, and update the webhooks_test.py file to use your own organization, GithHub auth token and ngrok auth token. 

Start server with python3 command, then put it in the background (append & or hit ctrl-z then bg)
	python3 webhooks_test.py
	(CTRL-Z)
	bg

Test that this is running locally with the curl command:
	curl /localhost:5000.    (Assuming you are using port 5000 in the .py flask file) 

Start ngrok with:  
   ngrok http 5000 for port 5000.  
	(NOTE: Other instructions say use ports like 83, not. good idea. Use upper port range) 

The output from ngrok has the url (ends with .io).  Go to your laptop browser and open a new tab, using this address. You should get similar results as the curl command earlier. 
You now have a working listener! 

Update GitHub web hooks: 
Go to the GitHub console, and under your organization, select Settings. Choose web hooks on the left hand side.  For your web hook, update the url field, using the ngrok url you just set up, with a suffix of ‘/hooktest’ (That’s from the @app.route definition in the python file.)  
Select content type application/json . 
Select which events you would like to use as triggers.  (I used just repository events.) 

Test this out. 
Create a new repo, in the orgqnization your version of .py points to. 
On the window where ngrok is displayed, you will see the POST event. 
In another window, if you run the tail myLogfile command, yu will see logging data reflecting the repository created event. 
Finally, if you go to the Github console for your organization, select Settings, then webhooks, you can find the recent events with headers, payloads, and response from the listener. 

Enjoy trying this out! 
