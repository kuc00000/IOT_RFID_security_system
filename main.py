from firebase import firebase as f
from hash import hash as h
import sys
import msvcrt
import datetime
from time import sleep


def get_secret(message=None) -> str:
    if message is not None:
        sys.stdout.write(message)
        sys.stdout.flush()
    buf = bytearray()
    skip = False
    while True:
        if not msvcrt.kbhit():
            continue
        x = msvcrt.getch()
        if x.startswith(b"\xe0") or x.startswith(b"\x00"):
            skip = True
            continue
        if skip:
            skip = False
            continue
        t = int.from_bytes(x, sys.byteorder)
        if t == 13:
            msvcrt.putch('\n'.encode())
            return buf.decode()
        elif t == 8:
            if buf:
                sys.stdout.write("\b \b")
                sys.stdout.flush()
                buf.pop()
        elif 32 <= t < 126:
            msvcrt.putch('*'.encode())
            buf.append(t)


while True:
    print("1 : Material management")
    print("2 : User management")
    print("0 : Exit")
    n = input("Input = ")
    if n == "0":
        break
    elif n == "1":
        while True:
            print("1 : Check the security level")
            print("2 : Registration")
            print("3 : Access control mode")
            print("4 : Return")
            print("0 : Exit")
            n = input("Input = ")
            if n == "0":
                break
            elif n == "1":
                _uid = get_secret()
                print("Security level = " + str((int(_uid) % 4 + 1)))
            elif n == "2":
                _uid = get_secret()
                _id = input("Id = ")
                salt = "test"
                if f.find_doc("Material", _id):
                    print("Error - id already exists in DB.")
                    continue
                if f.find_doc_with_uid("Material", _uid):
                    print("Error - uid already exists in DB.")
                    continue
                _name = input("Name = ")
                f.register_material(_id, _uid, _name,  (datetime.datetime.now() + datetime.timedelta(7, 0, 0, 0)).replace(tzinfo=None), int(_uid) % 4 + 1, salt)
                print("Success to register.")
            elif n == "3":
                _uid = get_secret()
                _id = f.find_doc_with_uid("Material", _uid)
                if _id:
                    print("Pass")
                else:
                    print("Warning - uid doesn't exist in DB.")
                    continue
                _due = f.get_field("Material", _id, "due_date")
                _due = _due.replace(tzinfo=None)
                if datetime.datetime.now() >= _due:
                    print("Warning - due date was over, please return it.")
            elif n == "4":
                _uid = get_secret()
                _id = f.find_doc_with_uid("Material", _uid)
                if _id:
                    _due = f.get_field("Material", _id, "due_date")
                    f.delete_doc("Material", _id)
                    print("Success to return.")
                    print("Due date : " + str(_due))
                    print("Export time : " + str(datetime.datetime.now().replace(tzinfo=None)))
                else:
                    print("Error - uid doesn't exist in DB.")
            else:
                print("Unexpected input - " + n + ". Try again.")
    elif n == "2":
        while True:
            print("1 : Card registration")
            print("2 : Access control mode")
            print("3 : Report lost and stolen")
            print("4 : Card release")
            print("5 : Check the entry and exit time")
            print("0 : Exit")
            n = input("Input = ")
            if n == "0":
                break
            elif n == "1":
                _uid = get_secret()
                _id = input("Id = ")
                salt = "test"
                if f.find_doc("User", _id):
                    print("Error - id already exists in DB.")
                    continue
                if f.find_doc_with_uid("User", _uid):
                    print("Error - uid already exists in DB.")
                    continue
                _name = input("Name = ")
                _password = get_secret("Password = ")
                f.register_user(_id, _uid, _name, _password, None, None, salt)
                print("Success to register.")
            elif n == "2":
                _uid = get_secret()
                _id = f.find_doc_with_uid("User", _uid)
                if _id:
                    print("Pass")
                else:
                    print("Warning - uid doesn't exist in DB.")
                    continue
                if f.get_field("User", _id, "entry_time") is None:
                    f.set_field("User", _id, "entry_time", datetime.datetime.now())
                    print("Check-in")
                elif f.get_field("User", _id, "exit_time") is None:
                    f.set_field("User", _id, "exit_time", datetime.datetime.now())
                    print("Check-out")
                else:
                    f.set_field("User", _id, "entry_time", datetime.datetime.now())
                    f.set_field("User", _id, "exit_time", None)
                    print("Check-in")
            elif n == "3":
                _name = input("Name = ")
                _password = get_secret("Password = ")
                doc = f.find_doc_with_np(_name, _password)
                if not doc:
                    print("Error - corresponding information doesn't exist.")
                else:
                    f.delete_doc("User", doc)
                    print("Success to delete information.")
            elif n == "4":
                _uid = get_secret()
                _id = f.find_doc_with_uid("User", _uid)
                if f.find_doc("User", _id):
                    f.delete_doc("User", _id)
                    print("Success to release the card.")
                else:
                    print("Error - uid doesn't exist in DB.")
            elif n == "5":
                _id = input("Id = ")
                if f.find_doc("User", _id):
                    print("Entry_time : " + str(f.get_field("User", _id, "entry_time")))
                    print("Exit_time : " + str(f.get_field("User", _id, "exit_time")))
                else:
                    print("Error - id doesn't exist in DB.")
            else:
                print("Unexpected input " + n + ". Try again.")
    else:
        print("Unexpected input " + n + ". Try again.")