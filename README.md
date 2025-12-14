AlloyDB Quick Setup Tool

This tool helps you link a billing account and spin up an AlloyDB Cluster + Instance using your active Google Cloud credentials.


Make sure this repo is cloned in your Google Cloud Shell Editor or 
you can do so by running the following command in the Cloud Shell command line terminal:

 ### git clone https://github.com/AbiramiSukumaran/easy-alloydb-setup


🚀 How to Run


### cd easy-alloydb-setup

Run the start script:

### sh run.sh



🖥️ Accessing the UI

Once the script prints "Starting Server on Port 8080"...

Click the Web Preview button (looks like an eye 👁️) in the Cloud Shell toolbar.

Select "Preview on port 8080".

⚠️ Requirements

Permissions: You must have Owner or Editor permissions on the Google Cloud Project you intend to deploy to.

Project: The project must be created before running this tool (the tool handles billing linking, but not project creation).
