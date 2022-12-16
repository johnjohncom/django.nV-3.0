django.nV 3.0
=========

django.nV is a purposefully vulnerable Django application provided by [nVisium](https://www.nvisium.com/). django.nV 3.0 supports django version 3, and some features have been patched to support Python 3.10+.

### System Requirements & Setup 

TODO

### Installation of Dependencies

To install the dependencies, simply run `pip install -r requirements.txt`.

### Database Setup

django.nV provides you with a script automatically creates the database as well as populates it with data. This script is titled `reset_db.sh`. django.nV does not ship with the database, so in order to run the application properly, you'll need to use this script:

    ./reset_db.sh

You can also use the same script to reset the database if you make any changes.

### Running the application
To run the app in its application folder type:

    ./runapp.sh

You should then be able to access the web interface at `http://localhost:8000/`.
