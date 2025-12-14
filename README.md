# AlloyDB Easy Setup for Development Purposes
This tool helps you link a billing account and spin up an AlloyDB Cluster + Instance (with all other API & network dependencies) using your active Google Cloud credentials.

## Start the process
If you have already landed in the terminal and cloned the repo, then just

1. Run the following command in your terminal from the project  folder:

#### sh run.sh

2. Next step, access the web UI for AlloyDB set up.

## But if you're yet to clone the repo:

#### Option A: One-Click 

1. Click the "Open in Cloud Shell" button.
   
It will open a new tab, clone the repository, and enter the directory automatically.

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/AbiramiSukumaran/easy-alloydb-setup&cloudshell_open_in_editor=README.md)

2. Run the Start Script:
   
In the Cloud Shell Terminal at the bottom, type the following and hit Enter:

sh run.sh

#### Option B: Manual Run

If you prefer to run commands manually in your existing terminal one by one:

git clone https://github.com/AbiramiSukumaran/easy-alloydb-setup

cd easy-alloydb-setup

sh run.sh

## 🖥️ Access the UI for setup

Once the script prints "Starting Server on Port 8080"...

Click the Web Preview button (looks like an eye 👁️) in the Cloud Shell toolbar.

Select "Preview on port 8080".




⚠️⚠️⚠️ Requirements

Permissions: You must have Owner or Editor permissions on the Google Cloud Project you intend to deploy to.

Project: The project must be created before running this tool (the tool handles billing linking, but not project creation).
