\# Docker Compose Multi-Container Assignment (Part 2)



\## Project Overview



This project deploys a Flask web application and a PostgreSQL database using Docker Compose. On top of the basic deployment it covers a new feature release (version 2), a database backup and restore strategy, scaling the web service to three instances, and monitoring with cAdvisor, Prometheus and Grafana.



\*\*Technologies:\*\* Docker, Docker Compose, Python (Flask), PostgreSQL 16, Prometheus, Grafana, cAdvisor.



\## Project Structure



```

assignment2-part2-compose/

|-- web/

|   |-- Dockerfile

|   |-- app.py

|   |-- requirements.txt

|-- db/

|   |-- Dockerfile

|-- backups/

|   |-- backup.sql

|-- monitoring/

|   |-- prometheus.yml

|-- screenshots/

|-- docker-compose.yml

|-- README.md

```



\## 1. Web Application Dockerfile



\*\*Description:\*\* This Dockerfile builds the image for the Flask web application. It starts from the small `python:3.12-slim` image, installs the dependencies listed in `requirements.txt`, copies `app.py`, and starts the app on port 5000 when the container starts.



\*\*File:\*\* `web/requirements.txt`



```

flask

psycopg2-binary

prometheus-client

```



\*\*File:\*\* `web/Dockerfile`



```dockerfile

\# Base image: small Python image

FROM python:3.12-slim



\# Working directory inside the container

WORKDIR /app



\# Copy only requirements first so the build cache can be reused

COPY requirements.txt .



\# Install dependencies

RUN pip install --no-cache-dir -r requirements.txt



\# Copy the application code

COPY app.py .



\# The app listens on port 5000

EXPOSE 5000



\# Start the app when the container starts

CMD \["python", "app.py"]

```



\*\*File:\*\* `web/app.py` (original version)



The app has these routes:



\- `/` returns "Hello, World!"

\- `/whoami` returns the ID of the container that served the request (used to prove scaling)

\- `/db` connects to the database and returns the PostgreSQL version (used to prove the two services are connected)

\- `/metrics` exposes Prometheus metrics, including the `web\_requests\_total` counter



```python

import os

import socket

from flask import Flask, Response

import psycopg2

from prometheus\_client import Counter, generate\_latest, CONTENT\_TYPE\_LATEST



app = Flask(\_\_name\_\_)



REQUESTS = Counter("web\_requests\_total", "Total requests", \["endpoint"])





@app.route("/")

def hello():

&#x20;   REQUESTS.labels("/").inc()

&#x20;   return "Hello, World!"





@app.route("/whoami")

def whoami():

&#x20;   REQUESTS.labels("/whoami").inc()

&#x20;   return f"Served by container: {socket.gethostname()}"





@app.route("/db")

def db\_check():

&#x20;   try:

&#x20;       conn = psycopg2.connect(

&#x20;           host=os.environ.get("DB\_HOST", "db"),

&#x20;           dbname=os.environ.get("DB\_NAME", "appdb"),

&#x20;           user=os.environ.get("DB\_USER", "appuser"),

&#x20;           password=os.environ.get("DB\_PASSWORD", "apppass"),

&#x20;           connect\_timeout=3,

&#x20;       )

&#x20;       cur = conn.cursor()

&#x20;       cur.execute("SELECT version();")

&#x20;       version = cur.fetchone()\[0]

&#x20;       conn.close()

&#x20;       return f"Database connected: {version}"

&#x20;   except Exception as e:

&#x20;       return f"Database connection FAILED: {e}", 500





@app.route("/metrics")

def metrics():

&#x20;   return Response(generate\_latest(), mimetype=CONTENT\_TYPE\_LATEST)





if \_\_name\_\_ == "\_\_main\_\_":

&#x20;   app.run(host="0.0.0.0", port=5000)

```



\## 2. Database Dockerfile



\*\*Description:\*\* This Dockerfile is based on the official PostgreSQL 16 image. The database user, password and database name are set with environment variables. (These credentials are only for this assignment; a real project should use secrets.)



\*\*File:\*\* `db/Dockerfile`



```dockerfile

\# Official PostgreSQL image

FROM postgres:16



\# Database user, password and database name

ENV POSTGRES\_USER=appuser

ENV POSTGRES\_PASSWORD=apppass

ENV POSTGRES\_DB=appdb



\# Default PostgreSQL port

EXPOSE 5432

```



\## 3. docker-compose.yml



\*\*Description:\*\* The Compose file defines two services: `web` (the Flask app) and `db` (PostgreSQL). Both are attached to a custom bridge network called `app\_network`, so the web app can reach the database simply by the service name `db`. The named volume `db\_data` keeps the database files outside the container, and the host folder `./backups` is mounted into the database container as `/backups`. The web service publishes a port range (`8000-8010`) so that every scaled instance gets its own free host port.



\*\*File:\*\* `docker-compose.yml` (the monitoring services were added later, see Section 8)



```yaml

services:

&#x20; web:

&#x20;   build: ./web

&#x20;   ports:

&#x20;     - "8000-8010:5000"

&#x20;   environment:

&#x20;     - DB\_HOST=db

&#x20;     - DB\_NAME=appdb

&#x20;     - DB\_USER=appuser

&#x20;     - DB\_PASSWORD=apppass

&#x20;   depends\_on:

&#x20;     - db

&#x20;   networks:

&#x20;     - app\_network



&#x20; db:

&#x20;   build: ./db

&#x20;   volumes:

&#x20;     - db\_data:/var/lib/postgresql/data

&#x20;     - ./backups:/backups

&#x20;   networks:

&#x20;     - app\_network



volumes:

&#x20; db\_data:



networks:

&#x20; app\_network:

```



\## 4. docker compose up



\*\*Description:\*\* This command builds both images (web and db) and starts both containers in the background. Newer Docker versions use `docker compose up` (with a space) instead of the old `docker-compose up`; both do the same job.



\*\*Command:\*\* build and start the services



```

docker compose up -d --build

```



\*\*Output:\*\*



```

\[+] up 6/6

&#x20;✔ Image assignment2-part2-compose-db            Built     41.0s

&#x20;✔ Image assignment2-part2-compose-web           Built     41.1s

&#x20;✔ Network assignment2-part2-compose\_app\_network Created   0.0s

&#x20;✔ Volume assignment2-part2-compose\_db\_data      Created   0.0s

&#x20;✔ Container assignment2-part2-compose-db-1      Started   0.6s

&#x20;✔ Container assignment2-part2-compose-web-1     Started   0.4s

```



\*\*Command:\*\* check the state of the services



```

docker compose ps

```



\*\*Output:\*\*



```

NAME                              IMAGE                          COMMAND                  SERVICE   STATUS         PORTS

assignment2-part2-compose-db-1    assignment2-part2-compose-db   "docker-entrypoint.s…"   db        Up 3 minutes   5432/tcp

assignment2-part2-compose-web-1   assignment2-part2-compose-web  "python app.py"          web       Up 3 minutes   0.0.0.0:8000->5000/tcp, \[::]:8000->5000/tcp

```



\*\*Command:\*\* show the logs of both services



```

docker compose logs

```



\*\*Output (important part):\*\*



```

web-1  |  \* Serving Flask app 'app'

web-1  |  \* Running on all addresses (0.0.0.0)

web-1  |  \* Running on http://172.18.0.3:5000

db-1   | PostgreSQL init process complete; ready for start up.

db-1   | LOG:  listening on IPv4 address "0.0.0.0", port 5432

db-1   | LOG:  database system is ready to accept connections

```



The Flask app is running on port 5000 and the database is ready to accept connections.



\*\*Command:\*\* check that the database is running



```

docker compose exec db psql -U appuser -d appdb -c "SELECT version();"

```



\*\*Output:\*\*



```

&#x20;                                                   version

\-----------------------------------------------------------------------------------------------------------------------

&#x20;PostgreSQL 16.15 (Debian 16.15-1.pgdg13+2) on x86\_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit

(1 row)

```



\*\*Screenshots:\*\* `http://localhost:8000` shows "Hello, World!", and `http://localhost:8000/db` shows "Database connected: PostgreSQL 16...", which proves that the web and db services are connected over the same network.



!\[hello v1](screenshots/hello-v1.png)



!\[db connected](screenshots/db-connected.png)



\## 5. New Feature (Version 2)



\*\*Description:\*\* Both the Dockerfile and `app.py` were modified. A new environment variable `APP\_MESSAGE` was added to `web/Dockerfile`, and the `/` route in `web/app.py` now reads its message from that variable. A new `/about` page was also added.



\*\*Change in `web/Dockerfile` (added before `EXPOSE 5000`):\*\*



```dockerfile

\# New feature: environment variable for a custom welcome message

ENV APP\_MESSAGE="Hello, World! - Version 2 is live"

```



\*\*Change in `web/app.py`:\*\*



```python

@app.route("/")

def hello():

&#x20;   REQUESTS.labels("/").inc()

&#x20;   return os.environ.get("APP\_MESSAGE", "Hello, World!")





@app.route("/about")

def about():

&#x20;   REQUESTS.labels("/about").inc()

&#x20;   return "About page: this is version 2 of the Docker Compose assignment."

```



\*\*Redeploy commands:\*\*



\*\*Command:\*\* rebuild only the web image with the new changes



```

docker compose build web

```



\*\*Output:\*\*



```

\[+] Building 2.1s (13/13) FINISHED

&#x20;...

\[+] build 1/1

&#x20;✔ Image assignment2-part2-compose-web Built    2.3s

```



\*\*Command:\*\* recreate and start only the web container (the database is not touched)



```

docker compose up -d web

```



\*\*Output:\*\*



```

\[+] up 2/2

&#x20;✔ Container assignment2-part2-compose-db-1  Running   0.0s

&#x20;✔ Container assignment2-part2-compose-web-1 Started   3.6s

```



\*\*Command:\*\* confirm that the web service is up again



```

docker compose ps

```



\*\*Output:\*\*



```

NAME                              IMAGE                          COMMAND                  SERVICE   CREATED          STATUS          PORTS

assignment2-part2-compose-db-1    assignment2-part2-compose-db   "docker-entrypoint.s…"   db        27 minutes ago   Up 27 minutes   5432/tcp

assignment2-part2-compose-web-1   assignment2-part2-compose-web  "python app.py"          web       14 seconds ago   Up 10 seconds   0.0.0.0:8001->5000/tcp, \[::]:8001->5000/tcp

```



The database container (`db-1`) kept running; only the web container was recreated. Docker assigned host port 8001 this time (a free port from the 8000-8010 range), so the new version was opened at `localhost:8001`.



\*\*Screenshots:\*\* `/` now shows "Hello, World! - Version 2 is live", and the new `/about` page is available.



!\[hello v2](screenshots/hello-v2.png)



!\[about v2](screenshots/about-v2.png)



\## 6. Database Backup Strategy



\*\*What the volume does:\*\* The named volume `db\_data` stores the database files (`/var/lib/postgresql/data`) outside the container, in Docker's own storage. If the container is deleted or recreated, the data survives. However, `docker compose down -v` also deletes the volume, so a separate backup file is needed as well.



\*\*What the backup command does:\*\* `pg\_dump` writes a full copy of the database into a `.sql` file. The host folder `./backups` is mounted at `/backups` inside the database container, so the backup file also appears in the `backups` folder on the host and stays safe even if the volume is deleted. (Optional: the backup command can be scheduled to run daily with Windows Task Scheduler to get periodic backups.)



\*\*Step 1: create test data\*\*



\*\*Command:\*\* create a table called `notes`



```

docker compose exec db psql -U appuser -d appdb -c "CREATE TABLE notes (id SERIAL PRIMARY KEY, text VARCHAR(100));"

```



\*\*Output:\*\*



```

CREATE TABLE

```



\*\*Command:\*\* insert two rows



```

docker compose exec db psql -U appuser -d appdb -c "INSERT INTO notes (text) VALUES ('first note'), ('second note');"

```



\*\*Output:\*\*



```

INSERT 0 2

```



\*\*Command:\*\* show the rows



```

docker compose exec db psql -U appuser -d appdb -c "SELECT \* FROM notes;"

```



\*\*Output:\*\*



```

&#x20;id |    text

\----+-------------

&#x20; 1 | first note

&#x20; 2 | second note

(2 rows)

```



\*\*Step 2: take a backup\*\*



\*\*Command:\*\* dump the whole database to `/backups/backup.sql` (the redirect is placed inside `sh -c` because redirecting with `>` directly in PowerShell would save the file in UTF-16 and the restore would fail)



```

docker compose exec -T db sh -c "pg\_dump -U appuser appdb > /backups/backup.sql"

```



\*\*Output:\*\* none (the file is created)



\*\*Command:\*\* confirm that the backup file exists



```

dir backups

```



\*\*Output:\*\*



```

Mode                 LastWriteTime         Length Name

\----                 -------------         ------ ----

\-a----        10/11/2026   2:16 AM           2013 backup.sql

```



\*\*Step 3: simulate a disaster (delete all data)\*\*



\*\*Command:\*\* remove the containers together with their volumes (the data is lost, the backup file on the host is safe)



```

docker compose down -v

```



\*\*Output:\*\*



```

\[+] down 4/4

&#x20;✔ Container assignment2-part2-compose-web-1     Removed   3.3s

&#x20;✔ Container assignment2-part2-compose-db-1      Removed   0.2s

&#x20;✔ Network assignment2-part2-compose\_app\_network Removed   0.2s

&#x20;✔ Volume assignment2-part2-compose\_db\_data      Removed   0.0s

```



\*\*Command:\*\* start everything again (the database is now empty)



```

docker compose up -d

```



\*\*Output:\*\*



```

\[+] up 4/4

&#x20;✔ Network assignment2-part2-compose\_app\_network Created   0.0s

&#x20;✔ Volume assignment2-part2-compose\_db\_data      Created   0.0s

&#x20;✔ Container assignment2-part2-compose-db-1      Started   0.3s

&#x20;✔ Container assignment2-part2-compose-web-1     Started   0.4s

```



\*\*Command:\*\* try to read the table (it no longer exists, the data is gone)



```

docker compose exec db psql -U appuser -d appdb -c "SELECT \* FROM notes;"

```



\*\*Output:\*\*



```

ERROR:  relation "notes" does not exist

LINE 1: SELECT \* FROM notes;

&#x20;                     ^

```



\*\*Step 4: restore test\*\*



\*\*Command:\*\* restore the data from the backup file



```

docker compose exec -T db sh -c "psql -U appuser -d appdb < /backups/backup.sql"

```



\*\*Output:\*\*



```

SET

SET

SET

SET

SET

&#x20;set\_config

\------------



(1 row)



SET

SET

SET

SET

SET

SET

CREATE TABLE

ALTER TABLE

CREATE SEQUENCE

ALTER SEQUENCE

ALTER SEQUENCE

ALTER TABLE

COPY 2

&#x20;setval

\--------

&#x20;     2

(1 row)



ALTER TABLE

```



\*\*Command:\*\* check the table again (both rows are back, so the restore was successful)



```

docker compose exec db psql -U appuser -d appdb -c "SELECT \* FROM notes;"

```



\*\*Output:\*\*



```

&#x20;id |    text

\----+-------------

&#x20; 1 | first note

&#x20; 2 | second note

(2 rows)

```



\## 7. Scaling Strategy



\*\*Note:\*\* The assignment mentions `docker-compose scale`. In newer versions of Docker Compose that command has been removed and replaced by the `--scale` flag, which does the same job. The web service publishes the port range `8000-8010:5000` in the Compose file, so each instance gets its own free host port.



\*\*Command:\*\* run three instances of the web service



```

docker compose up -d --scale web=3

```



\*\*Output:\*\*



```

\[+] up 4/4

&#x20;✔ Container assignment2-part2-compose-web-1 Running   0.0s

&#x20;✔ Container assignment2-part2-compose-db-1  Running   0.0s

&#x20;✔ Container assignment2-part2-compose-web-3 Started   0.6s

&#x20;✔ Container assignment2-part2-compose-web-2 Started   0.4s

```



\*\*Command:\*\* show the containers (three web containers, each with its own host port)



```

docker compose ps

```



\*\*Output:\*\*



```

NAME                              IMAGE                          COMMAND                  SERVICE   CREATED          STATUS          PORTS

assignment2-part2-compose-db-1    assignment2-part2-compose-db   "docker-entrypoint.s…"   db        20 hours ago     Up 20 hours     5432/tcp

assignment2-part2-compose-web-1   assignment2-part2-compose-web  "python app.py"          web       20 hours ago     Up 20 hours     0.0.0.0:8002->5000/tcp, \[::]:8002->5000/tcp

assignment2-part2-compose-web-2   assignment2-part2-compose-web  "python app.py"          web       7 seconds ago    Up 7 seconds    0.0.0.0:8003->5000/tcp, \[::]:8003->5000/tcp

assignment2-part2-compose-web-3   assignment2-part2-compose-web  "python app.py"          web       7 seconds ago    Up 6 seconds    0.0.0.0:8004->5000/tcp, \[::]:8004->5000/tcp

```



\*\*Verification:\*\* the `/whoami` page returns the ID of the container that served the request. Calling it on all three ports and getting three different IDs proves that the three instances are separate containers.



\*\*Command:\*\* call `/whoami` on every instance



```

8002..8004 | ForEach-Object { "Port $\_ -> " + (curl.exe -s "http://localhost:$\_/whoami") }

```



\*\*Output:\*\*



```

Port 8002 -> Served by container: dd3fbe5489ce

Port 8003 -> Served by container: 10b1a7b46ee7

Port 8004 -> Served by container: 939182b6b7af

```



\*\*Screenshots:\*\* the three instances in the browser.



!\[scale 8002](screenshots/scale-8002.png)



!\[scale 8003](screenshots/scale-8003.png)



!\[scale 8004](screenshots/scale-8004.png)



\## 8. Monitoring Strategy (Prometheus + Grafana)



\*\*Description:\*\* Three tools were added: \*\*cAdvisor\*\* (CPU and memory metrics of the containers), \*\*Prometheus\*\* (collects the metrics) and \*\*Grafana\*\* (shows graphs and dashboards). The web app also exposes its own `web\_requests\_total` counter on `/metrics`.



\*\*File:\*\* `monitoring/prometheus.yml`



```yaml

global:

&#x20; scrape\_interval: 15s



scrape\_configs:

&#x20; - job\_name: prometheus

&#x20;   static\_configs:

&#x20;     - targets: \['localhost:9090']



&#x20; - job\_name: web

&#x20;   dns\_sd\_configs:

&#x20;     - names: \['web']

&#x20;       type: A

&#x20;       port: 5000



&#x20; - job\_name: cadvisor

&#x20;   static\_configs:

&#x20;     - targets: \['cadvisor:8080']

```



In the `web` job, `dns\_sd\_configs` automatically discovers all scaled instances of the web service through DNS.



\*\*Services added to `docker-compose.yml`:\*\*



```yaml

&#x20; cadvisor:

&#x20;   image: gcr.io/cadvisor/cadvisor:v0.49.1

&#x20;   volumes:

&#x20;     - /:/rootfs:ro

&#x20;     - /var/run:/var/run:ro

&#x20;     - /sys:/sys:ro

&#x20;     - /var/lib/docker/:/var/lib/docker:ro

&#x20;   ports:

&#x20;     - "8080:8080"

&#x20;   networks:

&#x20;     - app\_network



&#x20; prometheus:

&#x20;   image: prom/prometheus

&#x20;   volumes:

&#x20;     - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro

&#x20;   ports:

&#x20;     - "9090:9090"

&#x20;   networks:

&#x20;     - app\_network



&#x20; grafana:

&#x20;   image: grafana/grafana

&#x20;   ports:

&#x20;     - "3000:3000"

&#x20;   volumes:

&#x20;     - grafana\_data:/var/lib/grafana

&#x20;   depends\_on:

&#x20;     - prometheus

&#x20;   networks:

&#x20;     - app\_network

```



A `grafana\_data:` entry was also added to the `volumes:` section at the bottom of the file.



\*\*Command:\*\* start the monitoring services and keep three web instances



```

docker compose up -d --scale web=3

```



\*\*Output:\*\*



```

\[+] up 35/35

&#x20;✔ Image prom/prometheus                             Pulled    133.8s

&#x20;✔ Image gcr.io/cadvisor/cadvisor:v0.49.1            Pulled    9.0s

&#x20;✔ Image grafana/grafana                             Pulled    128.9s

&#x20;✔ Container assignment2-part2-compose-web-1         Running   0.0s

&#x20;✔ Container assignment2-part2-compose-web-2         Running   0.0s

&#x20;✔ Container assignment2-part2-compose-web-3         Running   0.0s

&#x20;✔ Container assignment2-part2-compose-db-1          Running   0.0s

&#x20;✔ Volume assignment2-part2-compose\_grafana\_data     Created   0.0s

&#x20;✔ Container assignment2-part2-compose-cadvisor-1    Started   3.1s

&#x20;✔ Container assignment2-part2-compose-prometheus-1  Started   3.2s

&#x20;✔ Container assignment2-part2-compose-grafana-1     Started   0.6s

```



\*\*Command:\*\* check that all services are up



```

docker compose ps --format "table {{.Name}}\\t{{.Service}}\\t{{.Status}}\\t{{.Ports}}"

```



\*\*Output:\*\*



```

NAME                                    SERVICE      STATUS                   PORTS

assignment2-part2-compose-cadvisor-1    cadvisor     Up 5 minutes (healthy)   0.0.0.0:8080->8080/tcp, \[::]:8080->8080/tcp

assignment2-part2-compose-db-1          db           Up 20 hours              5432/tcp

assignment2-part2-compose-grafana-1     grafana      Up 5 minutes             0.0.0.0:3000->3000/tcp, \[::]:3000->3000/tcp

assignment2-part2-compose-prometheus-1  prometheus   Up 5 minutes             0.0.0.0:9090->9090/tcp, \[::]:9090->9090/tcp

assignment2-part2-compose-web-1         web          Up 20 hours              0.0.0.0:8002->5000/tcp, \[::]:8002->5000/tcp

assignment2-part2-compose-web-2         web          Up 33 minutes            0.0.0.0:8003->5000/tcp, \[::]:8003->5000/tcp

assignment2-part2-compose-web-3         web          Up 33 minutes            0.0.0.0:8004->5000/tcp, \[::]:8004->5000/tcp

```



\### Health monitoring (Prometheus targets)



On `http://localhost:9090/targets` all three jobs are \*\*UP\*\*: `cadvisor` 1/1, `prometheus` 1/1 and `web` 3/3 (all three web instances). This is the proof of health monitoring.



!\[prometheus targets](screenshots/prometheus-targets.png)



\### Prometheus queries



I first sent some requests to the web app so that the counters increase, and then ran `web\_requests\_total` in the Prometheus query box. The result shows the request count of every web instance separately.



!\[web requests total](screenshots/prometheus-web-requests.png)



The query `container\_memory\_usage\_bytes` shows the memory usage of the containers as reported by cAdvisor.



!\[container memory](screenshots/prometheus-memory.png)



\### Grafana



\- Grafana was opened at `http://localhost:3000` (login `admin`).

\- Data source: \*\*Prometheus\*\*, URL `http://prometheus:9090`. \*\*Save \& test\*\* was successful.



!\[grafana data source](screenshots/grafana-datasource.png)



\- \*\*What did not work:\*\* the cAdvisor dashboard (ID `14282`) was imported, but all of its panels showed "No data" on Windows with Docker Desktop. This is an old dashboard that depends on cAdvisor labels which are not available in this environment.



!\[grafana import no data](screenshots/grafana-import-nodata.png)



\- \*\*What worked:\*\* I created my own panel with the query `sum(rate(web\_requests\_total\[1m]))`. It shows the request rate of the web app: the line rises while traffic is being generated and falls back afterwards. The dashboard was saved as `Web Monitoring`.



!\[grafana dashboard](screenshots/grafana-dashboard.png)



\## Conclusion



What I learned from this assignment:



\- \*\*Compose networking:\*\* both services are attached to the custom network `app\_network`, so they find each other by service name (for example the web app reaches the database as `db`).

\- \*\*Volumes and backups:\*\* the `db\_data` volume keeps the data separate from the container, and a `pg\_dump` backup lets the data be restored even after the volume has been deleted.

\- \*\*Scaling:\*\* `docker compose up --scale web=3` runs several instances of one service, and `/whoami` proved that they are separate containers.

\- \*\*Monitoring:\*\* Prometheus collected metrics from all three web instances and from cAdvisor, and Grafana was used to draw a graph of the request rate.

