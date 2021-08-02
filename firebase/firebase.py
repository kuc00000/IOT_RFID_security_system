import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
#auth.json 파일이 현재 .py 파일의 위치에 존재해야 한다.

cred = credentials.Certificate('./auth.json')
#firebase_admin.initialize_app(cred) 이 코드는 처음 실행 시 한번만 호출하면 된다. 다시 호출하면 에러가 발생한다.


db = firestore.client() #database 참조 객체를 파이어스토어 클라이언트로부터 가져온다. 필수 부분

#user라는 collection에 document를 추가하는 코드, coll_id는 테이블명, doc_id는 primary key
#coll_name의 이름을 갖는 collection에 doc_name의 이름을 갖는 document 생성
def create_doc(coll_name,doc_name):
    doc_ref = db.collection(coll_name).document(doc_name) #doc_ref 객체는 document를 참조하는 객체
    return doc_ref #document 참조를 리턴

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

class Material(object):
    def __init__(self, user_id, due_date, export_date, security_level=0):
        self.user_id = user_id
        self.due_date = due_date
        self.export_date = export_date
        self.security_level = security_level

    #to_dict메서드는 현재 Material 오브젝트가 가진 정보를 dictionary의 형태로 리턴하는 메서드
    def to_dict(self):
        return {'user_id':self.user_id,'due_date':self.due_date,'export_date':self.export_date,'security_level':self.security_level}

    def __repr__(self):
        return(
            f'Material(\
                user_id={self.user_id}, \
                due_date={self.due_date}, \
                export_date={self.export_date}, \
                security_level={self.security_level}, \
            )'
        )

class User(object):
    def __init__(self, entry_time, exit_time, user_name, password='0000'):
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.user_name = user_name
        self.password = password

    #to_dict메서드는 현재 User 오브젝트가 가진 정보를 dictionary의 형태로 리턴하는 메서드
    def to_dict(self):
        return {'entry_time':self.entry_time,'exit_time':self.exit_time,'user_name':self.user_name,'password':self.password}

    def __repr__(self):
        return(
            f'Material(\
                user_id={self.user_id}, \
                due_date={self.due_date}, \
                export_date={self.export_date}, \
                security_level={self.security_level}, \
            )'
        )




'''
doc_ref = create_doc('Material','12345678')
today = datetime.datetime.now()
material = Material(user_id='12345', due_date=today, 
                export_date =today,security_level={'Voice comms':3})
doc_ref.set(material.to_dict())


위 코드는 Material collection에 12345678(장비의 ID값)을 이름으로 갖는
document를 생성하여 document의 필드 값들을 설정하는 코드이다.
datetime.datetime.now()는 현재 시간을 리턴한다.
만일 2018년 5월 13일의 날짜 데이터를 넣고 싶다면
date = datetime.datetime(2018,5,13,15,27,4,10000)
year:2018, month:5,day:13, hour:15, minute:27, second:4, microsecond:10000


doc_ref = create_doc('User','12345678')
today = datetime.datetime.now()
user = User(entry_time='12345', exit_time=today, 
                user_name ='Uichan Kim',password='12313131')
doc_ref.set(material.to_dict())

User 컬렉션에 12345678이라는 user_id를 갖는 user document를 추가하고 그 document의 필드 값들을
설정하는 코드

기존에 생성된 document의 내용을 바꾸는 것이 아닌 아예 새로운
document를 만들고 값을 설정하고 싶다면 다음과 같이 작성한다.

user = User(entry_time='12345', exit_time=today, 
                user_name ='Uichan Kim',password='12313131')
db.collection('User').add(user.to_dict())
'''

def get_doc(coll_name,doc_name):
    return db.collection(coll_name).document(doc_name)


def update_doc(coll_name,doc_name,field_name,value):
    doc_ref = db.collection(coll_name).document(doc_name)
    doc_ref.update({field_name:value})
''' 위 메서드는 coll_name의 collection(테이블)에 doc_name의 이름(primary key)
을 갖는 document에 field_name의 속성을 value라는 값으로 변경할 때 사용한다.
'''



'''
batch = db.batch()

# Set the data for NYC
nyc_ref = db.collection(u'cities').document(u'NYC')
batch.set(nyc_ref, {u'name': u'New York City'})

# Update the population for SF
sf_ref = db.collection(u'cities').document(u'SF')
batch.update(sf_ref, {u'population': 1000000})

# Delete DEN
den_ref = db.collection(u'cities').document(u'DEN')
batch.delete(den_ref)

# Commit the batch
batch.commit()

batch는 일괄 작업에 사용되는 객체이다.
batch는 commit 메서드를 호출하기 전까지 위와 같이 set,update,delete 메서드 등을 통해
동시에 여러개의 set,update,delete 작업을 수행할 수 있다. 이 작업은 최대 500개까지
지정 가능하다.
'''


def print_doc_data(coll_name,doc_name):
    doc_ref = db.collection(coll_name).document(doc_name)
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
    else:
        print(u'No such document!')

#coll_name에 해당하는 컬렉션의 모든 문서의 정보를 출력한다.
def print_all_doc(coll_name):
    docs = db.collection(coll_name).stream()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

#field_name에 해당하는 속성을 document에서 삭제        
def delete_field(coll_name,doc_name,field_name):
    doc_ref = db.collection(coll_name).document(doc_name)
    city_ref.update({
        field_name: firestore.DELETE_FIELD
    })


#문서를 삭제하는 함수
def delete_document(coll_name,doc_name):
    db.collection(coll_name).document(doc_name).delete()

