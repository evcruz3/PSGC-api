from typing import Optional
from pydantic import (
    BaseModel,
    Field,
)

class PSGCObject(BaseModel):
    """
    A general PSGC object
    """

    code: str = Field(
        ..., description='A 10-characted PSGC Code', title='PSGC Code'
    )
    name: str = Field(
        ..., description='Name of place', title='Name'
    )
    geographic_level: str = Field(
        ...,
        description='Geographic Level of place according to PSA',
        title='Geographic Level',
    )
    barangay_code: Optional[str] = Field(
        None,
        description='For holding the extracted barangay code information of the place, if applicable',
        title='Barangay Code',
        nullable=True,
    )
    barangay_name: Optional[str] = Field(
        None,
        description='For holding the extracted barangay name of the place, if applicable',
        title='Barangay Code',
        nullable=True,
    )
    city_municipality_code: Optional[str] = Field(
        None,
        description='For holding the extracted city-municipality code information of the place, if applicable',
        title='City Municipality Code',
        nullable=True,
    )
    city_municipality_name: Optional[str] = Field(
        None,
        description='For holding the extracted city-municipality name information of the place, if applicable',
        title='City Municipality Code',
        nullable=True,
    )
    province_code: Optional[str] = Field(
        None,
        description='For holding the extracted province code information of the place, if applicable',
        title='Province Code',
        nullable=True,
    )
    province_name: Optional[str] = Field(
        None,
        description='For holding the extracted province name information of the place, if applicable',
        title='Province Code',
        nullable=True,
    )
    region_code: Optional[str] = Field(
        None,
        description='For holding the extracted region code information of the place, if applicable',
        title='Region Code',
        nullable=True,
    )
    region_name: Optional[str] = Field(
        None,
        description='For holding the extracted region name information of the place, if applicable',
        title='Region Code',
        nullable=True,
    )