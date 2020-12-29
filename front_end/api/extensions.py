import mysql.connector
import os

#database connection
db = mysql.connector.connect(
    host='localhost',
    user=os.getenv('DATABASE_WEBSITE_USER'),
    password=os.getenv('DATABASE_WEBSITE_PASSWORD')
)

db_cursor = db.cursor()
db_cursor.execute('USE myspotifyinsight')
db.commit()

