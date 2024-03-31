import datetime
import json
import subprocess
import urllib
import webbrowser

import boto3
import requests


def open_console(hours, print_url, copy_clipboard):
    session = boto3.Session()
    temp_credentials = session.get_credentials()

    session_data = {
        "sessionId": temp_credentials.access_key,
        "sessionKey": temp_credentials.secret_key,
        "sessionToken": temp_credentials.token,
    }

    signin_endpoint = "https://signin.aws.amazon.com/federation"

    response = requests.get(
        signin_endpoint,
        params={
            "Action": "getSigninToken",
            "SessionDuration": str(datetime.timedelta(hours=hours).seconds),
            "Session": json.dumps(session_data),
        },
    )

    signin_token = json.loads(response.text)

    query_string = urllib.parse.urlencode(
        {
            "Action": "login",
            "Issuer": "Brawser",
            "Destination": "https://console.aws.amazon.com/",
            "SigninToken": signin_token["SigninToken"],
        }
    )
    federated_url = f"{signin_endpoint}?{query_string}"

    if(print_url):
        print("The federated URL is below:")
        print("")
        print(federated_url)
        print("")

    if(copy_clipboard):
        subprocess.run('pbcopy', universal_newlines=True, input=federated_url)
        print("Copied the federated URL.")

    if not print_url and not copy_clipboard:
        print("Open Managed Console")
        webbrowser.open(federated_url)


