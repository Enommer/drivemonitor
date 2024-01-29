import argparse
import time

from activity_monitor import ActivityMonitor
from drive_api import DriveAPI

MAIN_LOOP_SLEEP_TIME = 5

def get_args():
    parser = argparse.ArgumentParser(description='A script that monitors and protect public folders in google drive.')
    parser.add_argument('-p', '--use_proxy', action='store_true', help='Use a proxy (127.0.0.1:8080)', default=False)

    return parser.parse_args()

def get_public_permission_id(file_data):
    # Checks if file is public and returns the public permission id
    # (This will always be 'anyoneWithLink' but I'm returning the file_id in case this changes in the future)
    permissions = file_data['permissions']
    for permission in permissions:
        # Check if permission is public
        if permission['type'] == 'anyone':
            return permission['id']

    return None

def main():
    args = get_args()
    # Init the api objects
    activity_monitor = ActivityMonitor(use_proxy=args.use_proxy)
    drive_api = DriveAPI(use_proxy=args.use_proxy)

    while True:
        new_file_ids = activity_monitor.get_new_files()

        if new_file_ids:
            for new_file_id in new_file_ids:
                # Get more info about the file object
                new_file = drive_api.get_file_object(new_file_id)

                public_permission_id = get_public_permission_id(new_file)
                # File is public
                if public_permission_id:
                    print(f'[-] File {new_file_id} is public')

                    for parent in new_file['parents']:
                        # Is parent publicly accessible
                        # (Publicly accessible folders automatically set their children as public)
                        if get_public_permission_id(drive_api.get_file_object(parent)):
                            try:
                                drive_api.delete_file_permission(new_file_id, public_permission_id)
                                print('[-] File is now private!')
                            except Exception as e:
                                print('[!] Failed to delete permission, check logs!')
                else:
                    print(f'[-] File {new_file_id} is private')
        else:
            print('[+] No new files')

        time.sleep(MAIN_LOOP_SLEEP_TIME)


if __name__ == '__main__':
    main()
