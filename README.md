# Deployment of Machine Learning based Web API using Docker
#### This is a Web application developed for tutorial purpose, Please watch [these YouTube Videos](https://www.youtube.com/playlist?list=PLOoVZ0jKCw7f4zgNrHUPjXDP1jAoz3Axm) for complete explanation.

![alt tag](https://github.com/pothabattulasantosh/Demo_App/blob/master/Screenshot_application-view.png)

### Before running this App:

##### 1.Since this app was developed in Ubuntu OS, please make sure you have Linux keranl based OS (Eg:Ubuntu,CentOS).
##### 2.Read Docker prerequisites (please visit [here](https://docs.docker.com/engine/install/)) and install Docker in your OS.

### To Run this APP:

##### 1. Clone this repo into your system
```bash
 $ git clone https://github.com/pothabattulasantosh/Demo_App.git
 ```
##### 2. Go to Demo_App directory
```bash
 $ cd Demo_App
 ``` 
##### 3. Now create a docker Build for this application.

```bash
 $ sudo docker-compose build
 ``` 
##### 4. Now Up the application.

```bash
 $ sudo docker-compose up
 
``` 
##### After few seconds you can access this Application at http://0.0.0.0:5000 or http://<your serverIP/DNS>:5000
