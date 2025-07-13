"""
Counterparty-related entity models for the MoySklad API.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional, ClassVar

from .base import Meta, MetaEntity
from ..constants import CompanyType


@dataclass
class ContactPerson(MetaEntity):
    """Contact person entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/counterparty/contactperson"


    description: Optional[str] = None
    externalCode: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    agent: Optional[Dict] = None



@dataclass
class BankAccount(MetaEntity):
    """Bank account entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/counterparty/account"

    description: Optional[str] = None
    accountNumber: Optional[str] = None
    bankName: Optional[str] = None
    bankLocation: Optional[str] = None
    correspondentAccount: Optional[str] = None
    bic: Optional[str] = None
    isDefault: Optional[bool] = None
    agent: Optional[Dict] = None


@dataclass
class Counterparty(MetaEntity):
    """Counterparty entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/counterparty"

    code: Optional[str] = None
    externalCode: Optional[str] = None
    companyType: Optional[str] = None
    legalTitle: Optional[str] = None
    legalAddress: Optional[str] = None
    inn: Optional[str] = None
    kpp: Optional[str] = None
    ogrn: Optional[str] = None
    okpo: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
    actualAddress: Optional[str] = None
    accounts: Optional[Dict] = None
    tags: Optional[List[str]] = None
    contactpersons: Optional[Dict] = None
    notes: Optional[Dict] = None
    state: Optional[Dict] = None
    syncId: Optional[str] = None
    salesAmount: Optional[int] = None
    bonusPoints: Optional[int] = None
    bonusProgram: Optional[Dict] = None
    discountCardNumber: Optional[str] = None
    discounts: Optional[List[Dict]] = None
    priceType: Optional[Dict] = None
    created: Optional[str] = None
    description: Optional[str] = None
    actualAddressFull: Optional[Dict] = None

    birthDate: Optional[datetime] = None
    certificateDate: Optional[datetime] = None
    certificateNumber: Optional[str] = None
    legalAddressFull: Optional[Dict] = None
    legalFirstName: Optional[str] = None
    legalLastName: Optional[str] = None
    legalMiddleName: Optional[str] = None
    sex: Optional[str] = None

    owner: Optional[Dict] = None
    shared: Optional[bool] = None
    group: Optional[Dict] = None
    archived: Optional[bool] = None
    files: Optional[Dict] = None

    @staticmethod
    def get_href(entity_id: str) -> str:
        return f'https://api.moysklad.ru/api/remap/1.2/entity/counterparty/{entity_id}'

    def __post_init__(self):
        """Post-initialization hook."""
        super().__post_init__()

        # Convert string enum values to actual enum values if needed
        if isinstance(self.companyType, str):
            try:
                self.companyType = CompanyType(self.companyType)
            except ValueError:
                pass