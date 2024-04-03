from datetime import datetime
from functools import cached_property

from lxml import etree

from .url_path import URLPath
from .xml_data import XMLDataObject

class SRAFile(XMLDataObject):
    cluster: str
    filename: str
    url: URLPath.from_str
    size: int
    date: datetime.fromisoformat
    md5: str
    version: int
    semantic_name: str
    supertype: str
    sratoolkit: lambda x: bool(int(x))

    @cached_property
    def alternatives(self):
        return [
            SRAAlternatives(
                etree.ElementTree(elem)
            ) for elem in self.xml.xpath("./Alternatives")
        ]

class SRAAlternatives(XMLDataObject):
    url: URLPath.from_str
    free_egress: str
    access_type: str
    org: str
