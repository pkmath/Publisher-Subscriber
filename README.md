<br />
<p align="center">
  <h3 align="center">Subscriber - Publisher Setup</h3>
</p>

# Table of Contents

* [Project Structure](#project-structure)
* [Setup](#setup)
* [src](#src)
* [Clone the Application](#clone-the-application)
* [Contributing](#contributing)





# Project Structure


    ├── Publisher-Subscriber                    
    │   ├── setup             # init sql 
    │   └── src               # python scripts 
    │        ├── models       #Library code
    │        └── utils        #Library code

    


## Setup

This folder contains the sql file which creates the needed tables (postgres). Those tables are pre-define in sql and created when running the [init_db.sql](setup/init_db.sql) script.

The `Patient` table is filled automatically with 1000 random people (fake data). 
The last two tables are empty, and wil be filled with data read from the *publishers*.


## src

This folder contains all the python scripts.

*  [publisher.py](src/publisher.py)

This script produce fake data, `claims` and `diagnoses` every 2 seconds in JSON format, like the following:
```
Claim: {'id': 0, 'patient_id': 67, 'code': '03230', 'price': 3}
Diagnose: {'id': 0, 'patient_id': 744, 'icd10_code': 'R41.3'}
```

*  [ingestor.py](src/ingestor.py)

My library code handles subscribing to `claim` an `diagnose` publishers and can call a function every time there are new data. 
`ingestor.py` ingest those data in postgres whenever they arrive. 
Moreover, function takes care to not push, through the pipeline, duplicated data that may arrived. `Claim` and `diagnose` data are perceived as duplicate when their `id`(which is also a primary key in their respective sql tables) has been used before in the past. 

*  [pipeline_utils.py](src/utils/pipeline_utils.py)

Functions to create random fake data and generic read & write funcs

*  [subscriber.py](src/models/subscriber.py)

Functions to assign subscribers to data created from publishers.

*  [scheduler.py](src/models/scheduler.py)

`scheduler` library to schedule  queries to run every x minutes

## Clone the Application

``
git clone github.com/pkmath/Publisher-Subscriber.git
``


## Contributing

1. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
