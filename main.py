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
                uid = get_secret()
                print("Security level = " + str((int(uid) % 4 + 1)))
            elif n == "2":
                uid = get_secret()
                if f.find_doc("Material", uid):
                    print("Error - uid already exists in DB.")
                    continue
                t = input("User_id = ")
                f.register_material(uid, t,  (datetime.datetime.now() + datetime.timedelta(7, 0, 0, 0)).replace(tzinfo=None), int(uid) % 4 + 1)
                print("Success to register.")
            elif n == "3":
                uid = get_secret()
                if f.find_doc("Material", uid):
                    print("Pass")
                else:
                    print("Warning - uid doesn't exist in DB.")
                    continue
                due = f.get_field("Material", uid, "due_date")
                due = due.replace(tzinfo=None)
                if datetime.datetime.now() >= due:
                    print("Warning - due date was over, please return it.")
            elif n == "4":
                uid = get_secret()
                if f.find_doc("Material", uid):
                    due = f.get_field("Material", uid, "due_date")
                    f.delete_doc("Material", uid)
                    print("Success to return.")
                    print("Due date : " + str(due))
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
                uid = get_secret()
                if f.find_doc("User", uid):
                    print("Error - uid already exists in DB.")
                    continue
                else:
                    name = input("Name = ")
                    password = get_secret("Password = ")
                    f.register_user(uid, name, password, None, None)
                    print("Success to register.")
            elif n == "2":
                uid = get_secret()
                if f.find_doc("User", uid):
                    print("Pass")
                else:
                    print("Warning - uid doesn't exist in DB.")
                    continue
                if f.get_field("User", uid, "entry_time") is None:
                    f.set_field("User", uid, "entry_time", datetime.datetime.now())
                    print("Check-in")
                elif f.get_field("User", uid, "exit_time") is None:
                    f.set_field("User", uid, "exit_time", datetime.datetime.now())
                    print("Check-out")
                else:
                    f.set_field("User", uid, "entry_time", datetime.datetime.now())
                    f.set_field("User", uid, "exit_time", None)
                    print("Check-in")
            elif n == "3":
                name = input("Name = ")
                password = get_secret("Password = ")
                doc = f.find_doc_with_np(name, password)
                if not doc:
                    print("Error - corresponding information doesn't exist.")
                else:
                    doc.delete()
                print("Success to delete information.")
            elif n == "4":
                uid = get_secret()
                if f.find_doc("User", uid):
                    f.delete_doc("User", uid)
                    print("Success to release the card.")
                else:
                    print("Error - uid doesn't exist in DB.")
            elif n == "5":
                uid = get_secret()
                if f.find_doc("User", uid):
                    print("Entry_time : " + str(f.get_field("User", uid, "entry_time")))
                    print("Exit_time : " + str(f.get_field("User", uid, "exit_time")))
                else:
                    print("Error - uid doesn't exist in DB.")
            else:
                print("Unexpected input " + n + ". Try again.")
    else:
        print("Unexpected input " + n + ". Try again.")