Firstly you need to update the Linux kernel parameter `vm.max_map_count` to increase the maximum number of memory map.
You can do this permanently to your WSL distribution by running this (in Windows terminal):
```
wsl -d <YourDistroName> -u root sysctl -w vm.max_map_count=262144
```

Or if you only want to update the current WSL session and not permanently, you can run this:
```bash
sudo sysctl -w vm.max_map_count=262144
```


# (Newest) How to run

1. Core:
Get Python 3.13:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev
```

(re)create venv:
```bash
rm -rf venv
python3.13 -m venv venv
source venv/bin/activate
```

Run home assistant setup:
```bash
./script/setup
```

Then install the requirements:

```bash
pip install -r requirements_all.txt
```

Run it:
```bash
hass -c config
```


2. Frontend
Get Python 3.13:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev
```

(re)create venv:
```bash
rm -rf venv
python3.13 -m venv venv
source venv/bin/activate
```

Run home assistant setup:
```bash
./script/setup
./script/bootstrap
```

Run it:
```bash
./script/develop
```

# If you want to run tests localhost
Get Python 3.13:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev
```

(re)create venv:
```bash
rm -rf venv
python3.13 -m venv venv
source venv/bin/activate
```


Run home assistant setup:
```bash
./script/setup
```

Then install the requirements:

```bash
pip install -r requirements_all.txt
```

And then you can run the tests with:

```bash
pytest tests/
```

# If you want to run tests
If you only want to run tests you can do the following:

```bash
docker build -f Dockerfile.dev -t ha-dev:latest .
```

```bash
docker run -it --rm \
    -v $(pwd):/workspaces \
    -p 8123:8123 \
    ha-dev:latest \
    /bin/bash
```

Then inside the container run:

```bash
script/setup
```

Then activate the virtual environment:

```bash
source .venv/bin/activate
```

Then install the requirements:

```bash
pip install -r requirements_all.txt
```

And then you can run the tests with:

```bash
pytest tests/
```

# If you want persistent
Using docker compose you have the containers up and down as you wish and is saved across runs.

Setup the Sonarqube and it's corresponding database with the compose file `./sonarqube-compose.yml`:
```bash
docker compose -f sonarqube-compose.yml up
```

When those are started you can login the dashboard at `http://localhost:9000/` (Original credentials is admin and admin, then change your password)
Then you need to go into top right corner of your profile --> My Account --> Security
Then generate a token (Global Analysis Token) and save the TOKEN generated to be used for the scanner.

Then you can run the scanner with this image:
```bash
docker run --rm \
  --network home-assistant-core-ht25_sonarnet \
  -v <PROJECT_DIR>:/usr/src \
  -e SONAR_HOST_URL=http://sonarqube:9000 \
  -e SONAR_TOKEN=<SONAR_TOKEN> \
  sonarsource/sonar-scanner-cli
```

If you want to run the sonar-scanner connected to sonarcloud:
```bash
docker run --rm \
  -v /home/emhs21/home-assistant-core-ht25:/usr/src \
  -w /usr/src \
  -e SONAR_HOST_URL="https://sonarcloud.io" \
  -e SONAR_TOKEN="785f52ddfc7aff8c64db2442729ef3af72eb90ee" \
  sonarsource/sonar-scanner-cli \
  -Dsonar.projectKey=Hnsson_home-assistant-core-ht25 \
  -Dsonar.organization=hnsson \
  -Dsonar.branch.name=emil-duplicate-blocks
```

And change the project directory to the location of the directory, and also change the sonar token to what
you generated in the dashboard.

The scanner can run for about ~7 minutes and when it's done it will automatically remove itself and post a link in the terminal
like this: `ANALYSIS SUCCESSFUL, you can find the results at: http://sonarqube:9000/dashboard?id=home-assistant-core-ht25`, which you
can access if you swap the `sonarqube` with `localhost`. If you don't see that its done yet, just wait for some time.
