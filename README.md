# Airflow Tutorial

Introduction:

- Airflow is a tool to programmatically define workflows, especially used for data engineering pipelines.  
- The workflows can be defined only using Python at this point.
- The workflows are created as DAGs, so that there is no ambiguity in execution.
- The DAGs can be triggered in the following ways:
  - By definining a schedule to run these on
  - Manually
  - Based on an external trigger. Ex. When data is loaded to a DB
