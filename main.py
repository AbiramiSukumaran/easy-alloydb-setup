# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import subprocess
import threading
import uuid
import json
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory storage for logs (Not suitable for production with multiple workers)
# Format: { 'deploy_id': {'logs': [], 'status': 'running'|'done'|'error'} }
deployments = {}

def run_billing_link(project_id):
    """
    Attempts to find an open billing account and link the project to it.
    REQUIREMENT: Must find an account named exactly "Google Cloud Platform Trial Billing Account".
    Returns (success_bool, message).
    """
    try:
        # 1. List billing accounts
        cmd = ["gcloud", "billing", "accounts", "list", "--format=json", "--filter=open=true"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        accounts = json.loads(result.stdout)
        
        if not accounts:
            return False, "No open billing accounts found for this user."

        # 2. Strict Search for "Google Cloud Platform Trial Billing Account"
        target_account = None
        target_name = "Google Cloud Platform Trial Billing Account"
        
        for acct in accounts:
            # Exact string match
            if acct.get('displayName') == target_name:
                target_account = acct
                break
        
        # 3. Handle Not Found (No fallback)
        if not target_account:
            return False, f"Error: Could not find a billing account named '{target_name}'. Please ensure you have an active trial account with this exact name."

        print(f"DEBUG: Found and selected Trial Account: {target_account.get('displayName')}")

        acct_id = target_account['name'].split('/')[-1] # format usually billingAccounts/ID
        acct_display = target_account.get('displayName', acct_id)

        # 4. Link project
        link_cmd = [
            "gcloud", "billing", "projects", "link", project_id,
            f"--billing-account={acct_id}"
        ]
        subprocess.run(link_cmd, capture_output=True, text=True, check=True)
        
        return True, f"Successfully linked project '{project_id}' to billing account '{acct_display}' ({acct_id})"
        
    except subprocess.CalledProcessError as e:
        return False, f"GCloud Error: {e.stderr}"
    except Exception as e:
        return False, str(e)

def run_gcloud_script(deploy_id, project, region, password, cluster, instance):
    """Runs the shell script and streams output to global storage."""
    
    cmd = ['./create_alloydb.sh', project, region, password, cluster, instance]
    
    deployments[deploy_id]['logs'].append(f"Starting command: {' '.join(cmd)}\n")
    
    try:
        # Use Popen to capture stdout/stderr in real-time
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1  # Line buffered
        )

        # Read line by line
        for line in process.stdout:
            deployments[deploy_id]['logs'].append(line)
        
        process.wait()
        
        if process.returncode == 0:
            deployments[deploy_id]['status'] = 'done'
            deployments[deploy_id]['logs'].append("\nSUCCESS: Deployment finished.\n")
        else:
            deployments[deploy_id]['status'] = 'error'
            deployments[deploy_id]['logs'].append(f"\nERROR: Script exited with code {process.returncode}\n")

    except Exception as e:
        deployments[deploy_id]['status'] = 'error'
        deployments[deploy_id]['logs'].append(f"\nEXCEPTION: {str(e)}\n")

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/link-billing', methods=['POST'])
def link_billing():
    project_id = request.form.get('project_id')
    if not project_id:
        return jsonify({'status': 'error', 'message': 'Project ID is required'})

    success, msg = run_billing_link(project_id)
    return jsonify({
        'status': 'success' if success else 'error',
        'message': msg
    })

@app.route('/deploy', methods=['POST'])
def deploy():
    # 1. Get data
    project_id = request.form.get('project_id')
    region = request.form.get('region')
    password = request.form.get('password')
    cluster_id = request.form.get('cluster_id')
    instance_id = request.form.get('instance_id')

    # 2. Create ID and Thread
    deploy_id = str(uuid.uuid4())
    deployments[deploy_id] = {'logs': [], 'status': 'running'}

    thread = threading.Thread(
        target=run_gcloud_script, 
        args=(deploy_id, project_id, region, password, cluster_id, instance_id)
    )
    thread.start()

    # 3. Return ID for polling
    return jsonify({'deployment_id': deploy_id})

@app.route('/logs/<deploy_id>')
def get_logs(deploy_id):
    if deploy_id not in deployments:
        return jsonify({'error': 'Not found'}), 404
    
    return jsonify({
        'logs': deployments[deploy_id]['logs'],
        'status': deployments[deploy_id]['status']
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
