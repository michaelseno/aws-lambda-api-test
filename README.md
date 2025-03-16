## API Test Automation with CI/CD Pipeline using GitHub Actions and AWS

This project demonstrates a fully automated API testing framework using GitHub Actions, AWS Lambda, and other AWS services. The system is designed to trigger API tests on pull requests, deploy code to Lambda, and notify via SNS and EventBridge.

### Technologies Used:
- GitHub Actions
- AWS Lambda
- AWS S3
- AWS CloudWatch
- AWS EventBridge
- AWS SNS
- Python
- Unittest

### Project Overview:
The goal of this project was to automate API testing in a CI/CD pipeline, with automatic deployment to AWS Lambda and notifications through SNS. The process also includes periodic test runs using EventBridge cron jobs.

### How It Works:
1. GitHub Action triggered by pull requests to run unit tests.
2. If tests are successful, then the pull request can be merged
3. once merged, artifact is created and uploaded to S3.
4. Lambda function is updated and triggered to run the API tests.
5. EventBridge triggers the Lambda function periodically, Saves the logs into AWS CloudWatch and SNS sends notifications based on test results.

### Code Samples:

```yaml
name: API Test Automation Workflow
on:
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Install Dependencies
        run: |
          pip install -r requirements.txt

      - name: Run Unit Tests
        run: |
          python3 -m unittest discover -v tests
