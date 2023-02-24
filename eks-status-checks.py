import boto3

eks_client = boto3.client('eks')

clusters = eks_client.list_clusters()['clusters']


for cluster in clusters:
    response = eks_client.describe_cluster(
        name=clusters
    )
    cluster_info = response['cluster']
    cluster_status = cluster_info['status']
    cluster_version = cluster_info['version']
    cluster_endpoint = cluster_info['endpoint']
    print(f"{cluster} status is {cluster_status}\n version is {cluster_version}\n endpoint is {cluster_endpoint}")
