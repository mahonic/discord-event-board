# EVENT BOARD

## SYNOPSIS
This is an app that generates a html file with information about future discord events. 
It uses `discord.py` to connect to a discord server, fetch data, and then generate an html file.
Output file is generated based on a template that can be modified.

## USAGE
### Docker (recommended)
This app is docker ready. Assuming docker and docker-engine are installed run `docker-compose up --build`.
Make sure to set `DISCORD_AUTH_TOKEN` and `GUILD_ID` environment variables.

### Locally (linux)
This app uses python `3.11`. Earlier version might work, but they're not tested.

This app uses poetry for managing dependencies. Ensure it's installed locally. 
1. Create a local environment with `python -m venv .venv`.
2. Activate virtual env `source .venv/bin/activate`
3. Install dependencies with `poetry install`
4. Provide environment variables
   1. create a .env file and put environment variables there
   2. *(alternatively)* prepend the command in the next step with them like so `DISCORD_AUTH_TOKEN="code" GUILD_ID="id" python main.py`
5. Run the app `python main.py`


## ENVIRONMENT VARIABLES (required)
* `DISCORD_AUTH_TOKEN` *str* - auth token of a bot
* `GUILD_ID` *str* - id of a guild the bot is supposed to retrive events from

## ENVIRONMENT VARIABLES (optional)
* `HTML_LOCALE` *str* default = `en_uk` - which language should be used for generating names in the output data (like weekdays)
* `HTML_OUTPUT_PATH` *str* default = `PROJECT_ROOT/output/output.html` - where to save generated html file
* `LOGS_DIRECTORY` *str* default = `PROJECT_ROOT/logs` - where logs should be saved
* `DISCORD_LOG_LEVEL` *str* default = `INFO` - what level of messages should be logged from the discord.py library
* `APP_LOG_LEVEL` *str* default = `INFO` - what level of messages should be logged from the app


