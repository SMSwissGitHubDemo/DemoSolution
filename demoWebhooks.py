#!/usr/bin/env python
"""Webhook Listener Example for Adding Security testing to new repository

Author: Steve Swiss, using the core code from Todd Roberts

https://github.com/toddrob99/Webhooks
"""
import sys
import os
import logging
import logging.handlers
import time

import webhook_listener

import argparse

parser = argparse.ArgumentParser(
    prog="Webhook Listener", description="Start the webhook listener."
)
parser.add_argument(
    "--verbose", "-v", action="store_true", dest="verbose", help="Enable debug logging."
)
parser.add_argument(
    "--port",
    "-p",
    type=int,
    nargs=1,
    dest="port",
    help="Port for the web server to listen on (default: 8090).",
)
args = parser.parse_args()
port = args.port[0] if args.port and args.port[0] >= 0 else 8090

rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

logger = logging.getLogger("webhooks")

console = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s :: %(levelname)8s :: %(module)s(%(lineno)d) :: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S %p",
)
console.setFormatter(formatter)
logger.addHandler(console)

logPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logs")
if not os.path.exists(logPath):
    os.makedirs(logPath)

file = logging.handlers.TimedRotatingFileHandler(
    os.path.join(logPath, "webhooks.log"), when="midnight", interval=1, backupCount=7
)
file.setFormatter(formatter)
logger.addHandler(file)
logger.debug("Logging started!")


def parse_request(request, *args, **kwargs):
    logger.debug(
        "Received request:\n"
        + "Method: {}\n".format(request.method)
        + "Headers: {}\n".format(request.headers)
        + "Args (url path): {}\n".format(args)
        + "Keyword Args (url parameters): {}\n".format(kwargs)
        + "Body: {}".format(
            request.body.read(int(request.headers["Content-Length"]))
            if int(request.headers.get("Content-Length", 0)) > 0
            else ""
        )
    )

    # Process the request!
    # We want to respond to new repositories, and ensure they have advanced security enabled (and have at least one branch)
    # Ultimately we want to have advanced security tests just for protected branches, not every commit on developer branches
    # HOWEVER, we should err on the side of running these earlier in the process, when identifying and correcting is easiest
    # Here's the logic.

    #  Case Action = Repository Create - Activity repository AND payload.action="created"
    #   UpdateRepository: { "security_and_analysis": {"advanced_security": { "status": "enabled" } } }
    #   Check for any content: 'GET /repos/{owner}/{repo}/contents/{path}' 
    #   IF empty
    #  Add a default README to force creation of branch:Update repository with PUT /repos/{owner}/{repo}/contents/README.md
    # 
    #  FUTURE EXPANSION
    #  Case Action = Major Release from development repository (Start of enterprise testing before deployment approval)
    #     Trigger workflow for dynamic security testing (pen for example) 
    return


webhooks = webhook_listener.Listener(port=port, handlers={"POST": parse_request})
webhooks.start()

while True:
    logger.debug("Still alive...")
    time.sleep(300)
