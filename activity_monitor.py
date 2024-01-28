from datetime import datetime, timedelta

from base_api import BaseAPI


class ActivityMonitor(BaseAPI):
    TOKEN_FILE_NAME = 'old/activity_token.json'
    SERVICE_NAME = 'driveactivity'
    API_VERSION = 'v2'
    TOKEN_SCOPES = ['https://www.googleapis.com/auth/drive.activity.readonly']

    TIME_FILTER = 'time >= \"{time_stamp}\"'
    SEARCH_TIME_DELTA_MINUTES = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.reset_last_query_time()

    def reset_last_query_time(self):
        # Set to 5 minutes back to avoid missing events
        self.last_query_time = datetime.utcnow() - timedelta(minutes=self.SEARCH_TIME_DELTA_MINUTES)

    def get_last_query_time_formatted(self):
        # Format the last query time, including "Z" to indicate UTC
        return self.last_query_time.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

    def get_new_files(self):
        # Add the last time checked to the query filter
        query_string = self.TIME_FILTER.format(time_stamp=self.get_last_query_time_formatted())

        # Query the api for created files
        query_results = self.api.activity().query(body={"filter": query_string}).execute()

        # Reset the query time to now
        self.reset_last_query_time()

        # Extract activities field from the request
        activities = query_results.get('activities', [])
        new_file_ids = []

        # Check if there are any new activities
        if activities:
            for activity in activities:
                # Extract target fields from the request
                targets = activity.get('targets', [])

                # Note: I tried filtering for created files only, but I was getting weird behaviour with actions
                # being "moved" instead of "create", so I removed the action type filter and return any file that
                # is included as a target
                for target in targets:
                    # Extract file id (ie 'items/17teqawaAogvoYHNLxNdV_8ihPSgWqPEn')
                    file_id = target['driveItem']['name'].split('/')[-1]
                    new_file_ids.append(file_id)

        return new_file_ids
