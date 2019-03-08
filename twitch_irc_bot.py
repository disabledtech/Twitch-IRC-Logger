import socket
import time
import requests
from codecs import decode
import os

import logging
import logging.handlers

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

# Set our logger's time format to UTC
logging.Formatter.converter = time.gmtime

# Where logs will be stored.
logs_folder = os.path.join(os.getcwd(), 'logs/')

# Make the folder if it does not exist.
if not os.path.exists(logs_folder):
    os.mkdir(logs_folder)

# Set up the logger. Log files will rotated saved every 10 minutes.
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.handlers.TimedRotatingFileHandler(logs_folder + 'chat.log',   # Active log name
                                                                        when='M',
                                                                        interval=10,  # Log rotation in min.
                                                                        encoding='utf-8')])


class TwitchBot(object):
    """
    A bot which joins multiple Twitch IRC channels and records
    their messages to a rotating log file. The channels it joins
    are from a list of the streams with the most current viewers
    retrieved from the Twitch API. The number of streams to log
    can be configured up to a max. of 100.
    """

    def __init__(self, username, token, client_id, game='', refresh_interval=60, limit=25):
        """
        Initializes TwitchBot

        :param username:    What the bot will call itself when joining the IRC server. Do not use the same
                            name as a popular streamer, it will break the script.
        :param token:       The OAuth token used to join the Twitch IRC.
        :param client_id:   The client_id of your Twitch dev. application. See: https://dev.twitch.tv/docs/v5
        :param game:        The game that you want all streams to be playing. e.g. 'Overwatch'. Default: Any game ('').
        :param refresh_interval: How often (in seconds) to call update() and get a new list of top streams. Default: 60
        :param limit:       The maximum numbers of streams to join. Default: 25 Max: 100
        """

        self.__server = 'irc.chat.twitch.tv'  # Twitch IRC IP Address
        self.__port = 6667                    # Twitch IRC Port
        self.username = username
        self.token = token
        self.client_id = client_id

        self.refresh_interval = refresh_interval
        self.game = game
        self.limit = limit

        # Get an initial list of streams.
        self.channel_list = self.__get_top_streamers()

        # Connect to the Twitch IRC.
        self.__connect()

    def __connect(self):
        """
        Connect to the twitch.tv IRC server and then JOIN each IRC channel in self.channel_list

        :return: None
        """

        self.sock_connection = socket.socket()
        self.sock_connection.connect((self.__server, self.__port))

        self.sock_connection.send('PASS {}\n'.format(self.token).encode('utf-8'))
        self.sock_connection.send('NICK {}\n'.format(self.username).encode('utf-8'))

        # Call __join_channel() for all channels in the channel_list
        for channel in self.channel_list:

            self.__join_channel(channel)

    def __join_channel(self, channel):
        """
        Joins the specified twitch.tv IRC channel
        :param channel: The twitch.tv IRC channel to join. Usually (always?) the caster's channel name.

        :return: None
        """

        self.sock_connection.send('JOIN #{}\n'.format(channel).encode('utf-8'))

    def __leave_channel(self, channel):
        """
        Leaves the specified twitch.tv IRC channel
        :param channel: The twitch.tv IRC channel to leave. Usually (always?) the caster's channel name.

        :return: None
        """

        self.sock_connection.send('PART {}\n'.format(channel).encode('utf-8'))

    def update(self):
        """
        Updates which channels we're logging. Fetches a new list of
        streams from __get_top_streamers() and compares it with our current
        list of streams. Compares the lists to get which streams have
        entered/left the top 100. Calls __leave_channel/__join_channel on
        these lists as needed.

        :return: None
        """

        new_channels = self.__get_top_streamers()
        old_channels = self.channel_list

        # Compares the stream lists to find which streams to join/leave.
        channels_to_leave = list(set(old_channels) - set(new_channels))
        channels_to_join = list(set(new_channels) - set(old_channels))

        # Leave streams in not in top 100
        for channel in channels_to_leave:

            self.__leave_channel(channel)

        # Join streams new to the top 100
        for channel in channels_to_join:

            self.__join_channel(channel)

        # Update the list of channels we're currently in.
        self.channel_list = new_channels

    def run(self):
        """
        Run the script until user interruption.

        :return: None
        """

        # A flag used to determine if it'stime to call update().
        top_100_check = time.time()

        while True:

            try:

                # Get response from the IRC server
                try:

                    response = decode(self.sock_connection.recv(2048), encoding='utf-8')

                except UnicodeDecodeError:
                    # TODO Handle this better
                    # Sometimes this exception is raised, however it happens extremely
                    # rarely (< ~0.1%) and is not significant unless it is absolutely critical
                    # you do not miss anything. At the moment we simply skip over these errors.
                    continue

                # Sometimes in a busy channel many messages are received
                # in one 'response' and we need to split them apart. See
                # https://stackoverflow.com/q/28859961 for a longer and
                # more detailed explanation by someone else with the
                # same issue.
                #
                # All message end with '\r\n' so we can reliably count/split
                # them this way.

                line_count = response.count("\r\n")

                if line_count > 1:

                    messages = response.split("\r\n")

                    for single_msg in messages:

                        self.__log_message(single_msg)

                else:

                    self.__log_message(response)

                # Check if the time now is more than the refresh_interval + the
                # last time we checked the top 100.
                if time.time() > top_100_check + self.refresh_interval:

                    # Update the time we last checked to now.
                    top_100_check = time.time()

                    # Update our channel list.
                    self.update()

            # Shut down 'gracefully' on keyboard interrupt.
            except KeyboardInterrupt:

                self.__close_connection()

    def __get_top_streamers(self):
        """
        Gets the 100 channels with the most current viewers. Uses the param
        settings from initialization (self.game, self.limit) to determine
        which and how many streams to grab.

        :return: A list of channels in the top *self.limit* system currently.
        """

        # Parameters for the Twitch API request
        twitch_api_params = {
            'client_id': self.client_id,    # Required
            'api_version': 5,               # Required
            'game': self.game,              # Optional
            'limit': self.limit             # Optional, defaults to 25. Max is 100.
        }

        names = []

        # Request the JSON data from twitch.
        channel_list = requests.get('https://api.twitch.tv/kraken/streams/',
                                    params=twitch_api_params).json()

        # Extract channel names from the JSON data.
        for name in channel_list['streams']:
            names.append(name['channel']['name'])

        return names

    def __close_connection(self):
        """
        Close our socket connection.

        :return:
        """
        print('Exiting...')

        self.sock_connection.close()

        exit(0)

    def __log_message(self, response):
        """
        Save a valid message to your logs. A valid message is one that is
        NOT a PING from the server, IS greater than 0 in length, and
        does NOT contain our own name (such as those from the IRC
        server when we first join). Choosing the same *username* for
        the bot as a popular streamer will probably (100%) break the
        logging for said streamer's channel at best. I have no idea
        what a worst-case-scenario would be (disabled for 'impersonation'?).
        Investigate at your own discretion.

        :param response: A single message response from the server.
        :return:
        """

        # Send a PONG if the server sends a PING
        if response.startswith('PING'):

            self.sock_connection.send('PONG\n'.encode('utf-8'))

        elif len(response) > 0 and self.username not in response:

            logging.info(response.rstrip('\r\r\n'))