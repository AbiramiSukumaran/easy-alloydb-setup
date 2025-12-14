# AlloyDB Easy Setup for Development Purposes
This tool helps you link a billing account and spin up an AlloyDB Cluster + Instance (with all other API & network dependencies) using your active Google Cloud credentials.

## Clone the Repo & Navigate into the project directory
   
It will open a new tab (make sure you are in the right email account), clone the repository, and enter the directory automatically.

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/AbiramiSukumaran/easy-alloydb-setup&cloudshell_open_in_editor=README.md)

## Run:
   
In the Cloud Shell Terminal at the bottom, type the following and hit Enter:

sh run.sh

## That's it!!! Access it on web

Once the script prints "Starting Server on Port 8080"...

Click the link that you see in the terminal **or**

Click the Web Preview button (looks like an eye 👁️) in the Cloud Shell toolbar.

Select "Preview on port 8080".




Manual commands for above steps:

Run commands in your Cloud Shell Terminal one by one:

git clone https://github.com/AbiramiSukumaran/easy-alloydb-setup

cd easy-alloydb-setup

sh run.sh

Access UI!




⚠️⚠️⚠️ Requirements

Permissions: You must have Owner or Editor permissions on the Google Cloud Project you intend to deploy to.

Project: The project must be created before running this tool (the tool handles billing linking, but not project creation).
