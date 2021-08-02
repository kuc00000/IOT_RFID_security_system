import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('./auth.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

##user라는 collection에 document를 추가하는 코드, 아래 부분은 필드명
def create_doc_user(coll_id,doc_id):
    doc_ref = db.collection(coll_id).document(doc_id)
    return doc_ref
##이 부분은 필드명 자유롭게 편집 가능
doc_ref.set({
        'entry_time': 'none',
        'exit_time': 'none',
        'password': 'ddkxz5792',
        'user_name': 'Scout'
})
##현재 시간을 가져오려면 datetime.datetime.now() 함수로 구현 가능

##material table에 document를 추가하는 코드
def create_doc_material(coll_id,doc_id):
    doc_ref = db.collection(coll_id).document(doc_id)
    doc_ref.set({
        'due_date': 'none',
        'export_time': 'none',
        'security_level': {'Radio comms':1}, #map type의 경우 다음과 같이 작성
        'user_id': ''
    })

##collection 전체를 삭제하는 코드
def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.to_dict()}')
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)
    ##사용 예시 : delete_collection(db.collection('users'),10)
    ##collection 자체의 크기가 클수록 batch_size를 크게 하면 전체 삭제 가능
