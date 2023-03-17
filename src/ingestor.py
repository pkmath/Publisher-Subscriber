import psycopg2, os, datetime

from models.subscriber import Subscriber
from psycopg2.extensions import AsIs
#
# Pipe Names (DONT REMOVE THIS)
#
CLAIM_PIPE_NAME = os.getenv("CLAIM_PIPE_NAME")
DIAGNOSE_PIPE_NAME = os.getenv("DIAGNOSE_PIPE_NAME")

#
# Database configs (DONT REMOVE THIS)
#
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")
DB_USER=os.getenv("DB_USER")
DB_PASS=os.getenv("DB_PASS")

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host= DB_HOST, port=DB_PORT)
cursor = conn.cursor()

##################################
######## ingest_func #############
def dummy_ingest_func(
    event, #dict: claim or diagnose msg 
    category, #str: diagnose or claim
):
    global DB_HOST
    global DB_PORT
    global DB_NAME
    global DB_USER
    global DB_PASS
    
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host= DB_HOST, port=DB_PORT)
    cursor = conn.cursor()

    event['tsp']=datetime.datetime.now()
    columns = event.keys()
    values = [event[column] for column in columns]
    if category=='claim':
        insert_statement = 'insert into claim (%s) values %s ON CONFLICT DO NOTHING;' #as id is PK in db, on conflict avoids UniqueViolation errors
    elif category=='diagnose':
        insert_statement = 'insert into diagnose (%s) values %s ON CONFLICT DO NOTHING;'
    cursor.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
    conn.commit()

##################################


def main():
    # ~~~~ DONT REMOVE THIS ~~~~
    # Set up signal handlers for graceful shutdown
    Subscriber.setup_signal_handlers()
    # Create subscribers
    claim_sub = Subscriber(CLAIM_PIPE_NAME)
    diagnose_sub = Subscriber(DIAGNOSE_PIPE_NAME)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~


    
    claim_sub.run_detached(dummy_ingest_func, ["claim"])
    diagnose_sub.run_detached(dummy_ingest_func, ["diagnose"])

    # ~~~~ DONT REMOVE THIS ~~~~
    # wait until signals (SIGTERM or SIGINT)
    claim_sub.block_until_exit()
    diagnose_sub.block_until_exit()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":
    main()
