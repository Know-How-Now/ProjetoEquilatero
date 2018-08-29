import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import exceptions as exception
from google.cloud import firestore as cloudfirestore
import custom_classes as c_class
import datetime
from faker import Faker

cred = credentials.Certificate('<path-to-file>/serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
fake = Faker()

#---------------------[ CHECK IF DATA EXISTS ]---------------------#
def check_data_existance(collection, document):
    doc_ref = db.collection(collection).document(document)
    try:
        doc = doc_ref.get()
        #return doc.to_dict()
        return True
    except exception.NotFound:
        return False
#---------------------------------------------------------------------#

# [ START OF - GET ALL DATA IN COLLECTION ] #
def get_collection_docs(collection):
    docs = db.collection(collection).get()
    docs_id = []
    for doc in docs:
        docs_id.append(doc.id)
    return docs_id
    #[END of function]

def get_track_length(collection,document):
    # [REFERENCE collection (AND/OR document)]
    doc_ref = db.collection(collection).document(document)
    doc = doc_ref.get()
    if collection == 'Tracks':
        track = c_class.Track.from_dict(doc.to_dict())
        return track.length
    # [END: SPONSOR DESCRIPTION] #

# [ START OF - GET MULTIPLE TIMESTAMPPED DATA ] #
def get_multiple_document_data_test(collection,document):
    doc_ref = db.collection(collection).document(document)
    docs = doc_ref.get()
    timestamp = c_class.Timestamp(docs.to_dict())
    for key, value in timestamp:
        investment = c_class.Investment(**value)
        print('Key = ', key)
        print('Value = ', value)
        print('Investment (class) data = ', investment)
        print('Investment.ammount = ', investment.ammount)
        print('Investment.hashtags =', investment.allocated_to)
        print('Investment.hashtags[i] =', investment.allocated_to[1])
        if 'fast' in investment.allocated_to:
            print("'term' is in 'hashtags'!")
        if not 'whom' in investment.allocated_to:
            print("'term' is NOT in 'hashtags'!")
        print("#---------------------------------------#")

#get_multiple_document_data_test('Investments','1364824386')
# [ END OF - GET MULTIPLE TIMESTAMPPED DATA ] #
