# Trips Data Ingestion Challenge

### Description 

This challenge will evaluate your proficiency in Data Engineering, and your knowledge in Software development as well. 

### Assignment 

Your task is to build an automatic process to ingest data on an on-demand basis. The data represents trips taken by different vehicles, and include a city, a point of origin and a destination. 

This CSV file gives you a small sample of the data your solution will have to handle. We would like to have some visual reports of this data, but in order to do that, we need the following features. 

We do not need a graphical interface. Your application should preferably be a REST API, or a console application. 

### Mandatory Features

- [x] There must be an automated process to ingest and store the data. 
- [x] Trips with similar origin, destination, and time of day should be grouped together. 
- [x] Develop a way to obtain the weekly average number of trips for an area, defined by a bounding box (given by coordinates) or by a region. 
- [x] Develop a way to inform the user about the status of the data ingestion without using a polling solution. 
- [x] The solution should be scalable to 100 million entries. It is encouraged to simplify the data by a data model. Please add proof that the solution is scalable. 
- [x] Use a SQL database.

### Bonus features 

- [x] Containerize your solution. 
- [x] Sketch up how you would set up the application using any cloud provider (AWS, Google Cloud, etc). 
- [x] Include a .sql file with queries to answer these questions: 
- [x] From the two most commonly appearing regions, which is the latest datasource? ○ What regions has the "cheap_mobile" datasource appeared in? 

### Deliverables 

Your project should be stored in a public GitHub repository. When you are done, send us the link to your repo. 

It’s not necessary to host this application anywhere (although you can if you like). Just make sure your repo has a README.md which contains any instructions we might need for running your project.

### Observations/Recommendation
● If you will integrate your solution with any cloud platform, you must provide an account
(user/password) to us to test it.
● Please detail your code so that we can understand your reasoning and its use regardless
of platform expertise.
● We recommend recording a video explaining how it works and steps of execution.

## 💻 Requirements

To execute this process, you need to have installed the softwares below:

1. Git
2. Docker
3. Docker Compose

## :pencil: Local Architecture

![local-architecture](https://user-images.githubusercontent.com/3865974/167314127-d86f91e5-a104-4e97-88ec-009babe66a30.png)

For this challenge, I designed an architecture that uses a docker-compose to create a container with python scripts that meets the challenge requirements, a Redis server to enqueue jobs, and a PostgreSQL database to store data. 

### 🚀 Running the ingestion process

To run the files ingestion, the user must put files in 'files_to_ingest' directory. After this, run the below commands in root directory:

```
docker-compose up -d
docker-compose exec ingest_app python app.py trips.csv
```

The app build will create a volume mapped between the host and the container. So, to add more files to the ingestion process, just put them in the files_to_ingest directory in root.

If you wish to ingest more than one file, just add it after the script path. The files must be separated by a comma and it must be just the file name, without the full path.

When you run the exec command, the script will execute the following steps:

1. Get the files list to ingest
2. For each file, will add the ingestion job to Redis queue using the [RQ library](https://python-rq.org/).

The ingestion job will execute the following steps:

1. Read the CSV file passed as argument and create a pandas dataframe with the file data
2. Save this panda dataframe to 'trips' table in PostgreSQL. I decided to use the [to_sql](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html) pandas function, because it will create the table if does not exist.
>All steps executed log messages to show the user what's going on background.

I decided to use Redis with the RQ library because it gave me the possibility to enqueue jobs to be processed in the background with workers.
In order to simplify the running of this challenge, I've set to jobs run synchronously. But asynchronously it can be set just by changing one parameter to True.

### :chart_with_upwards_trend: Showing reports results

To show the queries results, just run the below command after doing the ingestion process.

```
docker-compose exec ingest_app python metrics.py
```
The results will be printed in the console.

## :cloud: Cloud Architecture

![aws-architecture](https://user-images.githubusercontent.com/3865974/167316405-1ea0104b-49a3-450d-bde1-bbc10498a368.png)

For the cloud architecture, I decided to use AWS because I am more familiar with this provider.

In order to achieve scalability and meet the requirement of using a REST API, this solution starts with the user making a POST to the API Gateway and sending the CSV file to be processed. This API will call an AWS Lambda Function which will convert this CSV file to a JSON format and send it to a Kinesis Data Firehose, that will deliver this data in an S3 bucket with parquet format. To query this data with a relational database, an Amazon Redshift will be created with an EXTERNAL TABLE, mapping to the S3 path with the parquet files. With the feature 'Redshift Spectrum', users can perform SQL queries on data stored in S3 buckets.

The tool that made scalability possible is the Kinesis Firehose, which is a serverless tool and can scale up easily.
According to [AWS documentation](https://www.amazonaws.cn/en/kinesis/data-firehose/features/):
>Amazon Kinesis Data Firehose is the easiest way to capture, transform, and load streaming data into data stores and analytics tools. Kinesis Data Firehose is a fully managed service that makes it easy to capture, transform, and load massive volumes of streaming data from hundreds of thousands of sources into Amazon S3, Amazon Redshift...

>Scales elastically
>Based on your ingestion pattern, Kinesis Data Firehose service might proactively increase the limits when excessive throttling is observed on your delivery stream.

It's possible for Firehose to send the data directly to Redshift. But I decided to send it to S3 because this makes it possible for the user to query this data also using AWS Athena.

To create the whole infrastructure, I would use Terraform, an infrastructure as code (IaC) tool that facilitates the provisioning and managing infrastructure on-prem and in the cloud.

[⬆ Back to top](#trips-data-ingestion-challenge)<br>
