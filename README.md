# ForTest
Environment setup (Windows Version):

1. Install Python 3.8.5
	> Download link:  https://www.python.org/downloads/release/python-385/
2. Install virtualenv
	> python -m pip install --user virtualenv
3. Create a virtual evironment
	> python -m venv env
4. Activate virtual environment
	> cd env
	> cd Scripts
	> activate
5. To exit the virtual environment use
	> Deactivate
6. Install all needed libraries.
	> pip install -r requirements.txt
7. Setup environment variables	
	> Set an OS environment variable named: DBHOST, DBPORT, DBUSERNAME, DBUSERPASS
	> With the connection string to the database, example: mssql+pyodbc://<username>:<password>@<Server>/<Database>?driver=ODBC+Driver+17+for+SQL+Server
	> To access PostgreSQL database (PostgreSQL database has to have PosGIS extension to work).
	> Run in PostgreSQL the ForTest.sql script.