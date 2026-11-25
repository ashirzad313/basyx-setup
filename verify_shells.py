#!/usr/bin/env python3
"""Check the exercise deliverables without starting Docker."""
from zipfile import ZipFile
from xml.etree import ElementTree as ET
from pathlib import Path

BASE = Path(__file__).resolve().parent
NS = {"a": "https://admin-shell.io/aas/3/0"}
SPEC = "aasx/DemoAASV3/DemoAASV3.aas.xml"


def model(archive):
    assert archive.testzip() is None, "Corrupt ZIP member"
    return ET.fromstring(archive.read(SPEC))


def main():
    with ZipFile(BASE / "ExampleV3.aasx") as original, ZipFile(BASE / "changed-shell.aasx") as changed, ZipFile(BASE / "new-shell.aasx") as new:
        before, after, personal = map(model, (original, changed, new))
        query = ".//a:submodelElementList[a:idShort='DemoSMLV3']/a:value/a:property"
        assert [p.findtext('a:idShort', namespaces=NS) for p in before.findall(query, NS)] == ['Element1', 'Element2']
        properties = after.findall(query, NS)
        assert [p.findtext('a:idShort', namespaces=NS) for p in properties] == ['Element1', 'Element2', 'Element3']
        prop = properties[-1]
        assert prop.findtext('a:displayName/a:langStringNameType/a:text', namespaces=NS) == 'Third Element'
        assert prop.findtext('a:valueType', namespaces=NS) == 'xs:string'
        assert prop.findtext('a:value', namespaces=NS) == 'third'
        assert set(original.namelist()) == set(changed.namelist())
        for name in original.namelist():
            if name != SPEC:
                assert original.read(name) == changed.read(name), name
        assert len(after.findall('a:assetAdministrationShells/a:assetAdministrationShell', NS)) == 2
        shells = personal.findall('a:assetAdministrationShells/a:assetAdministrationShell', NS)
        assert len(shells) == 1
        assert shells[0].findtext('a:displayName/a:langStringNameType/a:text', namespaces=NS)
        print('PASS: packages, Element3, personal shell, and supplementary files')


if __name__ == '__main__':
    main()
