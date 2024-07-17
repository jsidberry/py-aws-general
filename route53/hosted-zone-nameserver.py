import boto3

def create_route53_hosted_zone(domain_name):
    """
    Create a hosted zone in Amazon Route 53 for a specified domain.

    Parameters:
    domain_name (str): The domain name for which to create the hosted zone.

    Returns:
    dict: The response containing the hosted zone details.
    """
    # Create a Route53 client
    client = boto3.client('route53')

    # Create the hosted zone
    try:
        response = client.create_hosted_zone(
            Name=domain_name,
            CallerReference=str(hash(f"hosted_zone_{domain_name}")),
            HostedZoneConfig={
                'Comment': 'Hosted zone created by Boto3',
                'PrivateZone': False
            }
        )
        print("Hosted Zone created successfully.")
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Replace 'example.com' with your domain name
domain_name = 'example.com'
response = create_route53_hosted_zone(domain_name)
if response:
    print("Hosted Zone ID:", response['HostedZone']['Id'])
    print("Name Servers:", response['DelegationSet']['NameServers'])
