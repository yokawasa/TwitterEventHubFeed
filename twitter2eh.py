#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Yoichi Kawasaki'

import sys
import os
import argparse
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from azure.servicebus import ServiceBusService
import datetime
import json

### Global Defines
_TWITTER_EH_VERSION = '0.1.0'
_TWITTER_EH_CONFIG_FILE = 'twitter2eh.json'

def print_err(s):
    sys.stderr.write(u"[ERROR] {}\n".format(s))

def get_config(config_file):
    o ={}
    try:
        cf = open(config_file, 'r')
        o = json.load(cf)
    except IOError:
        print_err('Cannot Open {}'.format(config_file) )
    else:
        cf.close()
    return o

def generate_template(any_file):
    try:
        f = open(any_file,"w")
        f.write(
            "{\n"
            "    \"twitter_consumer_key\" : \"<Consumer Key for Twitter App>\",\n"
            "    \"twitter_consumer_secret\" : \"<Consumer Secret for Twitter App>\",\n"
            "    \"twitter_access_token\" : \"<Access Token for Twitter App>\",\n"
            "    \"twitter_access_secret\" : \"<Access Secret for Twitter App>\",\n"
            "    \"track_keywords\" : [\n"
            "        \"<Keyword or Hashtag>\",\n"
            "        \"<Keyword or Hashtag>\",\n"
            "        \"<Keyword or Hashtag>\"\n"
            "    ],\n"
            "    \"eventhub_namespace\" : \"<Event Hub Namespace>\",\n"
            "    \"eventhub_entity\" : \"<Event Hub Entity Name>\",\n"
            "    \"eventhub_sas_key\" : \"<Event Hub SAS Key Name>\",\n"
            "    \"eventhub_sas_value\" : \"<Event Hub SAS Value>\"\n"
            "}"
        )
    except IOError:
        print_err('Cannot Open {}'.format(any_file) )
    else:
        f.close

class EventHubListener(StreamListener):

    def __init__(self, entity, client, silient):
        self.entity = entity
        self.client = client
        self.silient = silient

    def on_data(self, data):
        try:
            dictData = json.loads(data)
            dictData["id"] = str(dictData["id"])
            print(dictData)
            self.client.send_event(self.entity, json.dumps(dictData))
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

def main():
    parser = argparse.ArgumentParser(description='This program streams feed from Twitter to EventHub')
    parser.add_argument(
        '-v','--version', action='version', version=_TWITTER_EH_VERSION)
    parser.add_argument(
        '--init', action='store_true',
        help='Create template client conf twitter2eh.json only if there is no existing one')
    parser.add_argument(
        '-c','--conf', default=_TWITTER_EH_CONFIG_FILE,
        help='Configuration file. Default:twitter2eh.json')
    parser.add_argument(
        '-s','--silent', action='store_true',
        help='silent mode - running the tool without displaying tweets json that you are streaming to your Event Hub')
    args = parser.parse_args()

    ### Args Validation
    config_file = _TWITTER_EH_CONFIG_FILE
    if args.init:
        # Initialize config file
        if not os.path.exists(config_file):
            generate_template(config_file)
            print ("Created template config file: {}".format(config_file))
        else:
            print_err("No action has done since config file already exist!: {}".format(config_file))
        quit()

    if os.path.exists(args.conf):
        config_file = args.conf

    if not os.path.exists(config_file):
        print_err(u"twitter2eh.json file doesn't exist: {0}\n"
                  u"Please speicify the file with --conf option\n".format(args.conf))
        print(parser.parse_args(['-h']))
        quit()

    c = get_config(args.conf)
    if "track_keywords" not in c:
        print_err("No track_keywords in config file!")
        quit()
    tracks = c['track_keywords']

    silent_mode = False
    if args.silent:
        silent_mode = True

    ### Execution
    auth = OAuthHandler(c['twitter_consumer_key'], c['twitter_consumer_secret'])
    auth.set_access_token(c['twitter_access_token'], c['twitter_access_secret'])
    api = tweepy.API(auth)

    client= ServiceBusService(
            c['eventhub_namespace'], 
            shared_access_key_name=c['eventhub_sas_key'],
            shared_access_key_value=c['eventhub_sas_value'])
    twitter_stream = Stream(
            auth,
            EventHubListener(c['eventhub_entity'], client, silent_mode))
    twitter_stream.filter(track=tracks, async=True)

if __name__ == "__main__":
    main()
