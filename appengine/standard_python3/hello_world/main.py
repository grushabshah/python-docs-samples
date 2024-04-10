# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]
from flask import Flask
import sys, os, subprocess
from flask import request
import json

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

METADATA_NETWORK_INTERFACE_URL = (
    "http://metadata/computeMetadata/v1/instance/network-interfaces/0/"
    "access-configs/0/external-ip"
)


def get_external_ip():
    """Gets the instance's external IP address from the Compute Engine metadata
    server.

    If the metadata server is unavailable, it assumes that the application is running locally.

    Returns:
        The instance's external IP address, or the string 'localhost' if the IP address
        is not available.
    """
    try:
        r = requests.get(
            METADATA_NETWORK_INTERFACE_URL,
            headers={"Metadata-Flavor": "Google"},
            timeout=2,
        )
        return r.text
    except requests.RequestException:
        logging.info("Metadata server could not be reached, assuming local.")
        return "localhost"


@app.route("/")
def hello():
    """Return a friendly HTTP greeting.

    Returns:
        A string with the words 'Hello World!'.
    """
    proc = subprocess.Popen('df -h; cat /layers/google.python.appengine/config', stdout=subprocess.PIPE, shell=True)
    dfoutput = proc.stdout.read()
    proc = subprocess.Popen('mount; pwd; ls -al; echo "=== $(date) ==="', stdout=subprocess.PIPE, shell=True)
    osrelease = proc.stdout.read()
    # external_ip = get_external_ip()
    return f"Hello World! (Python 3 Version: {sys.version}) \n ENV VARS: \n {os.environ} \n /etc/os-release: {osrelease.decode()}\n df: {dfoutput.decode()} \nHeaders:\n {print(json.dumps(dict(request.headers), indent=4))}".replace('\n', '<br>')


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 8080)), debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
