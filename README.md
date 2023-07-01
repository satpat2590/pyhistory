# pyhistory
Tackling through my long-anticipated history amalgamation through this stack: Python (Flask), MySQL, and Langchain!

## Overview:

In pursuing lofty ambitions, I decided to make this one particularly grand. I want to create a functional full-stack project which will 
use a MySQL database to store historical information: { event_name, year, synopsis, parent_event }. In doing so, I can envision a large collection of 
historical events and their significance in the grand scheme of time! 

To start, I'll have a basic application which is able to feed the database scheme to any LLM using Langchain (or LlamaIndex). The AI will 
then list out a bunch of events, making sure that all of the schema information is evident within the response itself. Sadly, great LLMs with historical
information capabilities are only present in GPT-4 (local versions are too small to do anything but summarization) which costs money. 

Once I find a job, I will turn this History AI into a thing! Meanwhile, I'll be assembling and polishing this stack without the use of Langchain. 

There will be an REST API developed which will allow anyone to perform CRUD operations to view the data on the frontend. However, a majority of
the data will be entered initially through functions which will call MySQL commands to perform CRUD operations. 

Here's the outline of the repository: 

Instead of running everything via the host computer, I decided to utilize docker-compose to handle multiple containers simultaneously on the same network. 

Make sure to download Docker through the website here: [Docker for Dummies!](https://www.docker.com/)

OR, you can use a package manager such as 'apt' or 'snap' to install it. Instructions can be found online for your OS and version!  

### Dockerfile 

Within the pyhistory/Dockerfile, we're initializing a python:<version> docker image and performing a few operations before turning it into a new image. Think of a Dockerfile
as essentially pre-processing the image so that it can have custom capabilities. 

Here are the custom additions in case you're feeling a tad lazy today and don't want to check out the super sweet Dockerfile I made: 

1. Installing python modules specified via pyhistory/pymysql/requirements.txt 
2. Installing MySQL CLI for use within the docker container (after running the newly created image from the Dockerfile) 
3. EXPOSE 80 essentially says to expose that port number from the container to the host 
4. CMD is the command that gets run whenever you run the docker image and turn it into a container 
    1. In this case, you're running 'tail -f /dev/null' which is essentially running the container forever unless stopped by force (docker stop or docker-compose down) 

All details for Dockerfiles can be found here: [Dockerfile for Dummies!](https://docs.docker.com/engine/reference/builder/)

### Docker Compose

Within the pyhistory/docker-compose.yml file, we create a configuration to start up a network of services. A service in docker, put simply, is a container which is run 
either with the use of a Dockerfile (which generates the new image), or by specifying the docker image manually. 

All of these service containers are run on the same network, which you have vast control over. I won't get into the meat of networks in docker-compose, because even I don't
have the slightest clue beyond the basics, but here is a breakdown of this particular docker-compose.yml file: 

We'll break this down by service so that you get a better idea of what is actually happening (hopefully) 

#### App 
```bash
  app: 
    depends_on: 
      - db 
    build: .
    environment: 
      - DATABASE_URL=mysql+mysqldb://${MYSQL_USER}:${MYSQL_PASSWORD}@db/${MYSQL_DATABASE}?charset=utf8mb4
    networks:
      - backend
```

The 'app' service (you can name this whatever you want) is configured above. 

1. 
The first configuration takes in a 'depends_on' value, which is essentially saying: 

"What other services does this one depend on?" OR "What services do I need to use in order to successfully complete my program (task)?" 

In this case, it is the 'db' service which we'll cover soon. This is obvious, as our application ('app') depends on the database ('db') to utilize CRUD operations through
APIs. 

2. 
'build' asks you: "If there is a Dockerfile which can build the image for this service (container), there where is it located?" 

To which you reply, "." (or the relative directory, pyhistory/ in this case) 

3. 
'environment' essentially says: "Are there any environment variables you need to use within the container that you don't want to specify within an .env file or through 
a custom means? Define them here!" 

In here we have one env variable called "DATABASE_URL" which also has this funny notation "${insert variable name here lol}". 

This funny notation is to call any environment variables on your HOST MACHINE. You can either define them for use in here through a .env file in the 
project directory, or have it defined systemwide using the notation (for Linux): 
```bash
export NAME=VALUE
```
And then call the variable within any file as "${NAME}"  

4. 
'networks' defines the network that your service is going to fall under. If you don't specify 'network', or remove this portion of the configuration, then your service
won't be under the 'backend' service, but rather one defined by the root directory (i.e 'pyhistory-default', etc...) 

Be careful if utilizing custom networks for other services. If you specify a custom service for one service but not the other, then they WON'T be within the same network, 
which may cause synchronization issues. 

#### DB
```bash
  db: 
    image: mysql:latest
    volumes: 
      - db_data:/var/lib/mysql 
    restart: always
    environment: 
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    ports:
      - '3307:3306'
    networks:
      - backend 
```
We've already covered some of the configuration details in 'app' so we can just gloss over the details here: 

1. 
'image' asks you: "Which docker image do you want to use for this service (container)?" Remember, the format is "<Docker Image>:<Version>" 

2. 
'volumes' asks you: "Are there any volumes (files, folders) that you want to map to a place within the container?" In this case, 'db_data' is a Docker-managed volume
which is persisted through the running docker-compose network ONLY. In other words, 'db_data' does not exist on your host machine, but simply shared between all services
utilizing the same network (in this case, 'backend'). 

Any MySQL database changes are persisted through the file '/var/lib/mysql' in the 'db' service (container) and by principle of volume mounting, also changed within the 
'db_data' which is also shared by the 'app' service. 

More information on volumes can be found here! [Volumes for Dummies!](https://docs.docker.com/storage/volumes/)

3. 
'restart'! To be honest, no idea, but people say it's good practice to set to 'always' when using a database as a service. 

Here are more technical details: [Container Death & Resurrection](https://sreeninet.wordpress.com/2017/08/15/docker-features-for-handling-containers-death-and-resurrection/)

4. 
'ports' maps a port on your host computer to one on the container. So basically: <host_port>:<container_port> 

You can choose to expose ports as well, which means make some ports available from the container to the host. 


## Running this Bad Boy 

### First Method
```bash
docker-compose up --build 
```

Go into a new terminal once the prior command is hanging. Check if containers are running by typing 'docker ps' 
and making sure there are two services running with a mysql image on one and a python image on another. 

If correct, continue:
```bash
docker exec -it <container_name> bash 
```

This should run a new terminal for you in the same window, but within the docker container. 
Repeat the 'exec' command for the other container in another terminal window, and you should be connected to both! 
Congratulations!

### Second Method
```bash
chmod +x build.sh && ./build.sh 
```

This command should run the 'docker-compose up --build -d' command, which does the same as above, but runs in detached mode, 
which means you can reuse the terminal to 'exec' into a running container. 

However, in the build.sh script, there's already a method to open two new terminals and run the containers in an interactive bash shell. 

Congratulations! You should be within the containers now. 

*Note: If you can't run the 'gnome-terminal -- [executable]' command then try finding your terminal type first through here (for Ubuntu) [Ubuntu/Linux Terminal Checker](https://askubuntu.com/questions/640096/how-do-i-check-which-terminal-i-am-using) and then run the corresponding command found here: [New Terminal Commands](https://askubuntu.com/questions/46627/how-can-i-make-a-script-that-opens-terminal-windows-and-executes-commands-in-the)* 

*Additional Note: The 'docker exec' commands runs the docker container using the container name found via 'docker ps'. In order to create your own docker container name, simply go into the pyhistory/docker-compose.yml file and add the field 'container-name' to both services, and then define them as you wish. Make sure to also change the container name argument within the 'docker exec' command in the pyhistory/build.sh file*

### Shutting Down Docker (Gracefully)

When you're done using the containers, simply call 'exit' in the command line for the container terminals, and then call
```bash
docker-compose down
```

If you don't make any changes to the containers, then on subsequent service spin-ups, you can omit the '--build' flag from
```bash
docker-compose up --build 
```





