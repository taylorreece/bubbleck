# Setup your development environment
Windows development setup:
 1. Install Python 3.4.3 from https://www.python.org/downloads/release/python-343/
 2. Install Postgresql 9.4.4 from http://www.enterprisedb.com/products-services-training/pgdownload#windows
 3. Install whatever text editor you like (gVim, Notepad++, Sublime, etc).
 4. Install psycopg2 package from http://www.stickpeople.com/projects/python/win-psycopg/
 5. Check out the myAutoTA repository from https://github.com/taylorreece/bubbleck 
 6. Edit/add the following environment variables:
	* Append ";C:\Python34;C:\Python34\Scripts" to PATH
	* Create a new variable PYTHONPATH "C:\bubbleck\shared_python\;C:\bubbleck\shared_python\bck\;."
 7. Open up PostgreSQL's pgAdmin.  
	* Create a new database 'bck'
	* Create a new role 'bck' with some password ("1234", maybe?) for that database
	* Run the schema file that's checked out in C:\bubbleck\schema\s0.sql.
 8. Copy C:\bubbleck\ansible\templates\bckconfig.py.j2 to C:\bubbleck\shared_python\bck\bckconfig.py
	* Change the variables within that file.
 9. Start up a shell; run python3 against C:\bubbleck\web\bubbleck\runbubbleck.py.
	* There'll likely be some missing packages; we'll install those globally with pip.
