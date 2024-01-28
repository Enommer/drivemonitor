import argparse
import time

from activity_monitor import ActivityMonitor
from drive_api import DriveAPI

MAIN_LOOP_SLEEP_TIME = 10


def get_args():
    parser = argparse.ArgumentParser(description='A script that monitors and protect public folders in google drive.')
    parser.add_argument('-p', '--use_proxy', action='store_true', help='Use a proxy (127.0.0.1:8080)', default=False)

    return parser.parse_args()


def main():
    args = get_args()
    # Init the api objects
    activity_monitor = ActivityMonitor(use_proxy=args.use_proxy)
    drive_api = DriveAPI(use_proxy=args.use_proxy)

    while True:
        new_file_ids = activity_monitor.get_new_files()

        if new_file_ids:
            for new_file_id in new_file_ids:
                print(f'[-] File {new_file_id}')

                # Get more info about the file object
                new_file = drive_api.get_file_object(new_file_id)

                # Check if the file is a folder
                if new_file['mimeType'] == 'application/vnd.google-apps.folder':
                    # Check if is a public folder
                    permissions = new_file['permissions']
                    for permission in permissions:
                        # Check if permission is public
                        if permission['type'] == 'anyone':
                            print('[-] File is a public folder - making private!')

                            # Delete the public permission
                            try:
                                drive_api.delete_file_permission(new_file_id, permission['id'])
                                print('[-] Folder is now private')
                            except Exception as e:
                                print('[!] Failed to delete permission, check logs!')
        else:
            print('[+] No new files')

        time.sleep(MAIN_LOOP_SLEEP_TIME)


if __name__ == '__main__':
    main()
