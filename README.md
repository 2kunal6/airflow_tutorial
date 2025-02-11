# Airflow Tutorial




## Introduction

- Airflow is a tool to programmatically define workflows and it is especially used for data engineering tasks.
- Without Airflow, to create those workflows we would have to write and maintain complex scripts, cron jobs, stored procedures etc.  This complexity will compound if we would have to combine these disparate flows to achieve a single outcome.
- There are many tools we can use to create data pipelines ranging from Temporal to Shell scripts to as far as Jenkins, but Airflow is open-source, flexible, and has a lot of community support.
- Please note that all the sample code referenced here exists in the src folder of this git repo.



## Basic Concepts

- DAG: A DAG is a collection of Tasks that are configured in a Directed Acyclic Graph (DAG) structure.  The DAG structure is important to avoid ambiguity due to circular dependencies among tasks.  Here are a few important features of the dag:
  - retries: it helps us automatically retry in case of temporary failures.
  - schedule: cron value that lets us schedule runs at specified times.
- Task: A single unit of work in an Airflow DAG
  - retries: retrying at task level
- Operators: Operating modules that create a task.  
  - There are lots of Operators available for a wide range of tasks starting from an EmptyOperator (that literally does nothing) to very specific tasks in specific domains like Slack, AWS, Spark etc.



## How to access Airflow?

- We can access Airflow via the Airflow UI or the Command Line Interface.  
- The Airflow UI is simple and intuitive, but at the same time it contains a lot of information like run info (success, failure, execution time, next run time etc.), xcom values passed between tasks, rendered template after evaluating all variables, the graph structure of the dag, task durations, the actual code picked from the airflow's dag location (helpful in case of sync failures etc.), color coded information about status of runs, and many more things.
- In addition to the above, the UI also provides many different functionalities like trigger dag, delete dag, filters etc.  One particularly important functionality is 'clear'.  The clear functionality exists for both dags and tasks, and by clearing we can rerun dags/tasks in case of failures.
- The DAGs can be triggered in the following ways:
  - By defining a schedule to run on.
  - Manually.
  - Based on an external trigger. Ex. When data is loaded to a DB.



## Installation

- A basic non-robust and non-production-grade setup is quite simple using Docker.  
- Please note that you need to install curl and docker before running the following commands and here are the instructions to do that: https://github.com/2kunal6/util/blob/main/installations.txt
```
mkdir airflow_local
cd airflow_local
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.0/docker-compose.yaml'
mkdir -p ./dags ./logs ./plugins ./config
sudo docker compose up airflow-init
sudo docker compose up
```
- It's a good idea to have a local installation done in our personal machines for faster POCs instead of having to go to the cluster each time.

#### Notes
- Please use sudo for the docker command unless docker is configured to work as a non-root user.  Here are more details on that: https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user
- Once this setup is done without any modifications, the Airflow server becomes available at http://localhost:8080
  - Please use username=airflow and password=airflow
- Now simply put your python dag files (which we will create later in this tutorial) into the dags folder created above.  Once we put these dag files in the dags folder created above, they will be available for viewing and running via the Airflow UI.
- To clean up the environment run: sudo docker compose down --volumes --remove-orphans
- More details and other installation methods can be found here in this page https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html


![setup_docker](https://github.com/2kunal6/airflow_tutorial/assets/12296594/76595eaa-3023-4d1f-8d1a-3cb4f708d962)

![login](https://github.com/2kunal6/airflow_tutorial/assets/12296594/ed925bf3-6dfd-40b3-af6d-31e6d6560116)

![home](https://github.com/2kunal6/airflow_tutorial/assets/12296594/9dab61bc-dc91-41bc-9e4d-fccfb38b6b8b)


Now knowing what Airflow is and having set it up, let's write some code.  We will start with simpler concepts and gradually move to more complex ones.  By the end of this tutorial we will write a complete dag which almost resembles a production grade Airflow server in the real world.



## Creating a basic DAG

- To create a basic dag we just need to define the dag (using a constructor) inside a python file along with a task.  A sample code is provided in src/dags/basic_dag.py
- To view and run this dag, we just need to copy this python code in the Airflow server's dags folder.
  - Ex: To make it available in our local Airflow installation, just copy it into the dags folder of the local installation.
```
cp src/dags/basic_dag.py <airflow-local-installation>/dags
```
- After copying, the dag should be visible in the Airflow homepage at http://localhost:8080/home
- Ideally, the dag should be visible momentarily or after a few minutes, but if it takes longer than that simply restart the Airflow docker service to view it immediately.
- Once the dag is visible in the homepage, we can run it by clicking on the "Pause" button in the Actions column.
  
![A_basic_dag](https://github.com/2kunal6/airflow_tutorial/assets/12296594/f8e4294f-6d82-4bb7-a5b0-54880a1b2b8a)

  
- To view more details of the dag and it's run details, we can click on the dag link.  
- In the dag details page we can see many details about the dag run including it's run status (success/failure/running etc.), the run history, the graph of it's task dependencies, the code etc.
  
  ![Dag_details](https://github.com/2kunal6/airflow_tutorial/assets/12296594/6b15d194-56ec-4b69-af55-8d591be9cfe2)

- default_args: Configuration values that we can pass to the DAG constructor so that it can be passed to each task's constructor. 

## Operators
- There are a large number of operators available provided out of the box both from Airflow and third-parties that can be used to accomplish different kind of tasks.  Apart from that we can also write our own operators with custom logic to achieve specific use-cases.  Having the ability to write our own operators makes Airflow very flexible.
- Here is a non-exhaustive list of the some important opearators grouped by providers: https://registry.astronomer.io/modules?typeName=Operators&limit=24&sorts=updatedAt%3Adesc
- Going through that entire list can be daunting.  Here's a list of some important operators that we use quite frequently:
  - PythonOperator: To run Python code
  - BashOperator: To run bash commands
  - LivyOperator: To run Spark code
- How to create a custom operator: https://airflow.apache.org/docs/apache-airflow/stable/howto/custom-operator.html


## Creating a basic DAG with schedule

- Scheduled dags are dags that run automatically at the defined schedule.  This important feature is the reason why Airflow is so popular.  Instead of writing and maintaining our own scheduling logic, we can simply rely on Airflow to do this for us reliably.
- Sample code: src/dags/scheduled_dag.py
- Notes:
  - start_date parameter is the time from which the dag should run and is a compulsory parameter.
  - After creating a scheduled dag we need to trigger it manually the first time.
  - use catch_up=False if you do not want to run the dag from the start_date, otherwise the dag will start running from the start_date to the present time. 
  - The dag only runs after the current interval is over.
    - Ex. If a dag is scheduled to run everyday at 9 am, and it is scheduled to start from today, then it will wait for the interval to end.  And therefore it will only run tomorrow at 9 am.
      - The image below (for code src/dags/scheduled_daily_dag.py) shows that the run is scheduled at 10:10 am but it did not run at that time. It will only run at 10:10 am the next day.  The only run presented there is the manually triggered one.

![next_inteval_run](https://github.com/2kunal6/airflow_tutorial/assets/12296594/63958f64-1dc6-4627-a86c-57aeecc946ff)

  - It is a good idea to schedule the dags based on UTC, so that it is more consistent with other external dependencies like Spark servers, monitoring systems, external dependencies to other dags etc. 
  - It is important to make the code (which is called by the DAG's task) idempotent, so that unintended reruns do not dirty the data.



## Creating a DAG that takes parameters

- Being able to pass parameters is useful when we want to run dags manually for testing for example.
- Sample code: src/dags/parameterized_dag.py
- Notes
  - We can pass the runtime config through a UI form or via Airflow CLI.
  - The default values provided will be overriden by user passed parameter values.
  - The sample code shows all the 4 ways to access the parameters, namely params, jinja, context, kwargs



## Passing Admin Variables

- The parameters mentioned above are passed to a DAG and only applicable to that particular dag but Admin variables applies to all dags in an Airflow cluster.  We can use it to set parameters that affects all dags like the run environment (dev/uat/prod).
- To set these Admin Variables we need to put the key-value pairs inside Admin -> Variables.  The Admin menu is present in the main menu towards the top. 
- Sample code:
  - src/dags/admin_variables_dag.py
  - src/config/config.yaml -> to be copied to <airflow-installation-root-directory>/config
  - src/dags/util/load_config.py
  - The dags and config folders can be directly copied to the local Airflow installation location mentioned above.  Please note the folders which are in the system path.
```
sudo rm -rf <airflow-installation-root-directory>/dags <airflow-installation-root-directory>/config 
cp -r airflow_tutorial/src/* <airflow-installation-root-directory>
```
- We can tune these locations as per our taste.



## xcom (cross-communication) and task-graph

- Task graph is the directed acyclic graph of tasks.  This directed structure tells us the order in which the tasks will run.  The dependent tasks run only after the predecessors have finished running\*.
- Different tasks in a DAG can share information with each other during the DAG runs, and to achieve this Airflow provides a concept call xcom using which we can push and pull key-value pairs.
- Sample code: src/dags/xcom_dag.py
- Notes:
  - This code also shows the syntax to make task dependencies.  The syntax to make task2 dependent on task1 (i.e. task2 runs only after task1 finishes) task1 >> task2
  - \* We can further control this to have one or all predecessors finish before the dependent runs.  Controls are also available to define the finish-states after which the dependents will start (ex. run dependents only successful runs of predecessors).



## External Sensors

- Whereas xcom helps tasks within a dag to communicate, External Sensors helps tasks across dags to communicate.
- This can be helpful in situations where we can't put dependent tasks inside a different dag (for example when those tasks are managed by different teams).
- Sample code:
  - src/dags/external_sensor_callee_dag.py
  - src/dags/external_sensor_caller_dag.py
- Please note that managing External Sensors could be a bit tricky due to several factors like wait times in queue, execution date, start date etc.  Therefore instead of using this we can also think about maintaining a persistent metadata table for runs which can also act as a log table.



## Accessing runtime parameters

- The Airflow UI provides a lot of information about the run status of dags but it is also important to access those information via code so that we can troubleshoot in runtime or automatically if required.
- This can be useful for example to send alerts in case of run failures (discussed later).
- Sample code: src/dags/accessing_parameters_dag.py
- Here's a non-exhaustive list of accessible variables both at dag and task level: https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html



## A Complete DAG

- More or less we have learnt all the concepts that we need to create a simple Airflow app that is almost production grade.  So let's bring all these concepts together, and write a complete dag.
- Sample Code: src/dags/complete_lifecycle_dag.py
- Understanding the code bit by bit:
  - The Config File:
    - This dag builds from a config file src/config/application_config.yaml which defines all dags and corresponding tasks.
    - At the top level we have created 2 types of dags - short and long-running ones.  This is just to show how we can create multiple dags using the same code (to avoid code duplication).  Creating dags in this fashion is called dynamic dag creation.  
    - *This is a common phenomenon in the real world where some tasks take longer than others.  In these situations we can start the long-running tasks only after the shorter ones finishes, so that we don't overwhelm the queue and make data available as soon as we can.
    - In this design we have clubbed the tasks inside one dag.  The other option would have been to create separate dags for each task.
      - Both these designs have their pros and cons, but keeping all tasks in one dag makes it a bit more scalable (because we can simply add more tasks to the config) and all tasks are readily available in a single page to view/rerun.
  - The Task Script:
    - The sample query provided in the load_data() function shows a sample script and gives a generic idea on how to make the runs idempotent.  To make the runs idempotent we basically check if the run already happened on a particular day, and proceed iff that didn't.  
    - Similarly, to handle partial runs we persist run log info only after complete successful runs.  We also need to delete/override all incomplete data to avoid dupes in case of partial runs.
  - Monitoring:
    - The send_metrics_task sends metrics to a monitoring system like Grafana.
    - We can then set alerts in the monitoring system to alert us for failures and unfinished runs.
    - trigger_rule = 'all_done' tells the task to run it only when all the upstream tasks have finished running
  - Data Quality Checks:
    - Data Quality checks are important to ensure that the Airflow jobs are running fine both from a technical pass/fail point of view and from a business point of view. 
    - The Data Quality check jobs can be called after the job runs finish.
    - Data Quality checks can range from simple count checks, to checking non-null values, to complicated ones like checking for outliers etc. using ML algorithms.



## Some Practical Tips

- It's a good idea to run the dev/uat dags a few hours before prod if possible, so that we can detect problems early hand if any.
- On a similar note, for dev or uat we do not need to load the entire data if that's expensive.  We just have to see if there's any change that might result in a bad data load.  Therefore it's enough to load some subset of the data.  The complete_lifecycle_dag shows an example on how to achieve that using limit conditionally.
- It's a good idea to use execution_date to load data for a particular day because it is more consistent compared to other variables, even when runs do not happen.
- At times our dags might not completely and successfully run.  In those cases we might have to run only a subset of tasks that failed.  To achieve that here are a few ideas:
    - Use the clear button to clear only tasks that we wish to run.
    - For dates which are not visible in the UI, we can pass the date as parameter.  But doing that will run all the tasks.  Therefore we need to make the tasks idempotent. 
    - If at all we want to write a feature to run only a subset of tasks for a particular date, then we can simply pass the subset of tasks we wish to run, and parse it in an upstream operator (upstream operator for an operator is the one which runs before this operator).  We can then just run a dummy query for the tasks not required to run.
- For tasks calling costly jobs like Spark we might want to limit the number of jobs we request to not overwhelm the system/queue.  This can be handled by setting max_active_tasks which limits the maximum number of job requests a dag can make via tasks.
    - Please note that this is different from max_active_runs which says the number of dag runs itself that can be active. 
    - It's generally a good idea to set max_active_runs=1, so that we run only one dag at a time to avoid confusion.


## Airflow Architecture
- Scheduler: It continuously scans the dags directory to schedule tasks based on their dependencies and schedule. It interacts with the metadata database to store and retrieve task state and execution information.
- Metadata DB: It stores DAGs, task status, execution history etc., typically using MySQL or Postgres.  It also helps Airflow recover from crash by using the persistent state.
- WebServer: A Flask-based web interface for monitoring DAGs, viewing logs, and manually triggering jobs.  It also displays information from the Metadata server.
- Executors: It allocates resources and runs tasks.  Types:
    - LocalExecutor – Runs tasks in parallel on a single machine.
    - CeleryExecutor – Distributes tasks across multiple worker nodes using Celery and Redis/RabbitMQ.
    - KubernetesExecutor – Dynamically creates Kubernetes pods for each task, providing scalability. 
- Worker Nodes: Executes the task by reading the code from the Metadata DB.
- Message Broker: Redis or RabbitMQ is used for task queuing.  The Scheduler sends tasks to the broker, and workers pick them up.



