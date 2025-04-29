"""
Constants and enumerations for the MoySklad API.
"""

from enum import Enum, auto


class CompanyType(str, Enum):
    """Company types in MoySklad."""
    LEGAL = "legal"
    ENTREPRENEUR = "entrepreneur"
    INDIVIDUAL = "individual"


class PaymentItemType(str, Enum):
    """Payment item types in MoySklad."""
    GOOD = "good"
    SERVICE = "service"
    WORK = "work"
    CONSIGNMENT = "consignment"
    COMMISSION_FEE = "commission_fee"
    ANOTHER_PAYMENT = "another_payment"
    PROPERTY_RIGHT = "property_right"
    EXCISE = "excise"
    AGENT_COMMISSION = "agent_commission"
    COMPOSITE_PAYMENT_ITEM = "composite_payment_item"
    ANOTHER_COMPOSITE_PAYMENT_ITEM = "another_composite_payment_item"


class TrackingType(str, Enum):
    """Tracking types for products."""
    NOT_TRACKED = "NOT_TRACKED"
    SERIAL_NUMBERS = "SERIAL_NUMBERS"
    TOBACCO = "TOBACCO"
    SHOES = "SHOES"
    LP_CLOTHES = "LP_CLOTHES"
    LP_LINENS = "LP_LINENS"
    MILK = "MILK"
    WATER = "WATER"
    OTP = "OTP"


class StateType(str, Enum):
    """Entity state types."""
    REGULAR = "Regular"
    SUCCESSFUL = "Successful"
    UNSUCCESSFUL = "Unsuccessful"


class DocumentStatus(str, Enum):
    """Common document statuses."""
    NEW = "new"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELED = "canceled"


class TaxSystem(str, Enum):
    """Tax systems in MoySklad."""
    GENERAL_TAX_SYSTEM = "GENERAL_TAX_SYSTEM"
    SIMPLIFIED_TAX_SYSTEM_INCOME = "SIMPLIFIED_TAX_SYSTEM_INCOME"
    SIMPLIFIED_TAX_SYSTEM_INCOME_OUTCOME = "SIMPLIFIED_TAX_SYSTEM_INCOME_OUTCOME"
    UNIFIED_AGRICULTURAL_TAX = "UNIFIED_AGRICULTURAL_TAX"
    PRESUMPTIVE_TAX_SYSTEM = "PRESUMPTIVE_TAX_SYSTEM"
    PATENT_BASED = "PATENT_BASED"