import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate('./auth.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def register_material(material_id, uid, name, due_date, security_level, salt):
    doc_ref = db.collection("Material").document(material_id)
    doc_ref.set({'uid': uid, 'name': name, 'due_date': due_date, 'security_level': security_level, 'salt': salt})


def register_user(id, uid, name, password, entry_time, exit_time, salt):
    doc_ref = db.collection("User").document(id)
    doc_ref.set({'uid': uid, 'name': name, 'password': password, 'entry_time': entry_time, 'exit_time': exit_time, 'salt': salt})


def find_doc(coll_name, doc_name):
    doc_ref = db.collection(coll_name).document(doc_name)
    doc = doc_ref.get()
    if doc.exists:
        return True
    else:
        return False


def delete_doc(coll_name, doc_name):
    doc_ref = db.collection(coll_name).document(doc_name)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.delete()
    else:
        print("Error")


def get_field(coll_name, doc_name, field_name):
    doc_ref = db.collection(coll_name).document(doc_name)
    doc = doc_ref.get()
    if doc.exists:
        return doc.get(field_name)
    else:
        return False


def set_field(coll_name, doc_name, field_name, value):
    doc_ref = db.collection(coll_name).document(doc_name)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update({field_name: value})
    else:
        print("Error")


def find_doc_with_np(name, password):
    docs = db.collection("User").stream()
    for doc in docs:
        if doc.exists:
            if doc.get("name") == name and doc.get("password") == password:
                return doc.id
    return False


def find_doc_with_uid(coll_name, uid):
    docs = db.collection(coll_name).stream()
    for doc in docs:
        if doc.exists:
            if doc.get("uid") == uid:
                return doc.id
    return False

