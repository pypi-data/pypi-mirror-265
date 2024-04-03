from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    Depends,
    APIRouter,
    HTTPException,
    Query,
)
from typing import Annotated, List

from agentdesk import Desktop
from agentdesk.vm import DesktopVM
from agentdesk.vm.load import load_provider
from threadmem import RoleModel


from guisurfer.server.models import (
    V1UserProfile,
    AgentModel,
    AgentsModel,
    CreateAgentModel,
    AgentTypeModel,
    AgentTypesModel,
    CreateAgentTypeModel,
    TasksModel,
    GCEProviderOptions,
    EC2ProviderOptions,
    LogsModel,
    LLMProviderModel,
)
from guisurfer.agent.runtime import AgentRuntime
from guisurfer.auth.transport import get_current_user
from guisurfer.server.runtime import DesktopRuntime
from guisurfer.agent.base import TaskAgentInstance
from guisurfer.agent.types import AgentType
from guisurfer.agent.llm import LLMProvider
from guisurfer.agent.models import SolveTaskModel
from guisurfer.job.agent.k8s import CreateAgentJobK8s, RestartAgentJobK8s
from guisurfer.server.hub import Hub
from guisurfer.server.key import SSHKeyPair
from guisurfer.agent.task import Task

router = APIRouter()


@router.post("/v1/agents", response_model=AgentModel)
async def create_agent(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    data: CreateAgentModel,
):
    print("\n!creating agent with model: ", data)
    print("\n!validating data...")
    if data.desktop:
        desktop_vms = Desktop.find(
            name=data.desktop.lower(), owner_id=current_user.email
        )
        if not desktop_vms:
            print("\n!no desktop vms")
            raise HTTPException(
                status_code=404, detail=f"Desktop {data.desktop} not found"
            )

    elif data.desktop_request:
        print("\n!finding desktop for user...")
        desktop_runtimes = DesktopRuntime.find_for_user(
            name=data.desktop_request.runtime, user_id=current_user.email
        )
        print("\n!found desktop runtimes: ", desktop_runtimes)
        if not desktop_runtimes:
            print("\n!no desktop runtimes")
            raise HTTPException(
                status_code=404,
                detail=f"DesktopRuntime {data.desktop_request.runtime} not found",
            )

    else:
        print("\ndesktop or desktop runtime not found")
        raise HTTPException(
            status_code=400, detail="desktop or desktop_runtime is required"
        )

    print("\n!finding agent runtime...")
    agent_runtimes = AgentRuntime.find_for_user(
        name=data.runtime, user_id=current_user.email
    )
    print("\nagnet runtimes: ", agent_runtimes)
    if not agent_runtimes:
        print("\nno agent runtimes!")
        raise HTTPException(
            status_code=404, detail=f"AgentRuntime {data.runtime} not found"
        )

    print("\n!finding agent type...")
    agent_types = AgentType.find_for_user(name=data.type, user_id=current_user.email)
    print("\nagent types: ", agent_types)
    if not agent_types:
        print("\n!no agent types")
        raise HTTPException(status_code=404, detail=f"AgentType {data.type} not found")
    agent_type = agent_types[0]

    print("\n!getting api key for agent...")
    hub = Hub()
    api_key = hub.get_api_key(current_user.token)

    print("\n!creating agent instance...")
    instance = TaskAgentInstance(
        runtime=data.runtime,
        type=data.type,
        desktop=data.desktop,
        name=data.name,
        owner_id=current_user.email,
        icon=data.icon if data.icon else agent_type.icon,
    )
    print("\n!Creating agent job...")
    job = CreateAgentJobK8s()
    job.create_agent(data=data, owner=current_user, api_key=api_key)
    print("\n!started create agent job")

    instance.refresh()
    return instance.to_schema()


@router.get("/v1/agents", response_model=AgentsModel)
async def get_agents(current_user: Annotated[V1UserProfile, Depends(get_current_user)]):
    agents = TaskAgentInstance.find(owner_id=current_user.email)
    return AgentsModel(agents=[agent.to_schema() for agent in agents])


@router.get("/v1/agents/{name}", response_model=AgentModel)
async def get_agent(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    agent: List[TaskAgentInstance] = TaskAgentInstance.find(
        name=name, owner_id=current_user.email
    )
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent[0].to_schema()


@router.delete("/v1/agents/{name}")
async def delete_agent(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    print(f"\n!!!deleting agent {name}...")
    try:
        task_agents = TaskAgentInstance.find(name=name, owner_id=current_user.email)
        if not task_agents:
            raise HTTPException(status_code=404, detail="Agent not found")
        task_agent = task_agents[0]
        print("task_agent: ", task_agent)
        task_agent.status = "deleting"
        task_agent.save()

        runtimes = AgentRuntime.find_for_user(
            name=task_agent.runtime, user_id=current_user.email
        )
        if not runtimes:
            raise HTTPException(status_code=404, detail="AgentRuntime not found")
        runtime = runtimes[0]
        print("runtime: ", runtime)

        print("\n!!deleting running agent...")
        runtime.delete_agent(name)
        print("\n!!deleted running agent")
    except Exception as e:
        print("\n!!error deleting agent: ", e)
        raise

    if task_agent.desktop:
        print("\n!!deleting desktop...")
        desktops = DesktopVM.find(
            name=task_agent.desktop.lower(), owner_id=current_user.email
        )
        if not desktops:
            raise HTTPException(status_code=404, detail="Desktop not found")
        desktop = desktops[0]

        runtime_name = desktop.metadata["runtime_name"]
        print(f"\n!!finding runtime {runtime_name}...")
        # TODO: yuck
        desktop_runtimes = DesktopRuntime.find_for_user(
            name=runtime_name, user_id=current_user.email
        )
        desktop_runtime = desktop_runtimes[0]
        print(f"\n!!found runtime, deleting vm with provider {desktop.provider}...")
        try:
            if desktop.provider.type == "gce":
                opts = GCEProviderOptions(
                    zone=desktop.metadata["zone"], region=desktop.metadata["region"]
                )
                desktop_runtime.delete_vm(
                    desktop.name, current_user.email, gce_opts=opts
                )
            elif desktop.provider.type == "ec2":
                opts = EC2ProviderOptions(region=desktop.metadata["region"])
                desktop_runtime.delete_vm(
                    desktop.name, current_user.email, ec2_opts=opts
                )
            else:
                raise HTTPException(status_code=404, detail="Provider not found")
            print("\n!!deleted desktop!")
        except Exception as e:
            print("\n!!error deleting desktop: ", e)

        try:
            ssh_keys = SSHKeyPair.find(
                owner_id=current_user.email, public_key=desktop.ssh_key
            )
            print("\n!!ssh keys: ", ssh_keys)
            if ssh_keys:
                print("\n!!found ssh keys to delete")
                ssh_key = ssh_keys[0]
                ssh_key.delete(ssh_key.name, ssh_key.owner_id)
                print("\n!!deleted ssh key")
        except Exception as e:
            print("\n!!error deleting ssh key: ", e)
    else:
        print("\n!!no desktop to delete")

    print("\n!!deleting agent record...")
    try:
        TaskAgentInstance.delete(id=task_agent.id)
    except Exception as e:
        print("\n!!error deleting agent record: ", e)


@router.post("/v1/agents/{name}/stop")
async def stop_agent(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    print("\n!stopping agent...")
    try:
        task_agents = TaskAgentInstance.find(name=name, owner_id=current_user.email)
        if not task_agents:
            raise HTTPException(status_code=404, detail="Agent not found")
        task_agent = task_agents[0]
        print("task_agent: ", task_agent)
        task_agent.status = "stopped"
        task_agent.save()

        runtimes = AgentRuntime.find_for_user(
            name=task_agent.runtime, user_id=current_user.email
        )
        if not runtimes:
            raise HTTPException(status_code=404, detail="AgentRuntime not found")
        runtime = runtimes[0]
        print("runtime: ", runtime)

        print("\n!!stop - deleting running agent...")
        runtime.delete_agent(name, delete_secret=False)
        print("\n!!stop - deleted running agent")
    except Exception as e:
        print("\n!!stop - error deleting agent: ", e)
        raise
    print("\n!stopped running agent")

    if task_agent.desktop:
        print("\n!stopping desktop...")
        desktops = DesktopVM.find(
            name=task_agent.desktop.lower(), owner_id=current_user.email
        )
        if not desktops:
            raise HTTPException(status_code=404, detail="Desktop not found")
        desktop = desktops[0]
        runtime_name = desktop.metadata["runtime_name"]
        print(f"\n!!finding runtime {runtime_name}...")
        # TODO: yuck
        desktop_runtimes = DesktopRuntime.find_for_user(
            name=runtime_name, user_id=current_user.email
        )
        desktop_runtime = desktop_runtimes[0]
        print(f"\n!!found runtime, stopping vm with provider {desktop.provider}...")
        try:
            if desktop.provider.type == "gce":
                opts = GCEProviderOptions(
                    zone=desktop.metadata["zone"], region=desktop.metadata["region"]
                )
                desktop_runtime.stop_vm(desktop.name, current_user.email, gce_opts=opts)
            elif desktop.provider.type == "ec2":
                opts = EC2ProviderOptions(region=desktop.metadata["region"])
                desktop_runtime.stop_vm(desktop.name, current_user.email, ec2_opts=opts)
            else:
                raise HTTPException(status_code=404, detail="Provider not found")
            print("\n!!stopped desktop!")
        except Exception as e:
            print("\n!!error stopping desktop: ", e)

        print("stopped desktop")


@router.post("/v1/agents/{name}/start")
async def start_agent(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    print(f"restarting agent {name}...")
    task_agents = TaskAgentInstance.find(name=name, owner_id=current_user.email)
    if not task_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    task_agent = task_agents[0]
    print("found task agent: ", task_agent.__dict__)
    task_agent.status = "restarting"
    task_agent.create_job_id = None
    task_agent.save()
    print("validating data...")
    if task_agent.desktop:
        desktop_vms = Desktop.find(
            name=task_agent.desktop.lower(), owner_id=current_user.email
        )
        if not desktop_vms:
            raise HTTPException(
                status_code=404, detail=f"Desktop {task_agent.desktop} not found"
            )
    else:
        raise HTTPException(status_code=400, detail="desktop is required")

    agent_runtimes = AgentRuntime.find_for_user(
        name=task_agent.runtime, user_id=current_user.email
    )
    if not agent_runtimes:
        raise HTTPException(
            status_code=404, detail=f"AgentRuntime {task_agent.runtime} not found"
        )

    print("getting api key for agent...")
    hub = Hub()
    api_key = hub.get_api_key(current_user.token)

    print("Creating agent job...")
    job = RestartAgentJobK8s()
    job.restart_agent(name=name, owner=current_user, api_key=api_key)
    print("started create agent job")

    task_agent.refresh()
    return task_agent.to_schema()


@router.post("/v1/agents/{name}/tasks")
async def solve_task(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    name: str,
    task_model: SolveTaskModel,
):
    print("finding agent...")
    task_agents = TaskAgentInstance.find(name=name, owner_id=current_user.email)
    if not task_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    task_agent = task_agents[0]

    print("finding runtime")
    runtimes = AgentRuntime.find_for_user(
        name=task_agent.runtime, user_id=current_user.email
    )
    if not runtimes:
        raise HTTPException(status_code=404, detail="Runtime not found")
    runtime = runtimes[0]

    print("finding task...")
    found_task = Task.find(id=task_model.task.id, owner_id=current_user.email)
    if not found_task:
        print("creating task...")
        task = Task.from_schema(task_model.task, current_user.email)
        task.save()
        task.thread.add_role(
            RoleModel(
                name="assistant",
                user_id=task_agent.id,
                user_name=task_agent.name,
                icon=task_agent.icon,
            )
        )
        task.thread.add_role(
            RoleModel(
                name="user",
                user_id=current_user.email,
                user_name=current_user.handle,
                icon=current_user.picture,
            )
        )
        print("created task")
    else:
        task = found_task[0]

    task.assigned_to = task_agent.name
    task.save()
    task_model.task = task.to_schema()

    print("telling agent to start task...")
    runtime.call(name, "/v1/tasks", "POST", task_model.model_dump())
    print("agent started task")

    return


@router.get("/v1/agents/{name}/tasks", response_model=TasksModel)
async def get_tasks(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    name: str,
):
    print("finding agent...")
    task_agents = TaskAgentInstance.find(name=name, owner_id=current_user.email)
    if not task_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    task_agent = task_agents[0]

    print("finding task...")
    found_tasks = Task.find(assigned_to=name, owner_id=current_user.email)
    if not found_tasks:
        return TasksModel(tasks=[])

    return TasksModel(tasks=[task.to_schema() for task in found_tasks])


@router.get("/v1/agents/{name}/logs", response_model=LogsModel)
async def get_pod_logs(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    name: str,
    tail_lines: int = Query(1000),
):
    print("Fetching logs...")

    print("Finding agent...")
    task_agents = TaskAgentInstance.find(name=name, owner_id=current_user.email)
    if not task_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    task_agent = task_agents[0]

    print("Finding runtime...")
    runtimes = AgentRuntime.find_for_user(
        name=task_agent.runtime, user_id=current_user.email
    )
    if not runtimes:
        raise HTTPException(status_code=404, detail="Runtime not found")
    runtime = runtimes[0]

    # Fetch logs from the Kubernetes pod
    print("Fetching logs from Kubernetes pod...")
    try:
        logs = runtime.get_kubernetes_pod_logs(
            task_agent.name.lower(), tail_lines=tail_lines
        )
        return LogsModel(logs=logs)
    except Exception as e:
        print(f"An error occurred while fetching pod logs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch logs: {e}")


@router.websocket("/ws/agents/{name}/logs")
async def stream_logs_websocket(
    websocket: WebSocket,
    name: str,
    token: str = Query(...),
):
    print("\nKWS connecting...")
    current_user = await get_current_user(token)
    await websocket.accept()
    print("\nKWS accepted")
    try:
        print("\nKWS finding agent...")
        task_agents = TaskAgentInstance.find(name=name, owner_id=current_user.email)
        if not task_agents:
            raise HTTPException(status_code=404, detail="Agent not found")
        task_agent = task_agents[0]

        print("\nKWS finding runtime")
        runtimes = AgentRuntime.find_for_user(
            name=task_agent.runtime, user_id=current_user.email
        )
        if not runtimes:
            raise HTTPException(status_code=404, detail="Runtime not found")
        runtime = runtimes[0]
        if not runtime:
            await websocket.send_text("AgentRuntime not found.")
            await websocket.close(code=1002)
            return

        # Stream logs from the specified pod to the client
        print("\nKWS streaming logs...")
        await runtime.stream_kubernetes_pod_logs(name, websocket)
    except WebSocketDisconnect:
        print(f"\nKWebSocket disconnected for pod {name}")
    except Exception as e:
        print(f"\nKWS An error occurred: {e}")
        await websocket.close(code=1011)


@router.post("/v1/agenttypes", response_model=AgentTypeModel)
async def create_types(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    data: CreateAgentTypeModel,
):
    agent = AgentType(
        name=data.name,
        owner_id=current_user.email,
        description=data.description,
        image=data.image,
        env_opts=data.env_opts,
        supported_runtimes=data.supported_runtimes,
        public=data.public,
    )
    return agent.to_schema()


@router.get("/v1/agenttypes", response_model=AgentTypesModel)
async def get_types(current_user: Annotated[V1UserProfile, Depends(get_current_user)]):
    user_types = AgentType.find_for_user(user_id=current_user.email)
    return AgentTypesModel(types=[agent.to_schema() for agent in user_types])


@router.get("/v1/agenttypes/{name}", response_model=AgentTypeModel)
async def get_type(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    agents = AgentType.find_for_user(name=name, user_id=current_user.email)

    if not agents:
        raise HTTPException(status_code=404, detail="Agent type not found")

    return agents[0].to_schema()


@router.delete("/v1/agenttypes/{name}")
async def delete_type(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    AgentType.delete(name=name, owner_id=current_user.email)
    return


@router.get("/v1/llmproviders", response_model=LLMProviderModel)
async def get_llm_providers(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
):
    opts = LLMProvider.all_opts()
    return LLMProviderModel(options=opts)
