import uvicorn
from application import app
from pathlib import Path
from dotenv import dotenv_values

dotenv_path = Path('.env')
if dotenv_path:
    config = dotenv_values(dotenv_path)
else:
    config = dict()
    exit()

if __name__ == '__main__':
    uvicorn.run(app, host=config['DOMAIN'], port=int(config['PORT']))
