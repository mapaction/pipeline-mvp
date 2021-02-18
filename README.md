# Pipeline MVP

MVP project for Airflow-based scheduling of data pipeline processing for MapAction. This repository is used for local development and for running in GCP.


## Structure

`/dags`

Folder with the DAG scripts, every DAG instance in the global namespace will be available inside Airflow.

`/plugins`

Folder with the `pipeline_plugin` that contains the custom operators and the domain logic.

`/scripts`

Scripts to automate setting up the environment for local development.

`/data`

Empty folder that is mounted in the local Docker container so that any data generated by the dags is also available in the local environment.

`/requirements.txt`

Python packages required for development in your IDE.

`/requirements-airflow.txt`

Python packages that need to be available in the Airflow server. These significantly increase startup time of your local Airflow server.

## Local development

### Requirements

Docker is a dependency for running a local version of Airflow.

### Initial setup

To create a virtual environment for local development, run the following from the root folder:

`source ./scripts/setup_environment.sh`

When you add new dependencies, rerun this command to install the new dependencies in your virtual environment.

### Development

To start the Airflow server, run the following from the root folder:

`sh ./start_airflow.sh`

The Airflow server runs in a Docker container, which has the `/dags`, `/plugins` and `/data` folders mounted in there, together with the `requirements-airflow.txt` file. When starting the container, these requirements are installed. The `/data` folder is accessible from `/opt/data` folder inside the Airflow server/worker. The `/dags` folder contains all the dags and is automatically synchronized, while the `/plugins` folder contains the plugins including all the processing logic. This is also automatically synchronized but still a bit shaky, so if things are not working, restart the Docker container.

### Airflow symbolic links

Because of the way the Airflow plugin system works, the code in the DAGs refers to the plugins in a different location. To help the IDE for development, we can use symlinks to symbolically link the files in the `plugins` folder to the Airflow package so that things like autocomplete will work. Run the `airflow_symbolic_links.sh` script from the root to set things up.

## CI / CD

For Google Cloud Composer, a CI/CD pipeline is set up using Google Cloud Build. When a new push is made to master, the `cloudbuild.yaml` file is used for the workflow. The following steps are executed:

- The commit hash is used as version
- The KubernetesPodOperator image is built and labeled with this version
- The `dags` folder is synchronized to Cloud Storage, which Cloud Composer synchronizes with
- The `plugins` folder is synchronized to Cloud Storage, which Cloud Composer synchronizes with
- The commit hash is set as variable in Cloud Composer so that the Operators use the new Docker image
