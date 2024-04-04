from typing import Optional

from google.auth import default, impersonated_credentials
from launchflow.context import ctx


def get_service_account_credentials(
    project_name: Optional[str] = None,
    environment_name: Optional[str] = None,
) -> str:
    """
    Get the GCP service account credentials for the specified project and environment.
    """
    gcp_service_account_email = ctx.get_gcp_service_account_email(
        project_name, environment_name
    )
    # Load the default credentials (from environment, compute engine, etc.)
    creds, _ = default()

    # Define the target service account to impersonate
    target_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    target_credentials = impersonated_credentials.Credentials(
        source_credentials=creds,
        target_principal=gcp_service_account_email,
        target_scopes=target_scopes,
        lifetime=30 * 60,  # The maximum lifetime in seconds
    )

    return target_credentials
