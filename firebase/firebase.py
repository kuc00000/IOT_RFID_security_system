import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate('./auth.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def find_doc(coll_name, doc_name):
    doc_ref = db.collection(coll_name).document(doc_name)
    doc = doc_ref.get()
    if doc.exists:
        return True
    else:
        return False


def update_doc(coll_name, doc_name, field_name, value):
    doc_ref = db.collection(coll_name).document(doc_name)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update({field_name: value})
    else:
        print("Error")


def delete_doc(coll_name, doc_name):
    doc_ref = db.collection(coll_name).document(doc_name)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.delete()
    else:
        print("Error")


def register_material(material_id, _user_id, _due_date, _security_level):
    doc_ref = db.collection("Material").document(material_id)
    doc_ref.set({'user_id': _user_id, 'due_date': _due_date, 'security_level': _security_level})


def register_user(_user_id, _user_name, _password, _entry_time, _exit_time):
    doc_ref = db.collection("User").document(_user_id)
    doc_ref.set({'user_name': _user_name, 'password': _password, 'entry_time': _entry_time, 'exit_time': _exit_time})


def get_due_date(material_id):
    doc_ref = db.collection("Material").document(material_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc_ref.get({"due_date"})
    else:
        return False

