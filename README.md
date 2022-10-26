# DemoSolution

This repository contains the sample code and slides describing the soluton to the customer problem - how to ensure static security testing of code updates.
GitHub's advanced security features provide the checks the customer wants (vulnerability, secrets), and can be configured to run on pushes (commits)

This solution borrows heavily from Todd Roberts' excellent webhook listener: https://pypi.org/project/Webhook-Listener/

Setup: 
(Set up basic python environment.)

From Todd's README,

pip install Webhook-Listener

Clone this repository, specifically the demoWebHooks.py file

Go to the GitHub repository and update WebHooks to use the URL for this server

To run:
Start the server: 
python3 demoWebHooks.py 

Trigger a repository CREATE event by creating a new (empty) repository via the dashboard

Bonus points: Add a simple Hello World file to the repository and COMMIT, and verify that security testing takes place. 


