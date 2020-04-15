""" Utility module to help run a bot programmatically. """
from __future__ import absolute_import
import logging
from gevent import monkey

monkey.patch_all()

try:
    from typing import Any, Union
except ImportError:
    # just give up on typing...
    Any = None
    Union = None

# imports from disco (if moved to the top, they will probably break
# due to requiring `gevent`'s monkey patching for asynchronous)
from disco.client import Client, ClientConfig       # noqa: E402
from disco.bot import Bot, BotConfig                # noqa: E402
from disco.util.logging import setup_logging        # noqa: E402
from disco.gateway.sharder import AutoSharder       # noqa: E402


def bot_creator(config=None, bot=True, autosharded=False, **kwargs):
    # type: (dict, bool, bool, **Any) -> Union[Bot, Client, AutoSharder]
    """
    Create a bot object and return it to be run without the cli.

    Parameters
    -----------
    config : dict
        The configuration to use. The configuration can also be passed through using
        keyword args, for example: `bot_creator({'bot':{'commands_prefix':'!'}}, token=TOKEN)`
    bot : bool
        Whether to return a :class:`disco.bot.bot.Bot` or a :class:`disco.client.Client`
        `True` for `Bot`, `False` for `Client`. This only matters if the config has no `bot` key.
    autosharded : bool
        Whether to automatically shard the bot.

    Yields
    -------
    :class:`disco.bot.bot.Bot` or :class:`disco.gateway.sharder.AutoSharder` or :class:`disco.client.Client`
        A bot with all the configuration specified.
    """
    config = config or {}
    config.update(kwargs)

    # Change the dictionary configuration to disco's proprietary Config
    config = ClientConfig(config)

    # Magical auto-sharding that you will eventually want
    if autosharded:
        return AutoSharder(config)

    # Setup logging based on the configured level
    setup_logging(level=getattr(logging, config.log_level.upper()))

    # Create the bot/client
    client = Client(config)

    # if there exists a config for the bot, then return the bot, else return the client.
    if hasattr(config, 'bot'):
        bot_config = BotConfig(config.bot)
        return Bot(client, bot_config)
    elif bot:
        bot_config = BotConfig()
        return Bot(client, bot_config)
    else:
        return client
