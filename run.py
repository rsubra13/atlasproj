from app import app_init

# To run from Gunicorn
#capp, manager = app_init()
capp,db = app_init()

# To run from python interpreter
if __name__ == "__main__":
    capp.run()
    #manager.run()

