# Ch02 PostgreSQL

This Chapter design how to set PostgreSQL with Django Project. And use docker to build development environment plus normal use of docker-compose.

## 1. Start project, DockerFile, and docker-compose

- Start Django project

    ```bash
    > python djagno-admin startproject database_project
    ```

- Create relate Dockerfile in folder
- Create docker-compose.yml in Project Folder. it’s ch02 in my case.

## 2. Run in detached Mode

This is simple case to run docker with docker-compose.

```bash
> docker-compose up -d 
```

```yaml
version: '3.9'

services:
  web:
    image: ch02_web
    command: python /code/manage.py runserver 0.0.0.0:8000
    ports:
      - 8000:8000
```

- Environment setting

    In my case, I set development environment in docker-mopose-dev.yml which let web on port 8001.

    ```yaml
    # docker-compose-dev.yml
    version: '3.9'
    
    services:
      web:
        build: database/.
        volumes:
          - ./database/src:/code
        ports:
          - 8001:8000
        networks:
          - dev-network
    
      db:
        networks:
          - dev-network 
    
    networks:
      dev-network:
        driver: bridge
    ```

    With override method to mount code, build image, and local network

    ```bash
    > docker-compose -p dev -f docker-compose.yml -f docker-compose-dev.yml -d
    ```

## 3. PostgreSQL

To run PostgreSQL in our project, we need to do 3 steps:

- install database adapter, `psycopg2` , so Python can talk to PostgreSQL
- update `DATABASE` config in `setting.py` file
- install and run PostgreSQL local ( Use container)

### 1. Psycopg

```yaml
> pipenv install psycopg2-binary
```

### 2. Setting

```python
# porstgre_project/setting.py

...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}
...
```

### 3. Run PostgreSQL with setting

Modify the docker-compose with db section

```yaml
# docker-compose.yml
version: '3.9'

services:
  web:
    image: ch02_web
    command: python /code/manage.py runserver 0.0.0.0:8000
    environment:
      - POSTGRES_NAME=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - 8000:8000
    depends_on:
      - db

  db:
    image: postgres:11
    environment:
      - POSTGRES_NAME=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
```

## 4. Run code on docker-compose

```bash
> docker-compose -p dev -f docker-compose.yml -f docker-compose-dev.yml up -d
```

Then try to use [localhost:8001](http://localhost:8001)/admin to log in, which will fail. So we need to create super user in our project

```bash
> docker-compose -p dev exec web python manage.py migrate
> docker-compose -p dev exec web python manage.py createsuperuser
```

## 5. Conclusion

- The docker-compose is not correct in book
- When active volume in docker-compose, `.dockerignore`  may not work properly.
- Use docker-compose to TOTAL replace virtual machine.
