from app import app, create_database

create_database()

if __name__ == '__main__':

    app.run()
