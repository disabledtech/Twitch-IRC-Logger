from twitch_irc_bot import TwitchBot
from configparser import ConfigParser


def main():
    config = ConfigParser()
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


if __name__ == '__main__':
    main()
