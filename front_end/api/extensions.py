from flask_login import LoginManager, UserMixin
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

login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id, user_name):
    regular_user = RegularUser.get_user(user_id=user_id, user_name=user_name)
    pass

login_manager.login_view = 'auth.access_denied'


#FIXME: don't know
class RegularUser():

    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymouse(self):
        return False

    @property
    def get_id(self):
        return self.user_id

    def get_user(self, user_id, user_name):
        sql_command_search = """
            select regular_user_id, user_name
                from regularusers
                where regular_user_id = %d; 
        """%(user_id)

        db_cursor.execute(sql_command_search)
        search_result = db_cursor.fetchall()

        if len(search_result) == 0:
            return None

        return RegularUser(user_id, user_name)
