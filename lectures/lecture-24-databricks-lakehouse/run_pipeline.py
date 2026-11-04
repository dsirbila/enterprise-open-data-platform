from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import NotebookTask, Task

w = WorkspaceClient()  # კითხულობს ავტორიზაციას ~/.databrickscfg-იდან

run = w.jobs.submit(
    run_name="eodp-medallion-run",
    tasks=[
        Task(
            task_key="bronze_silver_gold",
            notebook_task=NotebookTask(
                notebook_path="/Workspace/Repos/dsirbila/enterprise-open-data-platform/lectures/lecture-24-databricks-lakehouse/lab-24-medallion"
            ),
        )
    ],
).result()

print(f"Run დასრულდა სტატუსით: {run.state.result_state}")