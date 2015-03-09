__author__ = 'Ramki Subramanian'
DEBUG = False  # Flag to set debug level. (print statements on/off)

import re
import json
from bs4 import BeautifulSoup
from lxml import html
from urllib2 import (URLError, HTTPError)
import requests
from requests.exceptions import SSLError
import time
from multiprocessing.pool import ThreadPool as Pool


class MessageDecode(object):

    def __int__(self):
        pass

    def removeduplicates(self, inputlist):
        return list(set(inputlist))

    def decode(self, inputstring,messagetime):
        """

        :param inputstring: the input string which needs to be parsed and split
        :return: json
        """

        # Dictionary of list of 'mentions', 'emoticons' and 'links'
        final_dict = {}

        # 1. Find the "mentions" from the input string
        # Previous method - catches @ only in the start of the word and
        # only single word values.
        # e = re.findall(r"(\B(?:\@)[\w\S]*.*?)", inputString)
        # \B to catch the @ in the start of the word
        # \S- to handle only single word values
        try:
            # Advanced method: Match multi-words which starts with '@'
            # at any part of the sentence
            mentions = re.findall(r"((?:@)[\w.]+)", inputstring)

            # add to the final dict only if its not null
            if mentions:
                mentions_list = [i.strip('@') for i in mentions]
                mentions_list = self.removeduplicates(mentions_list)
                final_dict['mentions'] = mentions_list
        except AssertionError:
            pass

        # 2. Catch the emoticons from the input string
        try:
            # \s for whitespace (handling multiword names like Michael Jackson)
            # \w for alphanumeric (handling user names like mike999)
            emoticons = re.findall(r"(\([\w\s]{1,15}\).*?)", inputstring)
            if emoticons:
                emoticons_list = [em.strip('()') for em in emoticons]
                emoticons_list = self.removeduplicates(emoticons_list)
                final_dict['emoticons'] = emoticons_list
            if DEBUG:
                print("Emoticons:",  emoticons)
        except AssertionError:
            pass

        # 3. Picking URL from the chat string
        try:
            # url_list = re.findall(r"(http[^\s]+).*?",inputString,re.DOTALL)
            # ?:  - non groups, www1-9 handles websites with www9 prefix.
            url_list = re.findall('(?xi) (?:http[s]?:// | www\d{0,3}[.] | ftp?:// ) '
                                  '(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', inputstring)
            url_dict = {}
            url_list_of_dicts = []
            # pool = Pool(8)
            if DEBUG:
                print(url_list)
            try:
                for urlid, each_url in enumerate(url_list):
                    try:
                        # Get the HTML content of the given web URL
                        response = requests.get(each_url.decode('utf-8', 'ignore'))
                        # Use BeautifulSoup to parse and extract page title
                        # This gave HTTPError sometimes
                        soup = BeautifulSoup(response.text)
                        title = soup.title.string
                        encoded_title = title.encode('ascii','ignore')
                    except:
                        print "error"
                        encoded_title = None
                    # Use lxml to avoid those errors and its faster than BS.
                    # parsed_tree = html.fromstring(response.text)
                    # title = parsed_tree.xpath('//title/text()')

                    # Create the dict
                    url_dict['id'] = urlid
                    url_dict['url'] = each_url
                    url_dict['title'] = encoded_title

                    # Add this list of dicts to the final_dict
                    url_list_of_dicts.append(url_dict.copy())
                    # .copy() is important else same dict will be copied.
                    final_dict['links'] = url_list_of_dicts
                    final_dict['message_time'] = messagetime

            except (HTTPError, URLError, ValueError, SSLError) as e:
                print("The server couldn't be reached")
                print('Error code:'), e

        except AssertionError:
            pass
        formatted_json = json.dumps(final_dict, sort_keys=True, indent=4).decode('utf8')

        return formatted_json


if __name__ == '__main__':
    newObj = MessageDecode()
    inputString = raw_input("Please enter a chat string (Till you press enter)\n")
    # inputString = (" @Ramki (Smiley) u?? Weather is (awesome)\n http://www.crummy.com/software/BeautifulSoup/bs4/doc/"
    #                 "Did yo u check Adam's blog http://www.imdb.com/title/tt0583452/?ref_=tt_eps_rhs_1 (angry) @Ramki @jacob18"
    #                 "(Angry ) (Smilaey) ftp://ftp6.jp.freebsd.org/pub/FreeBSD/ (Smiley)")
    messageTime = time.ctime()
    finaljson = newObj.decode(inputString,messageTime)
    print "###########  Formatted JSON ############ \n", finaljson