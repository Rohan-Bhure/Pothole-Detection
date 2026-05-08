from inference_sdk import InferenceHTTPClient
from config import ROBOFLOW_API_KEY, WORKSPACE, WORKFLOWS

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=ROBOFLOW_API_KEY
)

def run_model(image_path, mode="image"):
    result = client.run_workflow(
        workspace_name=WORKSPACE,
        workflow_id=WORKFLOWS[mode],
        images={"image": image_path},
        use_cache=True
    )
    return result[0]