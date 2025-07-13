"""
Counterparty-related repositories for the MoySklad API.
"""

from typing import Dict, List, Any, Optional, Tuple

from .base import EntityRepository
from ..api_client import ApiClient
from ..entities.counterparty import Counterparty, ContactPerson, BankAccount
from ..entities.base import Meta
from ..query import QueryBuilder


class CounterpartyRepository(EntityRepository[Counterparty]):
    """Repository for Counterparty entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize counterparty repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/counterparty", Counterparty)

    def get_contact_persons(self, counterparty_id: str) -> List[ContactPerson]:
        """
        Get contact persons for a counterparty.

        Args:
            counterparty_id: Counterparty ID

        Returns:
            List of contact persons
        """
        response = self.api_client.get(f"{self.entity_name}/{counterparty_id}/contactpersons")

        rows = response.get("rows", [])
        return [ContactPerson.from_dict(row) for row in rows]

    def add_contact_person(self, counterparty_id: str, contact_person: ContactPerson) -> ContactPerson:
        """
        Add contact person to a counterparty.

        Args:
            counterparty_id: Counterparty ID
            contact_person: Contact person to add

        Returns:
            Created contact person
        """
        data = contact_person.to_dict()
        response = self.api_client.post(f"{self.entity_name}/{counterparty_id}/contactpersons", data=data)
        return ContactPerson.from_dict(response[0])

    def get_bank_accounts(self, counterparty_id: str) -> List[BankAccount]:
        """
        Get bank accounts for a counterparty.

        Args:
            counterparty_id: Counterparty ID

        Returns:
            List of bank accounts
        """
        response = self.api_client.get(f"{self.entity_name}/{counterparty_id}/accounts")

        rows = response.get("rows", [])
        return [BankAccount.from_dict(row) for row in rows]

    def add_bank_account(self, counterparty_id: str, bank_account: BankAccount) -> BankAccount:
        """
        Add bank account to a counterparty.

        Args:
            counterparty_id: Counterparty ID
            bank_account: Bank account to add

        Returns:
            Created bank account
        """
        data = bank_account.to_dict()
        response = self.api_client.post(f"{self.entity_name}/{counterparty_id}/accounts", data=data)
        return BankAccount.from_dict(response)

    def get_notes(self, counterparty_id: str) -> Dict:
        """
        Get notes for a counterparty.

        Args:
            counterparty_id: Counterparty ID

        Returns:
            Notes data
        """
        return self.api_client.get(f"{self.entity_name}/{counterparty_id}/notes")

    def add_note(self, counterparty_id: str, note_data: Dict) -> Dict:
        """
        Add note to a counterparty.

        Args:
            counterparty_id: Counterparty ID
            note_data: Note data

        Returns:
            Created note data
        """
        return self.api_client.post(f"{self.entity_name}/{counterparty_id}/notes", data=note_data)

    def get_by_phone(self, phone: str) -> List[Counterparty]:
        """
        Find counterparties by phone number.

        Args:
            phone: Phone number

        Returns:
            List of matching counterparties
        """
        query = self.query()
        query.filter().eq("phone", phone)

        counterparties, _ = self.find_all(query)
        return counterparties

    def get_by_email(self, email: str) -> List[Counterparty]:
        """
        Find counterparties by email.

        Args:
            email: Email address

        Returns:
            List of matching counterparties
        """
        query = self.query()
        query.filter().eq("email", email)

        counterparties, _ = self.find_all(query)
        return counterparties

    def get_by_inn(self, inn: str) -> List[Counterparty]:
        """
        Find counterparties by INN (tax number).

        Args:
            inn: INN (tax number)

        Returns:
            List of matching counterparties
        """
        query = self.query()
        query.filter().eq("inn", inn)

        counterparties, _ = self.find_all(query)
        return counterparties