""" Utility module to help run a bot programmatically. """
from __future__ import absolute_import
import logging
import os
from gevent import monkey

monkey.patch_all()

try:
    from typing import Any, Union
except ImportError:
    # just give up on typing...
    Any = None
    Union = None

# imports from disco (if moved to the top, they will probably break
# due to requiring `gevent`'s monkey patching for async)
from disco.client import Client, ClientConfig       # noqa: E402
from disco.bot import Bot, BotConfig                # noqa: E402
from disco.util.logging import setup_logging        # noqa: E402
from disco.gateway.sharder import AutoSharder       # noqa: E402


def bot_creator(config=None, bot=True, autosharded=False, process_config_file=True, **kwargs):
    # type: (dict, bool, bool, bool, **Any) -> Union[Bot, Client, AutoSharder]
    """
    Create a bot object and return it to be run without the cli. The config overrides in the following way:

    `kwargs` > `config` > config file

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
    process_config_file : bool
        Whether to check for a `config.json` / `config.yaml` and use that as a base (which then
        updates them with `config` and `kwargs`).

    Yields
    -------
    :class:`disco.bot.bot.Bot` or :class:`disco.gateway.sharder.AutoSharder` or :class:`disco.client.Client`
        A bot with all the configuration specified.
    """
    dict_config = config or {}
    dict_config.update(kwargs)

    if process_config_file:
        if os.path.exists('config.json'):
            config = ClientConfig.from_file('config.json')
        elif os.path.exists('config.yaml'):
            config = ClientConfig.from_file('config.yaml')
        else:
            config = ClientConfig()

    config.__dict__.update(dict_config)

    if autosharded:
        return AutoSharder(config)

    setup_logging(level=getattr(logging, config.log_level.upper()))

    client = Client(config)

    if hasattr(config, 'bot'):
        bot_config = BotConfig(config.bot)
        return Bot(client, bot_config)
    elif bot:
        bot_config = BotConfig()
        return Bot(client, bot_config)
    else:
        return client
