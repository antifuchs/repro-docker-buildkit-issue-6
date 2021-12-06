"""An AWS Python Pulumi program"""

import pulumi
import base64
import pulumi_aws as aws
import pulumi_docker_buildkit as docker


def get_registry_info(registry_id: str):
    creds = aws.ecr.get_credentials(registry_id=registry_id)
    username, password = base64.b64decode(creds.authorization_token).decode().split(":")
    return docker.RegistryArgs(
        server=creds.proxy_endpoint,
        username=username,
        password=password,
    )

for i in range(10):
    repo = aws.ecr.Repository(
        f"ecr-repo-{i}",
        image_scanning_configuration=aws.ecr.RepositoryImageScanningConfigurationArgs(
            scan_on_push=True,
        ),
    )
    docker.Image(
            f"image-{i}",
            dockerfile="Dockerfile",
            context="repo",
            name=repo.repository_url,
            registry=repo.registry_id.apply(get_registry_info),
        )
