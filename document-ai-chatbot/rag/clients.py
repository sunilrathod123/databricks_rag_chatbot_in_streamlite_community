from databricks.sdk import WorkspaceClient
from databricks_openai import DatabricksOpenAI

def build_gateway_client(host, token):
    workspace = WorkspaceClient(host=host, token=token)
    return DatabricksOpenAI(workspace_client=workspace, use_ai_gateway=True)
