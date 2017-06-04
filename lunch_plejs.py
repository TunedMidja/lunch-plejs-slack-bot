#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Slack bot that recommends a lunch place in central Stockholm """

import os
import time
import urllib2
import random
from bs4 import BeautifulSoup
from slackclient import SlackClient

BOT_ID = os.environ.get("BOT_ID")
TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_CLIENT = SlackClient(TOKEN)
LUNCH_PLACE_LIST_URL = 'http://www.kvartersmenyn.se/find/_/city/stockholm_1/area/city_4'

def pick_random_lunch_place_url():
    """
    Gets lunch restaurants in Stockholm (city) from Kvartersmenyn,
    picks one randomly and returns its URL.
    """

    lunch_place_list_html = urllib2.urlopen(LUNCH_PLACE_LIST_URL).read()
    soup = BeautifulSoup(lunch_place_list_html, 'html.parser')
    lunch_place_urls = []
    lunch_place_list = soup.select(".row.t_lunch")
    print "%s lunch places found!" % len(lunch_place_list)

    for lunch_place in lunch_place_list:
        lunch_place_urls.append(lunch_place.a['href'])

    return random.choice(lunch_place_urls)

def get_lunch_place_details(lunch_place_url):
    """
    Parses a Kvartersmenyn URL for a restaurant and returns details about it.
    """

    lunch_place_html = urllib2.urlopen(lunch_place_url).read()
    soup = BeautifulSoup(lunch_place_html, 'html.parser')
    name = soup.findAll("div", {"class": "name"})[0].h5.string
    aside = soup.findAll("aside")[0]
    homepage_url_html = BeautifulSoup(str(aside), 'html.parser').findAll("div")[-1]

    # Use restaurant homepage URL if exists, otherwise the one from Kvartersmenyn.
    homepage_url = homepage_url_html.p.a['href'] if homepage_url_html.p and homepage_url_html.p.a else None

    return name, lunch_place_url, homepage_url

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if SLACK_CLIENT.rtm_connect():
        print "LunchPlejs bot connected!"

        while True:
            for slack_message in SLACK_CLIENT.rtm_read():
                message = unicode(slack_message.get("text")).strip(' \t\n\r')
                user = slack_message.get("user")
                channel = slack_message.get("channel")

                message_string = message.encode('utf-8')

                # Only respond when mentioned
                if message_string.startswith("<@%s>" % BOT_ID):

                    command = message_string.replace("<@%s> " % BOT_ID, "")

                    text_to_post = None

                    if command == "tipsa":
                        PICKED_LUNCH_PLACE_URL = pick_random_lunch_place_url()
                        PICKED_LUNCH_PLACE_DETIALS = get_lunch_place_details(PICKED_LUNCH_PLACE_URL)
                        print PICKED_LUNCH_PLACE_DETIALS
                        TEXT_TODAYS_PLACE = 'Dagens lunchplejs: *%s*\n' % PICKED_LUNCH_PLACE_DETIALS[0]
                        TEXT_HOMEPAGE = 'Hemsida: %s\n' % PICKED_LUNCH_PLACE_DETIALS[2] if PICKED_LUNCH_PLACE_DETIALS[2] else ''
                        TEXT_MENU = 'Meny: %s' % PICKED_LUNCH_PLACE_DETIALS[1]
                        text_to_post = '%s%s%s' % (TEXT_TODAYS_PLACE, TEXT_HOMEPAGE, TEXT_MENU)
                    elif command == "hjälp":
                        text_to_post = "Jag kan för närvarande bara en sak (förutom att skriva ut den här texten) och det är att rekommendera ett lunchplejs. Detta gör jag när någon skriver \"@lunchplejs tipsa\"."
                    else:
                        continue

                    SLACK_CLIENT.api_call(
                        "chat.postMessage",
                        as_user="true",
                        channel=channel,
                        link_names="true",
                        text=text_to_post)

            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print "Connection error! Invalid Slack token (%s) or bot ID (%s)?" % TOKEN, BOT_ID
