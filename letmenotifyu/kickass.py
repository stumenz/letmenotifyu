#!/usr/bin/python3

import logging
import re


def search_episode(kickass_file, title, episode_name, uploader):
    "search for episode"
    with open(kickass_file, 'r') as f:
        for line in f:
            if re.search(r'%s' %(title+".*"+episode_name+' (?!720p).*'+uploader), line):
                logging.debug("found {}".format(line))
                episode_info = line.split("|")
                episode_title = episode_info[1]
                episode_torrent_link = episode_info[4]
                episode_torrent_hash = episode_info[0]
                return episode_title, episode_torrent_link, episode_torrent_hash
