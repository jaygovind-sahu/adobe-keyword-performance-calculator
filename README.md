# Adobe Search Keyword Performance

Process to calculate the search keyword performance.

## Process Overview

Input is a simple tab separated file which contains what we call 
"hit level data". A hit level record is a single "hit" from a 
visitor on the client's site. Based on the client's implementation, 
several variables can be set and sent to Adobe Analytics for 
deeper analysis.

This Python application reads this hit level data and derive the
performance - answering the question - how much revenue is the client
getting from external search engines, such as Google, Yahoo and MSN,
and which keywords are performing the best based on revenue.

## Development Environment

### Create Virtual Environment
```shell
$ virtualenv .env
```

### Activate Virtual Environment
```shell
$ source .env/bin/activate 
```

### Install Dependencies
```shell
$ make install
```

### Run Lint
```shell
$ make lint
```

### Run Tests
```shell
$ make test
```
Above command also includes running the lint.

### Run application 
```shell
$ spark-submit --py-files path/to/keyword_perf.zip path/to/main.py path/to/input.tsv
```
Path to the packaged zip file, `main.py` and input file should be 
substituted in above command.

### Test Application in Local
```shell
$ make run-local
```
Result is saved under `tests/keyword_perf/output/`.

## Deployment

Deployment is done through GitHub Actions.
* [test.yml](test.yml) - Runs lint and tests on every push.
* [deploy.yml](deploy.yml) - Deploys the code to S3 after successful completion of tests.

## Production Environment (AWS)
* Code is deployed into an S3 bucket
* Input file is uploaded into an S3 bucket
* An event is fired when file is uploaded to S3 to kick of a Lambda function
* Above Lambda function in turn spins up an EMR cluster and adds a step for processing - passing the input file path from `event`
