import boto3
import pandas as pd

def list_all_hosted_zones():
    """
    List all hosted zones in Amazon Route 53.

    Returns:
    list of dicts: Each dict contains details about a hosted zone.
    """
    # Create a Route53 client
    client = boto3.client('route53')

    # Paginator to handle multiple pages of hosted zones
    paginator = client.get_paginator('list_hosted_zones')
    hosted_zones = []

    try:
        # Iterate through paginated responses
        for page in paginator.paginate():
            for zone in page['HostedZones']:
                hosted_zones.append({
                    'Name': zone['Name'],
                    'ID': zone['Id'],
                    'Record Set Count': zone['ResourceRecordSetCount']
                })
                # print(f"Name: {zone['Name']}\t ID: {zone['Id']}\t Record Count: {zone['ResourceRecordSetCount']}")
        # Convert list of dicts to a DataFrame
        df = pd.DataFrame(hosted_zones)
        return df
        # return hosted_zones
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Call the function to list all hosted zones
all_hosted_zones_df = list_all_hosted_zones()

# Display the DataFrame
if not all_hosted_zones_df.empty:
    print(all_hosted_zones_df)
else:
    print("No hosted zones found or an error occurred.")