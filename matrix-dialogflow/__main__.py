print('matrix-dialogflow/__main__.py executed')

import yaml
from . import Bot

with open("config.yml", 'r') as ymlfile:
  cfg = yaml.load(ymlfile)

  bot = Bot(cfg['matrix']['homeserver'], cfg['matrix']['user_id'], cfg['matrix'][
            'token'], cfg['matrix']['owner_id'], cfg['dialogflow']['project'])
  bot.run()
