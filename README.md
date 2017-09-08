# Installation

## Requirements

System requirements:

* Python 3
* TKinter

```
sudo apt-get install python3-pip
sudo apt-get install python3-tk
```

Python requirements:

* Slack client

```
sudo -H pip3 install setuptools
sudo -H pip3 install slackclient
```

Then get the project and enter it:

```
git clone https://github.com/jmleroux/akeneo-video-conf-bot.git
cd akeneo-video-conf-bot
```

# Usage

```
python3 zoom2slack.py
```

Or with the executable shell launcher:

```
./run.sh
```

Screenshot before clicking the button:

![Screen 01](doc/img/screenshot-01.png)

Screenshot after:

![Screen 02](doc/img/screenshot-02.png)

### Resources:

* https://github.com/slackapi/python-slackclient
