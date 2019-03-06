<h1 align="center">Twitch IRC Logger</h1>

<div align="center">
    A configurable <code>Python 3</code> bot which logs chat messages in the Twitch channels with the highest viewers.
</div>

<br/>

<div align="center">
  <a href="http://badges.mit-license.org">
    <img src="http://img.shields.io/:license-mit-blue.svg?style=flat-square)"
      alt="MIT Licence" />
  </a>
</div>

## Table of Contents
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Example](#example)
- [Support](#support)



---

## Prerequisites

<br/>

- Python 3.5 or newer.

- <a href="https://pypi.org/project/requests/" target="_blank">Requests</a> is used to get data on the most popular streamers online right now.
```
pip install requests
```

---
## Usage

<br/>

Fill out the settings in ```config.ini``` and then run ```run_bot.py```. Log files will be saved in the same directory as the script in a directory called ```logs```

### Config.ini Settings

| Parameter                     | Description |
| --------------------     | -------------| 
| `username`        | What the bot will call itself when joining the IRC server. Do not use the same name as a popular streamer, it *will* cause issues.| 
| `token`           | The Twitch IRC requires an OAuth token for authentication. See https://twitchapps.com/tmi/ to get your own token. |  
| `client_id`       | The Twitch API requires a ClientID for API access which we use to get a list of currently popular streamers. See https://dev.twitch.tv/docs/v5 to get your own client ID |
| `channel_limit `  | The number of IRC channels to join. Ex. If set to 20 the bot will join and log the 20 channels with the most viewers. *Max*: 100 |

<br/>

---

## Example

This will join the top *10* streamers with the name *john_logger_bot999*.

`config.ini`


`username = john_logger_bot999` <br/>
`token = oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` <br/>
`client_id = xxxxxxxxxxxxxxxxxxxxxxxxxxx` <br/>
`channel_limit = 10` <br/>

---

## Support

Reach out to me at one of the following places if you need help!

- Reddit at <a href="https://www.reddit.com/user/AntiHydrogen" target="_blank">`/u/AntiHydrogen`</a>
- Github at <a href="https://github.com/disabledtech" target="_blank">`disabledtech`</a>


---

## License

MIT License

Copyright (c) 2019 disabledtech

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

