import sys
import msvcrt


def get_secret() -> str:
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
            print("4 : Deletion")
            print("0 : Exit")
            n = input("Input = ")
            if n == "0":
                break
            elif n == "1":
                uid = get_secret()
                print("Security level = " + str((int(uid) % 4 + 1)))
            elif n == "2":
                uid = get_secret()
                # check if uid is already saved in DB
                # if not, register uid with hashing
            elif n == "3":
                uid = get_secret()
                # check if uid is already saved in DB
                # if not, print warning message
                # check due_date and print message
            elif n == "4":
                uid = get_secret()
                # check if uid is already saved in DB
                # if not, print error message
                # delete uid from DB, and print due_date, export_time
            else:
                print("Unexpected input " + n + ". Try again.")
    elif n == "2":
        while True:
            print("1 : Card registration")
            print("2 : Access control mode")
            print("3 : Report lost and stolen")
            print("4 : Deletion")
            print("5 : Check the entry and exit time")
            print("0 : Exit")
            n = input("Input = ")
            if n == "0":
                break
            elif n == "1":
                uid = get_secret()
                # check if uid is already saved in DB
                # if not, register uid with hashing
            elif n == "2":
                uid = get_secret()
                # check if uid is already saved in DB
                # if not, print warning message
                # record entry & exit time
            elif n == "3":
                name = input("Name = ")
                print("Password = ", end='')
                password = get_secret()
                # check if uid with same information is exist in DB
                # if not, print error message
                # delete uid from DB
            elif n == "4":
                uid = get_secret()
                # check if uid is already saved in DB
                # if not, print error message
                # delete uid from DB
            elif n == "5":
                name = input("Name = ")
                # print entry & exit time
            else:
                print("Unexpected input " + n + ". Try again.")
    else:
        print("Unexpected input " + n + ". Try again.")
