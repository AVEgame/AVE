from ave import AVE, errors
import os

if os.getenv("DEBUG"):
    try:
        ave = AVE()
        ave.start()
    except errors.AVEQuit:
        ave.exit()
        print("Goodbye...")
    finally:
        ave.exit()
else:
    while True:
        try:
            ave = AVE()
            ave.start()
        except errors.AVEQuit:
            ave.exit()
            print("Goodbye...")
            break
        except:
            ave.exit()
            break
