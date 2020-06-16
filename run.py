import os
from anonymous import create_app

app = create_app(os.environ['APP_SETTINGS'])

if __name__=='__main__':
	app.run()
