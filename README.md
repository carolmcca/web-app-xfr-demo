# An Integrated and User-friendly Platform for the Deployment of Explainable Artificial Intelligence Methods Applied to Face Recognition

## About
Implementation of the paper "An Integrated and User-friendly Platform for the Deployment of Explainable Artificial Intelligence Methods Applied to Face Recognition" by Carolina Albuquerque, Pedro C. Neto, Tiago Gonçalves, and Ana F. Sequeira. This publication resulted from Carolina's MSc dissertation ["An integrated and user-friendly platform for  the deployment of explainable Artificial Intelligence methods applied to Face Recognition"](https://hdl.handle.net/10216/160960), which contains additional details and information.

Please refer to the [Hugging Face repository](https://huggingface.co/tiagofilipesousagoncalves/web-app-xfr-demo) for the face recognition model's weights.



## Description
The application is designed to demonstrate four main tasks: Enrollment, Identification, Authentication, and Verification.

## Key Features
* **Enrollment:** Users can enroll by choosing a username and password and uploading images, which are processed to extract facial embeddings and store them securely.
* **Identification:** Users can upload an image or select from provided examples to search for a corresponding identity in the database.
* **Authentication:** The application verifies user identities by comparing uploaded images with stored embeddings.
* **Verification:** Users can compare two images to check if they belong to the same individual without storing any additional data in the database.

## Usage
To run the application, the following environment variable should be set:
```
POSTGRES_DB = your_database_name
POSTGRES_USER = your_database_user
POSTGRES_PASSWORD = your_database_password
POSTGRES_HOST = your_datase_host
POSTGRES_PORT = your_datase_port

PGADMIN_DEFAULT_EMAIL = your_pgadmin_email
PGADMIN_DEFAULT_PASSWORD = your_pgadmin_password

ANNOY_INDEX_PATH = path/to/your/annoy_index_file.ann
FAISS_INDEX_PATH = path/to/your/faiss_index_file.faiss

VUE_APP_BACKEND_SERVER = http://localhost:8000/api
VUE_APP_ORIGIN = http://localhost:8080
```
To serve the application, run

```
docker compose -f [docker_compose_file] up --build
```

where [docker_compose_file] can be substituted with `docker-compose.dev.yml` for development environments, or `docker-compose.prod.yml` for production environments.

### Development environment
In the development environment, the frontend of the application is served on `localhost:8080` and the backend on `localhost:8000/api`. Ensure the environment variables `VUE_APP_BACKEND_SERVER` and `VUE_APP_ORIGIN` are set as in the example above.

### Production Environment
In the production environment, the server URL is also defined in the `.env` file. If you wish to serve the application using ngrok, create a tunnel for port 80 by running:
```
ngrok http 80
```

This command will provide the URL to which the port is being forwarded. Substitute this URL in the environment variables `VUE_APP_BACKEND_SERVER` and `VUE_APP_ORIGIN`. After running the command and setting the variables, you can run the Docker Compose command to start serving the application.


## Acknowledgment
This work was financed by National Funds through the Portuguese funding agency, FCT - Fundação para a Ciência e a Tecnologia, within project UIDB/50014/2020.

DOI 10.54499/UIDB/50014/2020 | https://doi.org/10.54499/uidb/50014/2020
