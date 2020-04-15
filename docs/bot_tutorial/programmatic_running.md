# CLI-less Running

In certain environments, it is either impossible 
to get to a console, or completely impractical. 
Even if you are not using said environments, being 
able to start your bot in a python file is very 
useful for config options that require functions.

Disco has the `util.runner` module just for this task. Just simply:
```py
from disco.util import runner

bot = runner.bot_creator({
    'token': 'YOUR.TOKEN.HERE',
    'bot': {
        'plugins': ['plugins.tutorial']}  # this can be anything
})

bot.run_forever()
```

Now you just need to `python main.py`, and the bot starts! Nice!

### Custom prefixes

One of the main reasons why you may want to use this method of 
starting your bot is that now you can give functions for configuration.
That is especially useful if, for example, you really want server-specific 
prefixes, or prefixes based on the user. All you need to do is put
a function which takes the message object and returns an array of strings.

For example, this bot will have different prefixes for the owner vs
a random user:
```py
from disco.util import runner

TOKEN    = 'YOUR_TOKEN_HERE'
OWNER_ID = 'YOUR_USER_ID_HERE'


def prefix_getter(message):
    if str(message.author.id) == OWNER_ID:
        return ['@']
    else:
        return ['!']


bot = runner.bot_creator({
    'token': TOKEN,
    'bot': {
        'commands_prefix_getter': prefix_getter,
        'require_mention': False,
        'plugins': ['plugins.tutorial']  # this can be anything
    }
})

bot.run_forever()
```