making network 



Command:

docker network create --driver bridge my\_network



Output:

ce521a0ff5feb077ceb4552f7b68f5c3f1ea7fec51b612eeab3a209052685327



Command:

docker network ls



Output:

NETWORK ID     NAME         DRIVER    SCOPE

9946419e89ee   bridge       bridge    local

d9a00e5d6a18   host         host      local

ce521a0ff5fe   my\_network   bridge    local

d737ea71d70c   none         null      local





making nginx\_container 



Command:

docker run -d --name nginx\_container --network my\_network -p 8080:80 nginx



Output:

8e9660781379c2082968bd2bc89a8c775295faa5f1583f03f6588d9eb000421f



Command:

docker ps



Output:

CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                                     NAMES

8e9660781379   nginx     "/docker-entrypoint.…"   16 seconds ago   Up 15 seconds   0.0.0.0:8080->80/tcp, \[::]:8080->80/tcp   nginx\_container





&#x20;nginx page verifying



Command:

curl.exe -I http://localhost:8080



Output:

HTTP/1.1 200 OK

Server: nginx/1.31.6

Date: Sat, 10 Oct 2026 16:53:54 GMT

Content-Type: text/html

Content-Length: 896

Last-Modified: Tue, 15 Sep 2026 12:54:15 GMT

Connection: keep-alive

ETag: "6aa93ff7-380"

Accept-Ranges: bytes



Screenshot: screenshots/nginx-8080.png





&#x20;making httpd\_container 



Command:

docker run -d --name httpd\_container --network my\_network -p 8081:80 httpd



Output:

1191b2c697d9ba584e0066000101ca4e5e0a296e6c3775cabc802ceb4f2d025e



Command:

docker ps



Output:

CONTAINER ID   IMAGE     COMMAND              CREATED          STATUS          PORTS                                     NAMES

1191b2c697d9   httpd     "httpd-foreground"   21 seconds ago   Up 20 seconds   0.0.0.0:8081->80/tcp, \[::]:8081->80/tcp   httpd\_container

8e9660781379   nginx     "/docker-entrypoint.…"   13 minutes ago   Up 13 minutes   0.0.0.0:8080->80/tcp, \[::]:8080->80/tcp   nginx\_container



httpd page verifying



Command:

curl.exe -I http://localhost:8081



Output:

HTTP/1.1 200 OK

Date: Sat, 10 Oct 2026 17:09:07 GMT

Server: Apache/2.4.69 (Unix)

Last-Modified: Fri, 07 Nov 2025 08:23:08 GMT

ETag: "bf-642fce432f300"

Accept-Ranges: bytes

Content-Length: 191

Content-Type: text/html



Screenshot: screenshots/httpd-8081.png



&#x20;docker network inspect



Command:

docker network inspect my\_network



Output:





Findings:

\- Driver: bridge, Scope: local

\- Subnet: 172.18.0.0/16

\- Gateway: 172.18.0.1



&#x20; - nginx\_container, IPv4 Address: 172.18.0.2/16

&#x20; - httpd\_container, IPv4 Address: 172.18.0.3/16



Removing and stoping nginx\_container 



Command:

docker stop nginx\_container



Output:

nginx\_container



Command:

docker rm nginx\_container



Output:

nginx\_container



Command:

docker ps -a



Output:

CONTAINER ID   IMAGE     COMMAND              CREATED          STATUS          PORTS                                     NAMES

1191b2c697d9   httpd     "httpd-foreground"   19 minutes ago   Up 19 minutes   0.0.0.0:8081->80/tcp, \[::]:8081->80/tcp   httpd\_container



\[

&#x20;   {

&#x20;       "Name": "my\_network",

&#x20;       "Id": "ce521a0ff5feb077ceb4552f7b68f5c3f1ea7fec51b612eeab3a209052685327",

&#x20;       "Created": "2026-10-10T16:32:06.037244385Z",

&#x20;       "Scope": "local",

&#x20;       "Driver": "bridge",

&#x20;       "EnableIPv4": true,

&#x20;       "EnableIPv6": false,

&#x20;       "IPAM": {

&#x20;           "Driver": "default",

&#x20;           "Options": {},

&#x20;           "Config": \[

&#x20;               {

&#x20;                   "Subnet": "172.18.0.0/16",

&#x20;                   "Gateway": "172.18.0.1"

&#x20;               }

&#x20;           ]

&#x20;       },

&#x20;       "Internal": false,

&#x20;       "Attachable": false,

&#x20;       "Ingress": false,

&#x20;       "ConfigFrom": {

&#x20;           "Network": ""

&#x20;       },

&#x20;       "ConfigOnly": false,

&#x20;       "Options": {

&#x20;           "com.docker.network.enable\_ipv4": "true",

&#x20;           "com.docker.network.enable\_ipv6": "false"

&#x20;       },

&#x20;       "Labels": {},

&#x20;       "Containers": {

&#x20;           "1191b2c697d9ba584e0066000101ca4e5e0a296e6c3775cabc802ceb4f2d025e": {

&#x20;               "Name": "httpd\_container",

&#x20;               "EndpointID": "dd8664950bcb49cfe983e04c985944c85ae6a897ab7ebaaa09d8aed24773341f",

&#x20;               "MacAddress": "92:5a:16:08:7f:a4",

&#x20;               "IPv4Address": "172.18.0.3/16",

&#x20;               "IPv6Address": ""

&#x20;           },

&#x20;           "8e9660781379c2082968bd2bc89a8c775295faa5f1583f03f6588d9eb000421f": {

&#x20;               "Name": "nginx\_container",

&#x20;               "EndpointID": "3035bc2c2c735f80ac563f35b8d00720c3b30e9ac3bbca74772684b7cc809b31",

&#x20;               "MacAddress": "52:db:11:7a:de:48",

&#x20;               "IPv4Address": "172.18.0.2/16",

&#x20;               "IPv6Address": ""

&#x20;           }

&#x20;       },

&#x20;       "Status": {

&#x20;           "IPAM": {

&#x20;               "Subnets": {

&#x20;                   "172.18.0.0/16": {

&#x20;                       "IPsInUse": 5,

&#x20;                       "DynamicIPsAvailable": 65531

&#x20;                   }

&#x20;               }

&#x20;           }

&#x20;       }

&#x20;   }

]





making nginx\_container\_2 



Command:

docker run -d --name nginx\_container\_2 --network my\_network -p 8082:80 nginx



Output:

d7f086eddf4abeba37a73d6726290b054cb0bc04f135ebda0027f087f6ba8879



Command:

docker ps



Output:

CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                                     NAMES

d7f086eddf4a   nginx     "/docker-entrypoint.…"   11 seconds ago   Up 11 seconds   0.0.0.0:8082->80/tcp, \[::]:8082->80/tcp   nginx\_container\_2

1191b2c697d9   httpd     "httpd-foreground"       23 minutes ago   Up 23 minutes   0.0.0.0:8081->80/tcp, \[::]:8081->80/tcp   httpd\_container



verifying nginx\_container\_2 page 



Command:

curl.exe -I http://localhost:8082



Output:

HTTP/1.1 200 OK

Server: nginx/1.31.6

Date: Sat, 10 Oct 2026 17:24:37 GMT

Content-Type: text/html

Content-Length: 896

Last-Modified: Tue, 15 Sep 2026 12:54:15 GMT

Connection: keep-alive

ETag: "6aa93ff7-380"

Accept-Ranges: bytes



Screenshot: screenshots/nginx-8082.png



docker container ls 



Command:

docker container ls



Output:

CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                                     NAMES

d7f086eddf4a   nginx     "/docker-entrypoint.…"   6 minutes ago    Up 6 minutes    0.0.0.0:8082->80/tcp, \[::]:8082->80/tcp   nginx\_container\_2

1191b2c697d9   httpd     "httpd-foreground"       29 minutes ago   Up 29 minutes   0.0.0.0:8081->80/tcp, \[::]:8081->80/tcp   httpd\_container





===== Step 3.11: Stopping and removing all  containers 



Command:

docker stop httpd\_container nginx\_container\_2



Output:

httpd\_container

nginx\_container\_2



Command:

docker rm httpd\_container nginx\_container\_2



Output:

httpd\_container

nginx\_container\_2



Command:

docker container ls -a



Output:

CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES



Cleanup network



Note: my\_network ek galat paste ki wajah se pehle hi delete ho chuka tha, is liye usay dobara banaya aur phir remove kiya, taake command ka sahi output dikhe.



Command:

docker network create --driver bridge my\_network



Output:

8d56cf3e5d4461849d0ae09e579b7e67646bca8129c1f49e4ea9a7e315a52ac0



Command:

docker network rm my\_network



Output:

my\_network



Command:

docker network ls



Output:

NETWORK ID     NAME      DRIVER    SCOPE

662b0a746144   bridge    bridge    local

d9a00e5d6a18   host      host      local

d737ea71d70c   none      null      local





Command:

docker compose ps



Output:

NAME                            IMAGE                         COMMAND                  SERVICE   CREATED         STATUS         PORTS

assignment2-part2-compose-db-1  assignment2-part2-compose-db  "docker-entrypoint.s…"   db        3 minutes ago   Up 3 minutes   5432/tcp

assignment2-part2-compose-web-1 assignment2-part2-compose-web "python app.py"          web       3 minutes ago   Up 3 minutes   0.0.0.0:8000->5000/tcp, \[::]:8000->5000/tcp





Command:

docker compose logs



Output 

web-1  |  \* Serving Flask app 'app'

web-1  |  \* Debug mode: off

web-1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.

web-1  |  \* Running on all addresses (0.0.0.0)

web-1  |  \* Running on http://127.0.0.1:5000

web-1  |  \* Running on http://172.18.0.3:5000

web-1  | Press CTRL+C to quit

db-1   | PostgreSQL init process complete; ready for start up.

db-1   | 2026-10-10 20:35:58.121 UTC \[1] LOG:  starting PostgreSQL 16.15 (Debian 16.15-1.pgdg13+2) on x86\_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit

db-1   | 2026-10-10 20:35:58.122 UTC \[1] LOG:  listening on IPv4 address "0.0.0.0", port 5432

db-1   | 2026-10-10 20:35:58.131 UTC \[1] LOG:  database system is ready to accept connections



Command:

docker compose exec db psql -U appuser -d appdb -c "SELECT version();"



Output:

&#x20;                                                   version

\-----------------------------------------------------------------------------------------------------------------------

&#x20;PostgreSQL 16.15 (Debian 16.15-1.pgdg13+2) on x86\_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit

(1 row)





Screenshots: screenshots/hello-v1.png, screenshots/db-connected.png





===== Step 4.5: Naya feature (Version 2) aur redeploy =====



Changes:

\- web/Dockerfile mein nayi line: ENV APP\_MESSAGE="Hello, World! - Version 2 is live"

\- web/app.py mein: "/" ab APP\_MESSAGE environment variable se message dikhata hai, aur naya /about route add kiya



Command:

docker compose build web



Output:

\[+] Building 2.1s (13/13) FINISHED

&#x20;...

\[+] build 1/1

&#x20;✔ Image assignment2-part2-compose-web Built    2.3s



Command:

docker compose up -d web



Output:

\[+] up 2/2

&#x20;✔ Container assignment2-part2-compose-db-1  Running   0.0s

&#x20;✔ Container assignment2-part2-compose-web-1 Started   3.6s





Command:

docker compose ps



Output:

NAME                              IMAGE                          COMMAND                  SERVICE   CREATED          STATUS          PORTS

assignment2-part2-compose-db-1    assignment2-part2-compose-db   "docker-entrypoint.s…"   db        27 minutes ago   Up 27 minutes   5432/tcp

assignment2-part2-compose-web-1   assignment2-part2-compose-web  "python app.py"          web       14 seconds ago   Up 10 seconds   0.0.0.0:8001->5000/tcp, \[::]:8001->5000/tcp





Screenshots: screenshots/hello-v2.png, screenshots/about-v2.png







&#x20;Database backup strategy 







Command:

docker compose exec db psql -U appuser -d appdb -c "CREATE TABLE notes (id SERIAL PRIMARY KEY, text VARCHAR(100));"



Output:

CREATE TABLE





Command:

docker compose exec -T db psql -U appuser -d appdb -c "INSERT INTO notes (text) VALUES ('first note'), ('second note');"



Output:

INSERT 0 2



Command:

docker compose exec -T db psql -U appuser -d appdb -c "SELECT \* FROM notes;"



Output:

&#x20;id |    text

\----+-------------

&#x20; 1 | first note

&#x20; 2 | second note

(2 rows)



Backup lena:



Command:

docker compose exec -T db sh -c "pg\_dump -U appuser appdb > /backups/backup.sql"



Output:

(koi output nahi, file ban gayi)



Command:

dir backups



Output:

Mode                 LastWriteTime         Length Name

\----                 -------------         ------ ----

\-a----        10/11/2026   2:16 AM           2013 backup.sql





Disaster simulate karna (data ura diya):



Command:

docker compose down -v



Output:

\[+] down 4/4

&#x20;✔ Container assignment2-part2-compose-web-1     Removed   3.3s

&#x20;✔ Container assignment2-part2-compose-db-1      Removed   0.2s

&#x20;✔ Network assignment2-part2-compose\_app\_network Removed   0.2s

&#x20;✔ Volume assignment2-part2-compose\_db\_data      Removed   0.0s



Command:

docker compose up -d



Output:

\[+] up 4/4

&#x20;✔ Network assignment2-part2-compose\_app\_network Created   0.0s

&#x20;✔ Volume assignment2-part2-compose\_db\_data      Created   0.0s

&#x20;✔ Container assignment2-part2-compose-db-1      Started   0.3s

&#x20;✔ Container assignment2-part2-compose-web-1     Started   0.4s



Command:

docker compose exec -T db psql -U appuser -d appdb -c "SELECT \* FROM notes;"



Output:

ERROR:  relation "notes" does not exist

LINE 1: SELECT \* FROM notes;

&#x20;                     ^





Restore karna (backup se data wapas laana):



Command:

docker compose exec -T db sh -c "psql -U appuser -d appdb < /backups/backup.sql"



Output:

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



Command:

docker compose exec -T db psql -U appuser -d appdb -c "SELECT \* FROM notes;"



Output:

&#x20;id |    text

\----+-------------

&#x20; 1 | first note

&#x20; 2 | second note

(2 rows)



===== Step 4.7: Scaling strategy =====



Note: assignment mein docker-compose scale likha hai. Naye Docker Compose mein woh command hata di gayi hai, us ki jagah --scale flag hai jo wahi kaam karta hai.



Command:

docker compose up -d --scale web=3



Output:

\[+] up 4/4

&#x20;✔ Container assignment2-part2-compose-web-1 Running   0.0s

&#x20;✔ Container assignment2-part2-compose-db-1  Running   0.0s

&#x20;✔ Container assignment2-part2-compose-web-3 Started   0.6s

&#x20;✔ Container assignment2-part2-compose-web-2 Started   0.4s





Command:

docker compose ps



Output:

NAME                              IMAGE                          COMMAND                  SERVICE   CREATED          STATUS          PORTS

assignment2-part2-compose-db-1    assignment2-part2-compose-db   "docker-entrypoint.s…"   db        20 hours ago     Up 20 hours     5432/tcp

assignment2-part2-compose-web-1   assignment2-part2-compose-web  "python app.py"          web       20 hours ago     Up 20 hours     0.0.0.0:8002->5000/tcp, \[::]:8002->5000/tcp

assignment2-part2-compose-web-2   assignment2-part2-compose-web  "python app.py"          web       7 seconds ago    Up 7 seconds    0.0.0.0:8003->5000/tcp, \[::]:8003->5000/tcp

assignment2-part2-compose-web-3   assignment2-part2-compose-web  "python app.py"          web       7 seconds ago    Up 6 seconds    0.0.0.0:8004->5000/tcp, \[::]:8004->5000/tcp







Command:

8002..8004 | ForEach-Object { "Port $\_ -> " + (curl.exe -s "http://localhost:$\_/whoami") }



Output:

Port 8002 -> Served by container: dd3fbe5489ce

Port 8003 -> Served by container: 10b1a7b46ee7

Port 8004 -> Served by container: 939182b6b7af







Screenshots: screenshots/scale-8002.png, screenshots/scale-8003.png, screenshots/scale-8004.png



NAME                                  SERVICE      STATUS                      PORTS

assignment2-part2-compose-cadvisor-1  cadvisor     Up 5 minutes (healthy)      0.0.0.0:8080->8080/tcp, \[::]:8080->8080/tcp

assignment2-part2-compose-db-1        db           Up 20 hours                 5432/tcp

assignment2-part2-compose-grafana-1   grafana      Up 5 minutes                0.0.0.0:3000->3000/tcp, \[::]:3000->3000/tcp

assignment2-part2-compose-prometheus-1 prometheus  Up 5 minutes                0.0.0.0:9090->9090/tcp, \[::]:9090->9090/tcp

assignment2-part2-compose-web-1       web          Up 20 hours                 0.0.0.0:8002->5000/tcp, \[::]:8002->5000/tcp

assignment2-part2-compose-web-2       web          Up 33 minutes               0.0.0.0:8003->5000/tcp, \[::]:8003->5000/tcp

assignment2-part2-compose-web-3       web          Up 33 minutes               0.0.0.0:8004->5000/tcp, \[::]:8004->5000/tcp





Prometheus targets (http://localhost:9090/targets):



\- cadvisor: 1/1 up

\- prometheus: 1/1 up

\- web: 3/3 up (172.18.0.5:5000, 172.18.0.3:5000, 172.18.0.4:5000)





Screenshot: screenshots/prometheus-targets.png



Grafana setup:



\- Grafana http://localhost:3000 par khula (login admin).

\- Data source: Prometheus, URL http://prometheus:9090, Save \& test successful

\- Dashboard ID 14282 (cAdvisor)  

\-

Screenshots: screenshots/grafana-datasource.png, screenshots/grafana-import-nodata.png, screenshots/grafana-dashboard.png, screenshots/prometheus-targets.png, screenshots/prometheus-web-requests.png, screenshots/prometheus-memory.png







