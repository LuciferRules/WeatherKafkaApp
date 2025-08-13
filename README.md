
### Enable Virtual Machine Platform for Docker Desktop
```bash
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
````

### Run Redpanda on docker
```bash
## Optional : remove the container if exist
docker rm redpanda-1

## Run
docker run -d --pull=always --name redpanda-1 -p 8081:8081 -p 8082:8082 -p 9092:9092 -p 9644:9644 docker.redpanda.com/redpandadata/redpanda:latest rpk redpanda start --node-id 0 --dev-mode --kafka-addr 0.0.0.0:9092 --rpc-addr 0.0.0.0:33145 --pandaproxy-addr 0.0.0.0:8082 --schema-registry-addr 0.0.0.0:8081 --advertised-kafka-addr localhost:9092
```

### Install and Configure Quix CLI using PowerShell
```powershell
iwr https://github.com/quixio/quix-cli/raw/main/install.ps1 -useb | iex
quix --version
```

### Connect local Quix context to local Redpanda broker at port 19092
```bash
quix contexts broker set localhost:19092 --enable
```

### Install pre-requisites
```powershell: initialize quix
## This created quix.xml, which is place for your pipeline definition and later we will add our services there.
quix local init
quix local pipeline up
```

### Create python virtual env
```bash
python -m venv venv
source venv/Scripts/activate
```

``` powershell: Install library (quixstreams)
pip install -r requirements.txt 
```

### Run producer or consumer
```bash
python producer.py
```
```bash
python consumer.py
```

### Push to github repo
```bash
git add .
git commit -m "Initial commit of the weather application"
git remote add origin https://github.com/LuciferRules/WeatherKafkaApp.git
git push -u origin master
```