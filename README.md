# Installation

## Requirements

System requirements:

* Python 3
* Gtk Object

```
sudo apt-get install python3-pip
sudo apt-get install python3-gi
```

Python requirements:

* Slack client

```
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

## Screenshots:

![Start](doc/img/start.png)

Message sent:

![Sent](doc/img/sent_to_channel.png)

### Resources:

* https://github.com/slackapi/python-slackclient
* https://developer.gnome.org/gtk3/3.22/gtk.html
