from base_api import BaseAPI


class DriveAPI(BaseAPI):
    TOKEN_FILE_NAME = 'old/drive_token.json'
    SERVICE_NAME = 'drive'
    API_VERSION = 'v3'
    TOKEN_SCOPES = ['https://www.googleapis.com/auth/drive']

    def get_file_object(self, file_id):
        return self.api.files().get(fileId=file_id, fields='id, name, owners, permissions, mimeType').execute()

    def delete_file_permission(self, file_id, perm_id):
        self.api.permissions().delete(fileId=file_id, permissionId=perm_id).execute()