# Airflow Tutorial




## Introduction

- Airflow is a tool to programmatically define workflows, especially used for data engineering pipelines.  
- The workflows can be defined only using Python at this point.
- The workflows are created as DAGs, so that there is no ambiguity in execution.
- The DAGs can be triggered in the following ways:
  - By definining a schedule to run these on
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
- A sample code is provided in src/dags/scheduled_dag.py
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

