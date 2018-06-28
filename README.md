# matrix-dialogflow

Usage:

```
$ git clone https://gitlab.com/vurpo/matrix-dialogflow
$ cd matrix-dialogflow
$ virtualenv venv --python=python3
$ pip install -r requirements.txt
$ cp config.yml.sample config.yml
```

Now edit `config.yml` with all the correct parameters for your Matrix bot user, and your DialogFlow agent (also, remember to set up your Google Cloud credentials locally to allow the bot to access your DialogFlow API)

```
$ python -m matrix-dialogflow
```