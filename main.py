# TODO configure autoflake, isort, and black
#  add pre-commit hooks
#  add pipelines for running linters checks and tests
from dataclasses import dataclass, field
from typing import Sequence

import discord
from discord.ext import commands
from jinja2 import Environment, FileSystemLoader

from app.vos import ScheduledEventVO
from config import TEMPLATES_DIRECTORY, get_settings
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


@dataclass(frozen=True, slots=True)
class GenerateEventBoardDTO:
    discord_invite: str  # TODO could in theory be a URL object with validation
    locale: str


@dataclass(frozen=True)
class GenerateEventBoardAsHTML:
    guild: discord.Guild
    _template_name: str = field(init=False, default="event_board.html")

    async def execute(self, dto: GenerateEventBoardDTO) -> str:
        events = [
            ScheduledEventVO(
                name=event.name,
                start_date=event.start_time,
                end_date=event.end_time,
                place=event.location,
                remarks=event.description,
                locale=dto.locale,
            )
            for event in sorted(self.guild.scheduled_events, key=lambda x: x.start_time)
        ]
        environment = Environment(
            loader=FileSystemLoader(TEMPLATES_DIRECTORY),
            autoescape=True,
        )
        template = environment.get_template(self._template_name)
        html_event_board = template.render(
            events=events, discord_invite=dto.discord_invite, locale=dto.locale
        )
        return html_event_board


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

    html_event_board = await GenerateEventBoardAsHTML(app_guild).execute(
        GenerateEventBoardDTO(
            discord_invite=settings.discord_invite, locale=settings.html_locale
        )
    )
    # TODO replace with pushing to a remote server
    settings.html_output_path.parent.mkdir(exist_ok=True)
    with settings.html_output_path.open(
        "w",
    ) as f:
        f.write(html_event_board)

    await MessageAdminsOnMissingTemplates(app_guild).execute()

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
