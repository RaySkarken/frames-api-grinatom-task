# Test task for "Grinatom"
## Setup instructions
### develop
- `git clone https://github.com/RaySkarken/frames-api-grinatom-task.git` - 
  clone repo
- `pip install -r requirements.txt` - install requirements(poetry)
- `poetry shell` - enter a virtual environment
- `poetry install` - install required modules
- `export $(cat .env.dev | egrep -v "(^#.*|^$)" | xargs)` - export environment 
  variables
- `docker-compose -f docker-compose.dev.yml up -d` - run postgres inside a docker container
- `uvicorn src.main:app --host 0.0.0.0 --port 8000` - run server

### production
- `git clone https://github.com/RaySkarken/frames-api-grinatom-task.git` - clone repo
- `docker-compose -f docker-compose.prod.yml up` - run server inside a docker container

## Description
This is my solution for test task for selection for an internship

## Progress
- [ ] create backbone server
- [ ] create authorization with OAuth2
- [ ] create endpoint for frames posting
- [ ] create endpoint for frames getting
- [ ] create endpoint for frames deleting
- [ ] create docker-compose files
