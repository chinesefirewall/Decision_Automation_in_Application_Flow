
---

# Project Overview

This project focuses on extracting data from a PostgreSQL database and subsequently uploading it to Amazon S3. This documentation elucidates the choices made in terms of infrastructure, scalability factors, and the rationale behind the selected data streaming method.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [How to Run the Code](#how-to-run-the-code)
- [Infrastructure Choices](#infrastructure-choices)
  - [Infrastructure as Code (IaC)](#infrastructure-as-code-iac)
  - [Scripted Implementation](#scripted-implementation)
- [Scalability](#scalability)
  - [Horizontal Scalability](#horizontal-scalability)
  - [Vertical Scalability](#vertical-scalability)
- [Real-time Data Streaming](#real-time-data-streaming)
- [Known Issues](#known-issues)
- [Future Improvements](#future-improvements)
- [Recommendation](#recommendation)

## Introduction

This project revolves around the task of securely extracting data from a PostgreSQL database and uploading it to Amazon S3, offering a robust solution to data management challenges.

## Prerequisites

Ensure the availability of the following tools and services to seamlessly run this project:
- PostgreSQL: The foundation for our data management.
- Amazon S3: The choice for data storage.
- Python: The primary language for script execution.
- boto3: Python SDK for AWS services, enabling Python developers to write software that makes use of Amazon S3.
- Pandas: A powerful data manipulation library for Python.


## Setup and Installation

1. Clone the project repository onto your local system.
2. Change to the project's directory.
3. To install necessary Python packages, run: `pip install -r requirements.txt`.
4. Configure PostgreSQL and Amazon S3 credentials accordingly.


## How to Run the Code

1. Change to the project directory.
2. Launch the main script with the command: `python main.py`.

## Infrastructure Choices

### Infrastructure as Code (IaC)

Infrastructure as Code (IaC) is undoubtedly an effective method for extensive implementations. However, it can accrue costs when deployed on the cloud.

### Scripted Implementation

To circumvent potential expenses related to cloud usage via IaC, this project adopts a scripted implementation. This choice not only curtails costs but also offers more granular control over data transactions, making it apt for this project.

## Scalability

Drawing from the insights gained during this project:

### Horizontal Scalability (Scaling Out)

Scaling out, or horizontal scalability, entails integrating more servers to accommodate heightened workloads.

**Advantages**:
- **Flexibility**: Allows easy addition of servers to the system.
- **Load Distribution**: Prevents over-reliance on a single system, thereby sidestepping potential bottlenecks.
- **Fault Tolerance**: System continuity remains unaffected even if a server fails.

**Disadvantages**:
- **Complexity**: Multi-server management can become intricate.
- **Data Consistency**: Keeping data synchronized in distributed systems is often challenging.

### Vertical Scalability (Scaling Up)

Vertical scalability involves bolstering a server's existing resources.

**Advantages**:
- **Simplicity**: Directly increasing server resources offers a straightforward scalability solution.
- **Data Consistency**: Easier data synchronization compared to horizontal scalability.

**Disadvantages**:
- **Cost**: Premium servers come with a heftier price tag.
- **Growth Limitations**: Servers can only be scaled up to a certain extent.

For enhanced scalability, consider integrating load balancers, optimizing database operations, and caching frequently accessed information.

## Real-time Data Streaming

In this project, data is fetched in batches using Python-SQL queries, leveraging the Postgres server's processing efficiency instead of loading data directly into Python dataframes. While this approach suits the current scale, it may not meet real-time streaming criteria.

For true real-time data streaming, consider the following methods:

### Using Polling
By periodically checking the database for new entries, polling can facilitate continuous data processing.

### Cron Job

Automating the data extraction and upload process at predefined intervals is possible through cron jobs.

**Advantages**:
- Straightforward setup.
- Efficient operations at preset times.

**Disadvantages**:
- Might result in update lags.
- Lacks the continuous data flow typical of real-time systems.

Incorporating cron jobs streamlines the data extraction and uploading process.

## Rationale for Excluding Client Names in S3 Bucket Uploads

**1. Adherence to Privacy Regulations:** To maintain compliance with industry-specific regulations, prioritizing client confidentiality is essential. This initiative rigorously follows both regional and industry privacy standards.

**2. Maintaining Data Consistency:** Client names in the primary database can undergo modifications. Relying on them as unique identifiers can jeopardize data precision. Hence, to ensure uniform data linkage, we use stable identifiers like client IDs.

**3. Streamlining Data Processes:** Including additional attributes, such as client names, escalates the file's size. This might be inconsequential for petite datasets but becomes crucial when handling voluminous data.

**4. Prevention of Data Duplication:** Integrating the produced CSV outputs with other systems that already possess a mapping of client names and IDs renders the inclusion of names superfluous.


## Known Issues

While this project and its documentation underwent rigorous testing before release, potential issues include:
- Absence of error handling for invalid AWS credentials.
- Risk of data duplication if the script faces interruptions and is restarted.

## Future Improvements

- Introducing a logging mechanism to monitor uploads.
- Incorporating more queries to extract additional database data.
- Integrating AWS Lambda for event-triggered data uploads.

## Recommendation

To demonstrate proficiency in real-time data processing, adopting a polling-based approach is recommended. Although this method offers a rudimentary representation of real-time systems, it hints at an understanding of its limitations and potential enhancements.

## You can access the s3 tables usingthe following  presigned URLs:




```markdown
### Data Tables

1. [Profit in Last 90 Days Rate](https://shorturl.at/aEGY7)

2. [Paid Loans Count](https://shorturl.at/mpuFV)

3. [Days Since Last Late Payment](https://shorturl.at/sAJU7)
```

---

Credit: Niyi Adebayo 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
