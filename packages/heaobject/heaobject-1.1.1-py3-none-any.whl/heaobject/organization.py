import logging

from heaobject.root import Permission, ShareImpl
from heaobject.data import DataObject, SameMimeType
from collections.abc import Iterable, Iterator
from typing import Optional

permission_id_dict = {
    'admin_ids': [Permission.COOWNER],
    'manager_ids': [Permission.VIEWER, Permission.EDITOR, Permission.SHARER, Permission.DELETER],
    'member_ids': [Permission.VIEWER, Permission.SHARER]
}


class Organization(DataObject, SameMimeType):
    """
    Represents a directory in the HEA desktop.
    """

    def __init__(self) -> None:
        super().__init__()
        # id is a super field
        self.__aws_account_ids: list[str] = []  # allow org to have multiple aws accounts
        self.__principal_investigator_id: Optional[str] = None  # this would be a people id
        self.__admin_ids: list[str] = []  # list of user ids to be managers
        self.__manager_ids: list[str] = []  # list of user ids to be managers
        self.__member_ids: list[str] = []  # list of user ids to be members
        # super's name and display name would be used as org name(required)

    @classmethod
    def get_mime_type(cls) -> str:
        """
        Returns the mime type of instances of the Organization class.

        :return: application/x.organization
        """
        return 'application/x.organization'

    @property
    def mime_type(self) -> str:
        """Read-only. The mime type for Organization objects, application/x.organization."""
        return type(self).get_mime_type()

    @property
    def aws_account_ids(self) -> list[str]:
        """
        The list of REST aws account ids that are served by this organization. The property's setter accepts a list of
        strings.
        """
        return [i for i in self.__aws_account_ids]

    @aws_account_ids.setter
    def aws_account_ids(self, value: list[str]) -> None:
        if value is None:
            self.__aws_account_ids = []
        elif not isinstance(value, str):
            self.__aws_account_ids = [str(i) for i in value]
        else:
            self.__aws_account_ids = [str(value)]

    def add_aws_account_id(self, value: str) -> None:
        """
        Adds a REST resource to the list of resources that are served by this component.
        :param value: a Resource object.
        """

        self.__aws_account_ids.append(str(value))

    def remove_aws_account_id(self, value: str) -> None:
        """
        Removes a REST aws_account_id from the list of ids that are served by this organization. Ignores None values.
        :param value: str representing the aws account id.
        """

        self.__aws_account_ids.remove(str(value))

    @property
    def principal_investigator_id(self) -> Optional[str]:
        """
        The principal investigator People ID.
        """
        return self.__principal_investigator_id

    @principal_investigator_id.setter
    def principal_investigator_id(self, principal_investigator_id: Optional[str]) -> None:
        self.__principal_investigator_id = str(principal_investigator_id) \
            if principal_investigator_id is not None else None

    @property
    def admin_ids(self) -> list[str]:
        """
        The organization manager ids.
        """
        return [i for i in self.__admin_ids] if self.__admin_ids else []

    @admin_ids.setter
    def admin_ids(self, admin_ids: list[str]) -> None:
        if admin_ids is None:
            self.__admin_ids = []
        elif not isinstance(admin_ids, str):
            self.__admin_ids = [str(i) for i in admin_ids]
        else:
            self.__admin_ids = [str(admin_ids)]

    def add_admin_id(self, value: str) -> None:
        self.__admin_ids.append(str(value))

    def remove_admin_id(self, value: str) -> None:
        """
        Removes a REST manager id from the list of ids that are served by this organization. Ignores None values.
        :param value:  str representing the manager id.
        """
        self.__admin_ids.remove(str(value))

    @property
    def manager_ids(self) -> list[str]:
        """
        The organization manager ids.
        """
        return [i for i in self.__manager_ids] if self.__manager_ids else []

    @manager_ids.setter
    def manager_ids(self, manager_ids: list[str]) -> None:
        if manager_ids is None:
            self.__manager_ids = []
        elif not isinstance(manager_ids, str):
            self.__manager_ids = [str(i) for i in manager_ids]
        else:
            self.__manager_ids = [str(manager_ids)]

    def add_manager_id(self, value: str) -> None:
        self.__manager_ids.append(str(value))

    def remove_manager_id(self, value: str) -> None:
        """
        Removes a REST manager id from the list of ids that are served by this organization. Ignores None values.
        :param value:  str representing the manager id.
        """
        self.__manager_ids.remove(str(value))

    @property
    def member_ids(self) -> list[str]:
        """
        The organization member ids.
        """
        return [i for i in self.__member_ids]

    @member_ids.setter
    def member_ids(self, member_ids: list[str]) -> None:
        if member_ids is None:
            self.__member_ids = []
        elif not isinstance(member_ids, str):
            self.__member_ids = [str(i) for i in member_ids]
        else:
            self.__member_ids = [str(member_ids)]

    def add_member_id(self, value: str) -> None:
        self.__member_ids.append(str(value))

    def remove_member_id(self, value: str) -> None:
        """
        Removes a REST member id from the list of member ids that are served by this organization. Ignores None values.
        :param value: a str representing the member id.
        """
        self.__member_ids.remove(str(value))

    def dynamic_permission(self, sub: str) -> list[Permission]:
        """
        Returns permissions if the sub is in the member_ids list, or an empty list if not.

        :param sub: the user id (required).
        :return: A list containing Permissions or the empty list.
        """
        try:
            perms: set[Permission] = set()
            if sub == self.principal_investigator_id:
                perms.add(Permission.COOWNER)
            else:
                for p_id in permission_id_dict:
                    if sub in getattr(self, p_id):
                        perms.update(permission_id_dict[p_id])
            return list(perms)
        except:
            logging.exception('Permissions are not correctly configured...returning empty permissions set')
            return []
