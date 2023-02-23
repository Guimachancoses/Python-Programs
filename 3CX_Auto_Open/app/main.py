from modules.app_launcher import check_and_launch_app
import time

def main():
    while True:
        check_and_launch_app()
        time.sleep(15)

if __name__ == '__main__':
    main()