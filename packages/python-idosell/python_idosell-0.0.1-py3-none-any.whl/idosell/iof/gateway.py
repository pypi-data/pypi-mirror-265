from pydantic import HttpUrl
from pydantic_xml.model import BaseXmlModel, element, attr, wrapped
import datetime as dt


class ShowcaseImage(BaseXmlModel, tag="showcase_image"):
    url: HttpUrl = attr()


class Address(BaseXmlModel, tag="address"):
    street: str | None = element(default=None)
    zipcode: str | None = element(default=None)
    city: str | None = element(default=None)
    country: str | None = element(default=None)
    province: str | None = element(default=None)


class Offer(BaseXmlModel, tag="offer"):
    created: dt.datetime | None = attr(default=None)
    expires: dt.datetime | None = attr(default=None)


class Time(BaseXmlModel, tag="time"):
    offers: list[Offer]


class Meta(BaseXmlModel, tag="meta"):
    long_name: str = element()
    short_name: str = element()
    showcase_image: ShowcaseImage = element()
    email: str = element()
    tel: str = element()
    fax: str = element()
    www: str = element()
    address: Address
    time: Time


class HashChangedUrl(BaseXmlModel):
    url: HttpUrl = attr()
    hash: str | None = attr(default=None)
    changed: dt.datetime | None = attr(default=None)


class Change(HashChangedUrl, tag="change"):
    pass


class LinkedFull(HashChangedUrl, tag="full"):
    changes: list[Change] = wrapped("changes", element(tag="change"))


class Gateway(BaseXmlModel, tag="provider_description"):
    file_format: str = attr()
    version: str = attr()
    generated_by: str = attr()
    generated: dt.datetime = attr()
    meta: Meta
    full: LinkedFull
    light: HashChangedUrl
    categories: HashChangedUrl
    sizes: HashChangedUrl
    producers: HashChangedUrl | None = element(default=None)
    stocks: HashChangedUrl | None = element(default=None)
    series: HashChangedUrl | None = element(default=None)
    warranties: HashChangedUrl | None = element(default=None)
    preset: HashChangedUrl | None = element(default=None)
