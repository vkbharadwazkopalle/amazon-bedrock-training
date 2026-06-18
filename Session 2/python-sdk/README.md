# Amazon Bedrock - Python SDK (Session 2)

This README describes steps from environment setup to running the sample app.

Prerequisites
- Python 3.9+ installed
- pip
- AWS account with Bedrock access (and appropriate IAM permissions)

1) Clone repository

	git clone https://github.com/vkbharadwazkopalle/amazon-bedrock-training.git
	cd Session\ 2/python-sdk

2) Create and activate virtual environment

	`python -m venv .venv`
	# macOS / Linux
	`source .venv/bin/activate`
	# Windows (PowerShell)
	`.\.venv\Scripts\Activate.ps1`

3) Install dependencies

    ```
	pip install --upgrade pip
	pip install -r requirements.txt
    ```

4) Configure AWS credentials

- Option A: environment variables
```
  export AWS_ACCESS_KEY_ID=YOUR_KEY
  export AWS_SECRET_ACCESS_KEY=YOUR_SECRET
  export AWS_REGION=us-west-2
```

- Option B: AWS CLI

  aws configure

- Option C: 
go to bedrock service
under quickstart, click on Generate API key
export the api key as env

get the bedrock bearer token from the console and run it in the terminal for temp session

If using AWS Bedrock, ensure you have endpoint/region and any required IAM policy.

5) Set application-specific environment variables

	# example
	export MODEL_ID="amazon-mpt-7b-instruct"   # set to desired Bedrock model

6) Run the feature scripts, for example

	`python chat_cli.py`

7) Common troubleshooting
- If dependencies fail, confirm Python version and reinstall in a fresh venv.
- If auth errors occur, verify AWS credentials and IAM permissions.

Notes
- Replace placeholders (YOUR_KEY, YOUR_SECRET) with real values.
- Adjust MODEL_ID and AWS_REGION to match your Bedrock setup.

