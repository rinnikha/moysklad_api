"""
Organization-related entity models for the MoySklad API.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, ClassVar

from .base import Meta, MetaEntity
from ..constants import CompanyType


@dataclass
class Organization(MetaEntity):
    """Organization entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/organization"

    actualAddress: Optional[str] = None
    actualAddressFull: Optional[Dict] = None
    archived: Optional[bool] = None
    attributes: Optional[List[Dict]] = None
    code: Optional[str] = None
    companyType: Optional[str] = None
    description: Optional[str] = None
    email: Optional[str] = None
    externalCode: Optional[str] = None
    fax: Optional[str] = None
    files: Optional[Dict] = None
    group: Optional[Dict] = None
    inn: Optional[str] = None
    kpp: Optional[str] = None
    legalAddress: Optional[str] = None
    legalAddressFull: Optional[Dict] = None
    legalTitle: Optional[str] = None
    legalFirstName: Optional[str] = None
    legalLastName: Optional[str] = None
    trackingContractNumber: Optional[str] = None
    trackingContractDate: Optional[str] = None
    ogrn: Optional[str] = None
    ogrnip: Optional[str] = None
    okpo: Optional[str] = None
    owner: Optional[Dict] = None
    payerVat: Optional[bool] = None
    phone: Optional[str] = None
    shared: Optional[bool] = None
    accounts: Optional[Dict] = None
    isEgaisEnable: Optional[bool] = None
    utmUrl: Optional[str] = None
    fsrarId: Optional[str] = None
    payerVat105: Optional[bool] = None
    certificateDate: Optional[str] = None
    chiefAccountant: Optional[str] = None
    certificateNumber: Optional[str] = None
    director: Optional[str] = None
    directorPosition: Optional[str] = None
    bonusProgram: Optional[Dict] = None
    bonusPoints: Optional[float] = 0
    advancePaymentVat: Optional[float] = 0

    created: Optional[str] = None
    updated: Optional[str] = None

    @staticmethod
    def get_href(entity_id: str) -> str:
        return f'https://api.moysklad.ru/api/remap/1.2/entity/organization/{entity_id}'

    def __post_init__(self):
        """Post-initialization hook."""
        super().__post_init__()

        # Convert string enum values to actual enum values if needed
        if isinstance(self.companyType, str):
            try:
                self.companyType = CompanyType(self.companyType)
            except ValueError:
                pass





@dataclass
class Employee(MetaEntity):
    """Employee entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/employee"

    firstName: Optional[str] = None
    # middleName: Optional[str] = None
    lastName: Optional[str] = None
    fullName: Optional[str] = None
    shortFio: Optional[str] = None
    archived: Optional[bool] = None
    accountId: Optional[str] = None
    uid: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    description: Optional[str] = None
    externalCode: Optional[str] = None
    code: Optional[str] = None
    owner: Optional[Dict] = None
    shared: Optional[bool] = None
    group: Optional[Dict] = None
    attributes: Optional[List[Dict]] = None
    cashiers: Optional[List[Dict]] = None
    permissions: Optional[Dict] = None
    image: Optional[Dict] = None
    salary: Optional[Dict] = None

    created: Optional[str] = None
    updated: Optional[str] = None


@dataclass
class Group(MetaEntity):
    """Group entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/group"

    index: Optional[int] = None

    @staticmethod
    def get_href(entity_id: str) -> str:
        return f'https://api.moysklad.ru/api/remap/1.2/entity/group/{entity_id}'


@dataclass
class Store(MetaEntity):
    """Store entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/store"

    address: Optional[str] = None
    addressFull: Optional[Dict] = None
    archived: Optional[bool] = None
    attributes: Optional[List[Dict]] = None
    code: Optional[str] = None
    description: Optional[str] = None
    externalCode: Optional[str] = None
    group: Optional[Dict] = None
    owner: Optional[Dict] = None
    parent: Optional[Dict] = None
    pathName: Optional[str] = None
    shared: Optional[bool] = None
    zones: Optional[List[Dict]] = None
    slots: Optional[List[Dict]] = None

    @staticmethod
    def get_href(entity_id: str) -> str:
        return f'https://api.moysklad.ru/api/remap/1.2/entity/store/{entity_id}'