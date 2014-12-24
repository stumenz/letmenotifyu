from datetime import datetime
from notifylib.notify import announce
import logging
from notifylib import util
import sqlite3


class Series:
    def __init__(self, cursor, connect):
        self.cursor = cursor
        self.connect = connect

    def fetch_series_data(self):
        self.cursor.execute('SELECT id,series_link,number_of_episodes from series where status=1')
        return self.cursor.fetchall()

    def fetch_new_episdoes(self, series_link):
        return util.primewire(series_link)

    def insert_new_epsiodes(self, all_eps, new_ep_number, series_id, no_seasons):
        self.cursor.execute("SELECT title,watch from series where id=?", (series_id,))
        series_detail = self.cursor.fetchall()
        logging.info("adding new episodes for %s",series_detail[0])
        for new_data in all_eps:
            try:
                self.cursor.execute("INSERT INTO episodes(" +
                                    'series_id,' +
                                    'episode_link,' +
                                    'episode_name,' +
                                    'Date) ' +
                                    'VALUES(?,?,?,?)'
                                    ,(series_id, new_data[0], new_data[1], datetime.now(),))
                self.connect.commit()
                announce("New Series Episode", series_detail[0],
                         "www.primewire.ag" + new_data[0])
                
            except sqlite3.IntegrityError as e:
                logging.error("Series episode already exists")
        self.cursor.execute("UPDATE series set number_of_episodes=?,"+
                                'number_of_seasons=?,last_update=?  where id=?',
                                (new_ep_number, no_seasons, datetime.now(), series_id,))
        self.connect.commit()

    def new_series_episodes(self, all_episodes, new_ep_number, series_id, no_seasons):
        logging.info("New series to be added")
        try:
            for new_data in all_episodes:
                self.cursor.execute("INSERT INTO episodes("+
                                    'series_id,'+
                                    'episode_link,'+
                                    'episode_name) ' +
                                    'VALUES(?,?,?)',
                                    (series_id, new_data[0], new_data[1],))
            self.cursor.execute("UPDATE series set number_of_episodes=?,"+
                                'number_of_seasons=?,'+
                                'last_update=?,'+
                                'current_season=? '+
                                'where id=?',
                                 (new_ep_number, no_seasons, datetime.now(),
                                  no_seasons,  series_id,))
            util.series_poster(self.cursor, self.connect, series_id)
            self.connect.commit()
            logging.info("New series episodes added")
        except Exception as e:
            logging.error("unable to add series episodes")
            logging.exception(e)
            self.connect.rollback()











