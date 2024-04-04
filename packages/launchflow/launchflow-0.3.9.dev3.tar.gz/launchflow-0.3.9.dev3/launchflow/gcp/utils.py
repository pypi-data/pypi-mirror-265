import os
from typing import Optional

from google.auth import default, impersonated_credentials

from launchflow.context import ctx


# Cloud Run automatically sets the K_SERVICE environment variable
# Docs: https://cloud.google.com/run/docs/container-contract#env-vars
def is_running_on_cloud_run():
    """Check if running on Google Cloud Run."""
    return "K_SERVICE" in os.environ


def get_service_account_credentials(
    project_name: Optional[str] = None,
    environment_name: Optional[str] = None,
) -> str:
    """
    Get the GCP service account credentials for the specified project and environment.
    """
    target_scopes = ["https://www.googleapis.com/auth/cloud-platform"]

    # Load the default credentials (from environment, compute engine, etc.)
    creds, _ = default(scopes=target_scopes)

    if is_running_on_cloud_run() and creds.service_account_email is not None:
        # If running on Cloud Run, use the default credentials
        return creds

    # If not on Cloud Run, fetch the GCP service account email from LaunchFlow
    gcp_service_account_email = ctx.get_gcp_service_account_email(
        project_name, environment_name
    )

    # Define the target service account to impersonate
    target_credentials = impersonated_credentials.Credentials(
        source_credentials=creds,
        target_principal=gcp_service_account_email,
        target_scopes=target_scopes,
        lifetime=30 * 60,  # The maximum lifetime in seconds
    )

    return target_credentials
