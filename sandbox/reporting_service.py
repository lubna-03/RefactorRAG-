import boto3
import json
import datetime
import uuid
from config import S3_REPORT_BUCKET_NAME
from exceptions import ReportStorageError

class ReportingService:
    def __init__(self, s3_bucket_name: str):
        self.s3_bucket_name = s3_bucket_name
        # Initialize S3 client. In a real app, credentials would be managed securely.
        # For local testing, ensure AWS credentials are configured (e.g., via environment variables or ~/.aws/credentials)
        try:
            self.s3_client = boto3.client('s3')
            # Optional: Verify bucket exists or create it if necessary (for dev/test)
            # self.s3_client.head_bucket(Bucket=self.s3_bucket_name)
        except Exception as e:
            print(f"WARNING: Could not initialize S3 client. Reports will be simulated. Error: {e}")
            self.s3_client = None # Set to None if initialization fails

    def store_transaction_report(self, transaction_details: dict) -> bool:
        try:
            report_filename = f"transaction_report_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4()}.json"
            report_content = json.dumps(transaction_details, indent=2)

            if self.s3_client:
                # Simulate uploading to S3
                print(f"DEBUG: Uploading report '{report_filename}' to S3 bucket '{self.s3_bucket_name}'")
                # self.s3_client.put_object(Bucket=self.s3_bucket_name, Key=report_filename, Body=report_content)
                print(f"DEBUG: S3 upload simulated successfully for {report_filename}")
            else:
                print(f"DEBUG: S3 client not initialized. Simulating local storage of report '{report_filename}'.")
                # Fallback or simulation for when S3 client isn't available
                # with open(f"/tmp/{report_filename}", "w") as f: # Use /tmp for cross-platform temp storage
                #     f.write(report_content)
                print(f"DEBUG: Report content: {report_content}")

            return True
        except Exception as e:
            print(f"ERROR: Failed to store transaction report: {e}")
            raise ReportStorageError(f"Failed to store transaction report: {e}")
