# -*- coding: utf-8 -*-#

from typing import List
from google.oauth2 import service_account
from googleapiclient.discovery import build


class GSuiteClient:
    def __init__(
        self, permission_file_path: str, permission_scopes: List[str], admin_user: str
    ):
        self._permission_file_path = permission_file_path
        self._permission_scopes = permission_scopes
        self._admin_user = admin_user
        self._service = None
        self._credentials = None

    def create_service(self):
        if self._service is None:
            self._service = build(
                "admin",
                "directory_v1",
                credentials=self.credentials,
                cache_discovery=False,
            )

    @property
    def user_service(self):
        self.create_service()
        return self._service.users()

    @property
    def group_service(self):
        self.create_service()
        return self._service.groups()

    @property
    def member_service(self):
        self.create_service()
        return self._service.members()

    @property
    def credentials(self):
        if self._credentials is None:
            credentials = service_account.Credentials.from_service_account_file(
                filename=self._permission_file_path, scopes=self._permission_scopes
            )
            self._credentials = credentials.with_subject(self._admin_user)
        return self._credentials


class GSuiteUserFetcher:
    def __init__(self, service):
        self._service = service

    def fetch_user_by_email(self, user_email: str):
        user_data = self._service.get(userKey=user_email, projection="full").execute()
        return user_data

    def fetch_users(self):
        return self._service.list(domain='aidkr.com', projection="full").execute()


class GSuiteGroupFetcher:
    def __init__(self, service):
        self._service = service

    def fetch_group_by_key(self, key: str):
        group_data = self._service.get(groupKey=key).execute()
        return group_data

    def fetch_groups(self, params):
        return self._service.list(**params).execute()


class GSuiteMemberFetcher:
    def __init__(self, service):
        self._service = service

    def fetch_members_by_group_key(self, group_key: str):
        member_data = self._service.list(groupKey=group_key).execute()
        return member_data

    def fetch_member(self, groupKey: str, memberKey: str):
        return self._service.get(groupKey=groupKey, memberKey=memberKey).execute()
