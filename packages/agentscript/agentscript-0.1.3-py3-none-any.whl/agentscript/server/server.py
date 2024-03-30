import logging

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    InvocationModel,
    InvocationsModel,
    ExecModel,
    ExecsModel,
)
from ..interpreter_old import Execution, Invocation, Interpreter

app = FastAPI()

logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log the request details
    logging.info(f"Method: {request.method} Path: {request.url.path}")
    response = await call_next(request)
    return response


@app.get("/")
async def root():
    return {"message": "Agentscript server"}


@app.get("/health")
async def health():
    return {"status": "ok"}


# TODO: this should be its own project, an agent tracker
@app.get("/invocations", response_model=InvocationsModel)
async def get_invocations():
    invocations = Invocation.find()
    return InvocationsModel(
        invocations=[invocation.to_schema() for invocation in invocations]
    )


@app.get("/invocations/{id}", response_model=InvocationModel)
async def get_invocation(id: str):
    invocation = Invocation.find(id=id)
    if len(invocation) != 1:
        raise HTTPException(status_code=404, detail="Invocation not found")
    return invocation[0].to_schema()


@app.post("/execute", response_model=ExecModel)
async def execute(msg: str):
    execution: Execution = Interpreter.execute(msg)
    return execution.to_schema()


@app.get("/executions", response_model=InvocationsModel)
async def get_executions():
    executions = Execution.find()
    return ExecsModel(executions=[execution.to_schema() for execution in executions])


@app.get("/executions/{id}", response_model=ExecModel)
async def get_execution(id: str):
    execution = Execution.find(id=id)
    if len(execution) != 1:
        raise HTTPException(status_code=404, detail="Invocation not found")
    return execution[0].to_schema()
