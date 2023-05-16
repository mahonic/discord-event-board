# TODO configure autoflake, isort, and black
#  add pre-commit hooks
#  add pipelines for running linters checks and tests
from dataclasses import dataclass
from typing import Sequence

import discord
from discord.ext import commands
from jinja2 import Environment, FileSystemLoader

from app.vos import ScheduledEventVO
from config import Settings, get_settings
from loggers import app_logger

intents = discord.Intents.default()
intents.message_content = True

# TODO ~~maybe~~ replace with discord.client - commands are not used as of now
bot = commands.Bot(intents=intents, command_prefix="$")
settings = get_settings()


def get_app_guild(guilds: Sequence[discord.Guild]) -> discord.Guild | None:
    for guild in guilds:
        if guild.id == settings.guild_id:
            return guild
    return None


@dataclass
class GenerateEventBoardAsHTML:
    guild: discord.Guild
    settings: Settings

    async def execute(self):
        events = [
            ScheduledEventVO(
                name=event.name,
                start_date=event.start_time,
                end_date=event.end_time,
                place=event.location,
                remarks=event.description,
                locale=settings.html_locale,
            )
            for event in sorted(self.guild.scheduled_events, key=lambda x: x.start_time)
        ]
        environment = Environment(
            # todo make a config variable or move the whole env to a separate file
            loader=FileSystemLoader("templates"),
            autoescape=True,
        )
        template = environment.get_template(
            "event_board.html"
        )  # TODO make a dict[enum, str] or other variable
        content = template.render(events=events)
        # print(content)
        with self.settings.html_output_path.open("w") as f:
            f.write(content)
        # TODO check scheduled events and generate a html file based on that
        #  use jinja templates - template.html


@dataclass
class MessageAdminsOnMissingTemplates:
    guild: discord.Guild

    async def execute(self):
        # TODO check for future events. If no events are scheduled notify guild admins somehow
        #  could be by @ing them on some channel - this needs permission for sending messages + preferably an option to specify in which channel to send messages
        #  or sending them a DM - this requires admins to allow non-friend dms
        #  or it could be an email or sms :shrug:
        #  it could also affect the exit code of the app so that the executor service will notify bot host
        pass


@bot.event
async def on_ready():
    app_logger.info(f"We have logged in as {bot.user}")
    for guild in bot.guilds:
        # TODO maybe make the bot leave non-app guilds
        app_logger.info(
            'Connected to guild (id={id}, name="{name}")'.format(
                id=guild.id, name=guild.name
            )
        )
    app_guild = get_app_guild(bot.guilds)
    if app_guild is None:
        raise ValueError(
            "Bot not connected to the app guild (id = {})."
            " Either the id is wrong or the bot is not present in the guild.".format(
                settings.guild_id
            )
        )
    await GenerateEventBoardAsHTML(app_guild, settings).execute()
    await bot.close()


# TODO add a tests to make sure the bot closes on any error
# TODO also add a test to make sure the bot closes when it completes it tasks without any errors
@bot.event
async def on_error(event_name, *args, **kwargs):
    """We don't want the bot to run forever - only to get scheduled events and then quit."""
    app_logger.exception(
        f'Unhandled exception raised by event "{event_name}" ({args=}, {kwargs=}). Stopping the bot.'
    )
    await bot.close()


@bot.command()
async def show_events(context: commands.Context):
    events_str = []
    for event in context.guild.scheduled_events:
        events_str.append(
            f"Event {event.name}"
            f"\n\t id = {event.id}"
            f"\n\t description = {event.description}"
            f"\n\t start time = {event.start_time}"
        )
    await context.send("\n\n".join(events_str))


def main():
    # Suppress the default configuration since we have our own
    bot.run(settings.discord_auth_token, log_handler=None)


if __name__ == "__main__":
    main()
