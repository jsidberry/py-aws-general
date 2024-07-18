import boto3
import pprint as pp


def get_hosted_zone_id(domain_name):
    """
    Retrieve the hosted zone ID for a given domain name from Amazon Route 53.

    Parameters:
    domain_name (str): The domain name to find the hosted zone ID for.

    Returns:
    str: The hosted zone ID if found, None otherwise.
    """
    # Create a Route53 client
    client = boto3.client('route53')

    # Paginator to handle the case where there are more hosted zones than returned in one response
    paginator = client.get_paginator('list_hosted_zones')

    try:
        # Iterate through paginated responses
        for page in paginator.paginate():
            for zone in page['HostedZones']:
                if zone['Name'].startswith(domain_name):
                    # print(f"Hosted Zone found: {zone['Name']}ID: {zone['Id']}")
                    return zone['Id']
        print("No hosted zone found for the domain.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def update_nameservers(hosted_zone_id, domain_name, new_nameservers):
    """
    Update the nameserver records for a hosted zone in Amazon Route 53.

    Parameters:
    hosted_zone_id (str): The ID of the hosted zone.
    domain_name (str): The domain name, ending with a dot (e.g., "example.com.").
    new_nameservers (list): List of nameserver strings.

    Returns:
    dict: The response from the Route 53 ChangeResourceRecordSets API call.
    """
    client = boto3.client('route53')

    # Define the change to the NS record set
    record_change = {
        'Action': 'UPSERT',  # 'UPSERT' will either update or create the record set
        'ResourceRecordSet': {
            'Name': domain_name,
            'Type': 'NS',
            'TTL': 300,
            'ResourceRecords': [{'Value': ns} for ns in new_nameservers]
        }
    }

    try:
        response = client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                'Comment': 'update NS records',
                'Changes': [record_change]
            }
        )
        print("Nameserver update request submitted successfully.")
        return response
    except Exception as e:
        print(f"Failed to update nameservers: {e}")
        return None


# Example usage:
domain_name       = 'example.com.'        # Notice the trailing dot, which is necessary
hosted_zone_resp  = get_hosted_zone_id(domain_name)  
hosted_zone_id    = hosted_zone_resp[12:] # Replace with your actual hosted zone ID
new_nameservers   = [
    'NS1020.WEBSITEWELCOME.COM', # Replace these with the actual nameservers
    'NS1019.WEBSITEWELCOME.COM'
]

if hosted_zone_id:
    print(f"\nHosted Zone ID for {domain_name}: {hosted_zone_id[12:]}")
    response = update_nameservers(hosted_zone_id, domain_name, new_nameservers)
    if response:
        print(f"\nHTTP Status Code: {response['ResponseMetadata']['HTTPStatusCode']}")
else:
    print("\nHosted Zone ID not found.")
