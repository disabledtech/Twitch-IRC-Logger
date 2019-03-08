from twitch_irc_bot import TwitchBot
from configparser import ConfigParser
import os


def main():

    config = ConfigParser()

    # Try to find the config file, if it does not exist, create one.
    if not os.path.exists(os.path.join(os.getcwd(), 'config.ini')):

        print("Config file not found. Creating one...")

        __create_config(config)

        print("Config file created. Please fill out the settings.")

        exit(0)

    config.read('config.ini')

    username = config['TWITCH_BOT_SETTINGS']['username']
    token = config['TWITCH_BOT_SETTINGS']['token']
    client_id = config['TWITCH_BOT_SETTINGS']['client_id']
    channel_limit = config['TWITCH_BOT_SETTINGS'].getint('channel_limit')


    # Initialize bot.
    bot = TwitchBot(username=username,
                    token=token,
                    client_id=client_id,
                    limit=channel_limit)

    # Runs the bot until user interrupts it.
    bot.run()


def __create_config(config):
    """
    Creates a fresh config file with the needed parameters.

    :param config: a ConfigParser() object.
    """

    config['TWITCH_BOT_SETTINGS'] = {'username': '',
                                     'token': '',
                                     'client_id': '',
                                     'channel_limit': ''}

    with open('config.ini', 'w') as new_config_files:

        config.write(new_config_files)


if __name__ == '__main__':
    main()
