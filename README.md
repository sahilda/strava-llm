## Install
```
python3 -m venv .venv
source .venv/bin/activate
pip install python-dotenv langsmith chainlit openai llama_index
```

## Setup
* add `.env` file
* grab your strava activites using the `strava_client.py` script
* Add any training plans to `data/` directory
* If you add/remove files to your `data/` directory, you'll need to remove the index by deleting the `data_index` directory and its contents.

## Run the app
```
chainlit run app.py -w
```

## What is this?
Strava training helper
