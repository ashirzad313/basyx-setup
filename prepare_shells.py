#!/usr/bin/env python3
"""Reproduce the assignment packages offline from the original example."""
import argparse
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

BASE = Path(__file__).resolve().parent
NS = "https://admin-shell.io/aas/3/0"
ET.register_namespace("", NS)
SPEC = "aasx/DemoAASV3/DemoAASV3.aas.xml"


def q(name):
    return f"{{{NS}}}{name}"


def add(parent, name, text=None):
    child = ET.SubElement(parent, q(name))
    child.text = text
    return child


def display(parent, name):
    lang = add(add(parent, "displayName"), "langStringNameType")
    add(lang, "language", "en")
    add(lang, "text", name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", default="ashirzad313", help="Your actual display name")
    args = parser.parse_args()
    if not args.name.strip():
        parser.error("Name must not be empty")
    with ZipFile(BASE / "ExampleV3.aasx") as source:
        root = ET.fromstring(source.read(SPEC))
        model = next(s for s in root.findall(f"{q('submodels')}/{q('submodel')}")
                     if s.findtext(q("idShort")) == "DemoSubmodelV3")
        target = next(s for s in model.iter(q("submodelElementList"))
                      if s.findtext(q("idShort")) == "DemoSMLV3")
        values = target.find(q("value"))
        assert values is not None
        prop = add(values, "property")
        add(prop, "idShort", "Element3")
        display(prop, "Third Element")
        add(prop, "valueType", "xs:string")
        add(prop, "value", "third")
        ET.indent(root, space="  ")
        with ZipFile(BASE / "changed-shell.aasx", "w", ZIP_DEFLATED) as dest:
            for info in source.infolist():
                data = ET.tostring(root, encoding="utf-8", xml_declaration=True) if info.filename == SPEC else source.read(info)
                dest.writestr(info.filename, data)
        root = ET.Element(q("environment"))
        shell = add(add(root, "assetAdministrationShells"), "assetAdministrationShell")
        add(shell, "idShort", "PersonalShell")
        display(shell, args.name)
        add(shell, "id", "urn:basyx-setup:aas:personal")
        asset = add(shell, "assetInformation")
        add(asset, "assetKind", "Instance")
        add(asset, "globalAssetId", "urn:basyx-setup:asset:personal")
        ET.indent(root, space="  ")
        with ZipFile(BASE / "new-shell.aasx", "w", ZIP_DEFLATED) as dest:
            for name in ("aasx/aasx-origin", "_rels/.rels", "aasx/_rels/aasx-origin.rels", "[Content_Types].xml"):
                dest.writestr(name, source.read(name))
            dest.writestr(SPEC, ET.tostring(root, encoding="utf-8", xml_declaration=True))
    print("Created changed-shell.aasx and new-shell.aasx")


if __name__ == "__main__":
    main()
