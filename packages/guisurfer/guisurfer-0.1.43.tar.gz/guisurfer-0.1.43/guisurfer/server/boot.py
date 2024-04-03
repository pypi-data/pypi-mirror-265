import os

from guisurfer.agent.types import AgentType
from guisurfer.server.models import EnvVarOptModel, LLMProviders


#   - name: "OPENAI_API_KEY",
#     description: "OpenAI API Key"
#     required: False
#     secret: True
#   - name: "GEMINI_API_KEY",
#     description: "Gemini API Key"
#     required: False
#     secret: True
#   - name: "ANTHROPIC_API_KEY",
#     description: "Anthropic API Key"
#     required: False
#     secret: True
#   - name: PREFERRED_MODEL
#     description: "Preferred model to use"
#     required: False
#     default: "gpt4v"
#     options: ["gpt4v", "claud-opus", "gemini-pro-v"]


def ensure_common_models():
    branch = os.getenv("BRANCH")
    if not branch:
        raise ValueError("$BRANCH must be set")
    tag = "latest"
    if branch != "main":
        tag = f"latest-{branch}"
    try:
        found = AgentType.find(name="SurfDino", owner_id="patrick.barker@kentauros.ai")
        if found:
            print("Common models found")
            return

        print("Creating common models...")
        AgentType(
            name="SurfDino",
            description="A GUI surfer which uses Grounding Dino and OCR",
            image=f"us-central1-docker.pkg.dev/agentsea-dev/guisurfer/surfdino:{tag}",
            versions={
                "latest": "us-central1-docker.pkg.dev/agentsea-dev/guisurfer/surfdino:latest",
                "dev": "us-central1-docker.pkg.dev/agentsea-dev/guisurfer/surfdino:latest-develop",
            },
            supported_runtimes=["gke"],
            llm_providers=LLMProviders(
                preference=[
                    "gpt-4-vision-preview",
                    "anthropic/claude-3-opus-20240229",
                    "gemini/gemini-pro-vision",
                ]
            ),
            owner_id="patrick.barker@kentauros.ai",
            public=True,
            icon="https://storage.googleapis.com/guisurfer-assets/surf_dino2.webp",
            mem_request="2Gi",
            mem_limit="8Gi",
            cpu_request="2",
            cpu_limit="8",
        )
    except Exception as e:
        print(
            f"failed to create common models: {e} \n this can likely be ignored if they exist"
        )
        return
    print("common models created")


def boot_seq():
    ensure_common_models()
