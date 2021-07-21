# -*- coding: utf-8 -*-

import os
import sys
import dropbox
import traceback
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

DROPBOX_ROOT_PATH = '/farmsplan'


class DropboxApi:
    def __init__(self, token):
        try:
            self.__dbx = dropbox.Dropbox(token)
        except:
            traceback.print_exc()

    def get_folder_entries(self, path=''):
        return self.__dbx.files_list_folder(path).entries

    def delete_file_from_dropbox(self, path):
        try:
            self.__dbx.users_get_current_account()
        except AuthError as err:
            traceback.print_exc(
                "ERROR: Invalid access token; try re-generating an "
                "access token from the app console on the web."
            )
            return

        return self.__dbx.files_delete_v2(path)

    def get_file_from_dropbox(self, path):
        path_prefix, filename = os.path.split(path)
        local_path = '/tmp/%s' % filename

        try:
            self.__dbx.users_get_current_account()
        except AuthError as err:
            traceback.print_exc(
                "ERROR: Invalid access token; try re-generating an "
                "access token from the app console on the web."
            )
            return

        self.__dbx.files_download_to_file(local_path, path)
        return local_path

    def dbx_file_exists(self, path):
        try:
            if not self.__dbx.files_get_metadata(path):
                return False
            return True
        except:
            traceback.print_exc('[file_exists]files_get_metadata error')
            return False

    def backup_file_to_dropbox(self, local_path, backup_path):
        with open(local_path, 'rb') as f:
            print("Uploading " + local_path + " to Dropbox as " + backup_path + "...")
            base, filename = os.path.split(backup_path)

            try:
                self.__dbx.files_get_metadata(base)
            except:
                self.__dbx.files_create_folder_v2(base)

            try:
                self.__dbx.files_upload(f.read(), backup_path, mode=WriteMode('overwrite'))
            except ApiError as err:
                if (err.error.is_path() and err.error.get_path().error.is_insufficient_space()):
                    traceback.print_exc("ERROR: Cannot back up; insufficient space.")
                elif err.user_message_text:
                    traceback.print_exc(err.user_message_text)
                else:
                    traceback.print_exc('')

    def create_folder(self, base):
        try:
            self.__dbx.files_get_metadata(base)            
        except:
            self.__dbx.files_create_folder_v2(base)


if __name__ == '__main__':
    token = os.environ.get('DROPBOX_API_TOKEN')
    api = DropboxApi(token)

    print('test - 폴더 리스트 출력')
    print(api.get_folder_entries(''))