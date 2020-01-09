import dialogflow
import sys
import os
from matrix_client.client import MatrixClient, Room
from matrix_client.api import MatrixRequestError
import yaml
import re


def detect_intent(project, session_id, text, language_code):
  session_client = dialogflow.SessionsClient()
  session = session_client.session_path(project, session_id)

  query_input = dialogflow.types.QueryInput(
      text=dialogflow.types.TextInput(text=text, language_code=language_code))
  response = session_client.detect_intent(
      session=session, query_input=query_input)

  return response.query_result.fulfillment_messages


class Bot:

  def __init__(self, homeserver, userID, password, ownerID, dialogflow_project):
    self.ownerID = ownerID
    self.userID = userID
    self.client = MatrixClient(homeserver)

    token = self.client.login(username=userID, password=password)

    self.project = dialogflow_project
    rooms = self.client.get_rooms()
    for name, room in self.client.get_rooms().items():
      room.add_listener(self.onEvent)

  def report_mainloop_error(self):
    pass

  def run(self):
    self.client.add_invite_listener(self.accept_invite)
    while True:
      try:
        self.client.listen_forever()
      except KeyboardInterrupt:
        raise
      except:
        self.report_mainloop_error()

  def accept_invite(self, room_id, state):
    self.client.join_room(room_id)
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(self.project, room_id)
    query_input = dialogflow.types.QueryInput(
        event=dialogflow.types.EventInput(name='WELCOME', language_code='en'))

  def onEvent(self, room, event):
    if event['sender'] != self.userID:
      print("New event in room {} : {}".format(room, event))
      if event['type'] == "m.room.message" and event['content']['msgtype'] == "m.text":
        if event['sender'] == self.ownerID:  # admin commands
          leaveCommand = re.match("!leave (.+)", event['content']['body'])
          if leaveCommand:
            self.client.get_rooms()[leaveCommand.group(1)].leave()
        response = detect_intent(self.project, room.room_id, event[
                                 'content']['body'], 'en')
        print("Got DialogFlow response: {}".format(response))
        for message in response:
          for text in message.text.text:
            room.send_text("{}".format(text))

if __name__ == "__main__":
  with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

  bot = Bot(cfg['matrix']['homeserver'], cfg['matrix']['user_id'], cfg['matrix'][
            'token'], cfg['matrix']['owner_id'], cfg['dialogflow']['project'])
  bot.run()
