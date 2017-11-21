from pytrends.pyGTrends import pyGTrends
import time
from random import randint
# import pymysql
import pymysql.cursors
import logging

google_username = "************"
google_password = "********"

logging.basicConfig(filename='Trends.log', level=logging.DEBUG)
log = logging.getLogger(__name__)


# connect to Google
# connector = pyGTrends(google_username, google_password)

server = 'localhost'
database = 'GoogleTrends'
user = 'root'
password = '123456'
log.info('Connecting to data base....!')
connection = pymysql.connect(host=server,
                             user=user,
                             password=password,
                             db=database)
log.info('We are connected to Database')
keywords = 'Policybazaar'

log.info('Connecting to Google Trends....!')
connector = pyGTrends(google_username, google_password)
log.info('Connected to Google Trends.')


while True:
    # connect to Google
    # connector = pyGTrends(google_username, google_password)
    # make request
    log.info('we are inside while loop')
    try:

        connector.request_report(keywords, hl='en-US', cat=None, geo='IN', date='now 1-H', tz="Etc/GMT-5:30")
        log.info('Requested query got...')
        xx = connector.get_data()
        yy = str(xx)
        ll = yy.split('\n')
        log.info(ll)
        if len(ll) < 10:
            continue
        else:
            new_ll = []
            i = 5
            index_error = []
            while ',' in ll[i]:
                new_ll.append(ll[i])
                i += 1
                index_error.append(i)
            log.info(index_error)
            log.info(new_ll)
            for x in new_ll:
                dd = x.split(',')
                try:
                    with connection.cursor() as cursor:
                        # Create a new record
                        log.info('inserting data in database')
                        sql = "INSERT INTO Trends (time_stamp, searches) VALUES (%s, %s)"
                        # print(sql, (dd[0], dd[1]))
                        # sql = "INSERT INTO Trends (`email`, `password`) VALUES (%s, %s)"
                        cursor.execute(sql, (dd[0], dd[1]))

                        # connection is not autocommit by default. So you must commit to save
                        # your changes.
                        connection.commit()
                        log.info('Data got inserted in database')

                except:
                    log.info('Data is not being inserted...Please check.')
                    pass
                # connection.close()
            time.sleep(randint(3000,3500))
        time.sleep(randint(50,55))
    except:
        pass

