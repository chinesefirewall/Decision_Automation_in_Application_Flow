c# Import necessary Python libraries
import io
import time
from datetime import datetime
from functools import wraps

import boto3
import pandas as pd
import psycopg2

# Import AWS S3 credentials
from AwsCredential import AwsAccessKeyID, AwsSecretAccessKey

# Configuration for connecting to the local PostgreSQL database
DataBase_params = {
    'host': "localhost",
    'database': "postgres",
    'user': "niyi",
    'password': "Xingjin112"
}

# Define the target S3 bucket name
S3_BUCKET = 'creditstar-data-bucket'

# Define SQL queries for fetching data from the database
queries = {
    'paid_loans_count': """
        SELECT client_id, COUNT(id) AS paid_loans_count
        FROM loan
        WHERE status = 'paid'
        GROUP BY client_id
    """,
    'days_since_last_late_payment': """
        SELECT client_id, CURRENT_DATE - MAX(matured_on) AS days_since_last_late_payment
        FROM loan
        WHERE status = 'overdue'
        GROUP BY client_id

    """,
    'profit_in_last_90_days_rate': """
    SELECT client_id, SUM(interest) / SUM(payment.amount) AS profit_in_last_90_days_rate
    FROM payment
    JOIN loan ON payment.loan_id = loan.id
    WHERE payment.created_on >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY client_id
"""
}

# Define batch size for data processing, useful when handling large datasets
BATCH_SIZE = 500

# Establish S3 connections using provided credentials
s3_resource = boto3.resource('s3', aws_access_key_id=AwsAccessKeyID, aws_secret_access_key=AwsSecretAccessKey)
s3_client = boto3.client('s3', aws_access_key_id=AwsAccessKeyID, aws_secret_access_key=AwsSecretAccessKey)


def get_data_chunk(query, connection, offset):
    """Fetch a chunk of data from the database based on the provided offset and query."""
    df = pd.read_sql(query + f" LIMIT {BATCH_SIZE} OFFSET {offset}", connection)
    return df


def retry(times=3, delay=3):
    """Decorator for retrying a function in case of exceptions."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
            raise Exception(f"Failed to execute {func.__name__} after {times} attempts!")

        return wrapper

    return decorator


# Apply the decorator to functions that require retrying
@retry(times=3, delay=3)
def upload_to_s3(dataframe, bucket_name, file_name):
    """Upload a Pandas dataframe to an S3 bucket as a CSV."""
    try:
        csv_buffer = io.StringIO()
        dataframe.to_csv(csv_buffer, index=False)
        s3_resource.Object(bucket_name, file_name).put(Body=csv_buffer.getvalue())
    except Exception as e:
        print(f"Error uploading to S3: {e}")


def main():
    """Main function for processing data and uploading to S3."""
    connection = psycopg2.connect(**DataBase_params)
    try:
        for name, query in queries.items():

            offset = 0
            new_data = []  # A list to store dataframes

            while True:
                df_chunk = get_data_chunk(query, connection, offset)

                # Exit loop if chunk is empty
                if df_chunk.empty:
                    break

                new_data.append(df_chunk)

                # Increase the offset for the next chunk
                offset += BATCH_SIZE

            # Concatenate all the chunks into a single dataframe
            combined_data = pd.concat(new_data, ignore_index=True)

            # Removing duplicates (if needed)
            combined_data.drop_duplicates(inplace=True)

            # Get the current timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            upload_to_s3(combined_data, S3_BUCKET, f"{name}_{timestamp}.csv")

        connection.commit()

    except Exception as e:
        connection.rollback()
        print(f"Error processing data: {e}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
