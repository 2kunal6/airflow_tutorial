# Airflow Tutorial




## Introduction

- Airflow is a tool to programmatically define workflows, especially used for data engineering pipelines.
- Without Airflow, to achieve the same, we would have to write and maintain complex shell/python scripts, cron job logic, DB stored procedures etc.  This complexity would have been compounded if we would have to orchestrate these disparate flows to achieve a single outcome.
- There are a lot many tools we can use to create data pipelines ranging form Temporal to shell scripts to as far as Jenkins, but Airflow is open-source, flexible, and has a lot of community support.
- These are a few important concepts in Airflow:
  - DAG: Collection of Tasks that are configured in a Directed Acyclic Graph (DAG) structure.  The DAG structure is important to avoid circular dependencies among tasks.  Here are a few features of the dag:
    - retries: help us retry in case of dag-run failure to overcome temporary problems like server going down for sometime.
    - schedule: cron value that lets us schedule runs at a complex level like daily, weekly, at particular timings etc.
  - Task: A single unit of work in an Airflow DAG
    - retries: retrying at task level
  - Operators: Collection of operating modules that create a task.  
    - There are an ocean of Operators available to achieve a range of tasks starting with an EmptyOperator that literally does nothing, to ranging to specific tasks in specific domains like Slack, AWS, Spark etc.
    - This is further discussed in detail in a later topic.
- The DAGs can be triggered in the following ways:
  - By defining a schedule to run these on
  - Manually
  - Based on an external trigger. Ex. When data is loaded to a DB



## Installation

A basic non-robust and non-production-grade setup is quite simple using Docker via the following simple commands:
Note: You need to install curl and docker before running the following commands.  Here are the instructions to do that: https://github.com/2kunal6/util/blob/main/installations.txt
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.0/docker-compose.yaml'
mkdir -p ./dags ./logs ./plugins ./config
sudo docker compose up airflow-init
sudo docker compose up
```

#### Notes
- Please use sudo for the docker command unless docker is configured to work as a non-root user.  More details here: https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user
- Without any modifications, you can view/manage the Airflow server now via http://localhost:8080
  - Please use username=airflow and password=airflow
- Now simply put your python dag files (which we will create subsequently) into the dags folder created above, and you will be able to view and run your dags.
- To clean up the environment run: sudo docker compose down --volumes --remove-orphans
- More details and other installation methods can be found here in this page https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

#### Why local installation?
It's a good idea to have a local installation done in our personal machines for faster POCs, although in the real world we will have to dedicate a cluster for Airflow for high availability and sharing.
- Local installation helps in faster POCs because with dedicated servers connected to production data it's easy to go wrong, or choke Spark servers if it's used to invoke Spark, if we are not careful.
- Moreover, if Airflow is hosted in AWS, then there would be some wait time for the code sync to happen through CI/CD to the S3 location from where the MWAA picks up for example.
- It also helps the team working on the same repo to not have to work through experimental changes.  We can commit only after a certain level of confidence in the code.


![setup_docker](https://github.com/2kunal6/airflow_tutorial/assets/12296594/76595eaa-3023-4d1f-8d1a-3cb4f708d962)

![login](https://github.com/2kunal6/airflow_tutorial/assets/12296594/ed925bf3-6dfd-40b3-af6d-31e6d6560116)

![home](https://github.com/2kunal6/airflow_tutorial/assets/12296594/9dab61bc-dc91-41bc-9e4d-fccfb38b6b8b)



## Creating a basic DAG

- To create a dag we just need to define a dag with a task along with the imports.  A sample code is provided in src/dags/basic_dag.py
- To view and run this dag, we just need to copy this python code with the DAG definition in the Airflow server's dags folder.
  - ex. To make it available in our local Airflow installation, just copy it into the dags folder of the local installation.
```
cp src/dags/basic_dag.py <airflow-local-installation>/dags
```
- After copying, the dag should be visible in the Airflow homepage at http://localhost:8080/home
- Ideally, the dag should be visible momentarily or after a few minutes of delay, but if it takes longer than that, then we can simply restart the Airflow docker service to view it immediately.
- Once the dag is visible in the homepage, we can run it by clicking on the "Pause" button in the Actions column.
  
![A_basic_dag](https://github.com/2kunal6/airflow_tutorial/assets/12296594/f8e4294f-6d82-4bb7-a5b0-54880a1b2b8a)

  
- To view more details of the dag and it's run details, we can click on the dag link.  
- In the dag details page we can see many details about the dag run including it's run status (success/failure/running etc.), the run history, the graph of it's task dependencies, the code etc.
  
  ![Dag_details](https://github.com/2kunal6/airflow_tutorial/assets/12296594/6b15d194-56ec-4b69-af55-8d591be9cfe2)




## Creating a basic DAG with schedule
- Sample code: src/dags/scheduled_dag.py
- Notes:
  - start_date parameter is necessary, and it tells us the time from which the dag should run.
  - After creating a scheduled dag we need to trigger it manually the first time.
  - use catch_up=False if you do not want to run the dag from the start_date, otherwise the dag will start running from the start_date to the present time. 
  - The dag only runs after the current interval is over.
    - Ex. If a dag is scheduled to run everyday at 9 am, and it is scheduled to start from today, then it will wait for the interval to end.  And therefore it will only run tomorrow at 9 am.
      - The image below (for code src/dags/scheduled_daily_dag.py) shows that the run is scheduled at 10:10 am but it did not run at that time. It will only run at 10:10 am the next day.  The only run presented there is the manually triggered one.

![next_inteval_run](https://github.com/2kunal6/airflow_tutorial/assets/12296594/63958f64-1dc6-4627-a86c-57aeecc946ff)

  - It is a good idea to schedule the dags based on UTC, so that it is more consistent with other external dependencies like Spark servers, monitoring systems, external dependencies to other dags etc. because otherwise it gets confusing when daylight savings go on or off. 
  - It is important to make the code (which is called by the DAG) idempotent, so that if by mistake the code runs twice, it does not dirty the data, especially in production.




## xcom and task-graph
- Sample code: src/dags/xcom_dag.py
- Notes:
  - This code shows the syntax to make task dependencies.  It can be done like this: task1 >> task2
  - This code also shows xcom, which is allows talking among tasks.
  - This can be helpful for example to parse and share the parameters passed to the dag at one place.  All the dependent tasks can pull from the same task, thus following the Don't-Repeat-Yourself principle.




## Creating a DAG that takes parameters
- Sample code: src/dags/parameterized_dag.py
- Notes
  - It helps us provide runtime config through a UI form.
  - The default values provided will be overriden by user passed params through the UI.
  - Passing parameters could be helpful when we need manual runs in case of bad runs, to run adhoc scripts to create/update/delete from tables, or simply for testing.
  - The sample code shows all the 4 methods that we can use to access the parameters namely: params, jinja, context, kwargs




## Passing Admin Variables
- Sample code:
  - src/dags/admin_variables_dag.py
  - src/config/config.yaml -> to be copied to <airflow-installation-root-directory>/config
  - src/dags/util/load_config.py
  - The dags and config folders can be directly copied to <airflow-installation-root-directory>.  Please note the folders which are in the system path.
```
sudo rm -rf <airflow-installation-root-directory>/dags <airflow-installation-root-directory>/config 
cp -r airflow_tutorial/src/* <airflow-installation-root-directory>
```
  - We can tune these locations as per our taste.
- Notes 
  - Please note that admin variables can be accessed by all dags, whereas dag level parameters (which we pass from the UI) is available only to that particular dag from which that trigger was made.
  - The admin variables can help us pick environment (dev/qa/uat/prod) related config, as shown in the code.




## External Sensors
- Sample code:
  - src/dags/external_sensor_callee_dag.py
  - src/dags/external_sensor_caller_dag.py
- Notes:
  - This helps us to start a dag run only when a different dag run finishes.
  - This can be used in situations in which for example a task makes the data available, and the downstream task needs to operate on that data only when it's completely available.
  - Managing External Sensors could be a bit tricky given wait times in queue, considering execution date and start date etc.  We can also maintain a persistent metadata table for runs, which can also store more metadata information like the config, state etc. of the callee service (like Spark).




## Accessing Parameters
- Sample code:
  - src/dags/accessing_parameters_dag.py
- Notes:
  - A number of dag and task level details, along with their run level details are available and can be accessed.
  - Accessing these variables within the code can help us write our logic based on these parameters.
  - A non-exhaustive list of accessible variables can be found here: https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html
  - Ex 1. We can check inside code if all the tasks have finished running, and only then send the status of all the tasks for monitoring (discussed later).
  - Ex 2. In case the dag failed to run on a given date because of Airflow going down, we can use the execution_date to run for that particular date.




## Operators
- There are a large number of operators available, both from Airflow and third-party ones, that can be used to accomplish different kind of tasks.
- Here is a non-exhaustive list of the same grouped by providers: https://registry.astronomer.io/modules?typeName=Operators&limit=24&sorts=updatedAt%3Adesc
- It's generally a good idea to use as few operators as possible to keep the application simple.  Here's a list of operators in order of importance (arguably):
  - PythonOperator: To run Python code
  - LivyOperator: To interact with the Spark cluster over REST APIs
  - BashOperator: We can instead use python commands like os.system or suprocess to run the bash commands
