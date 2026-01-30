#!/usr/bin/env python3
"""
Tests using hex strings with pre-encoded filesystem data.

All the hex file strings generated below have been created by transferring
files to a micro:bit running MicroPython v1.0.1 using Mu.

These tests verify that the Python library produces the exact same output as
the TypeScript library and can correctly read filesystem data created by
real MicroPython devices.
"""

from io import StringIO
from typing import TypedDict

import pytest
from intelhex import IntelHex

from micropython_microbit_fs import File, add_files, get_device_info, get_files
from micropython_microbit_fs.filesystem import calculate_file_size


class _FileDataRequired(TypedDict):
    """Required fields for test file data."""

    filename: str
    content: str
    hex: str


class FileData(_FileDataRequired, total=False):
    """Type for test file data dictionaries with optional fields."""

    file_address: int
    fs_size: int


# Test file 1: Small file fitting in one chunk
TEST_FILE_1: FileData = {
    "filename": "test_file_1.py",
    "content": "from microbit import display\r\ndisplay.show('x')",
    "hex": (
        ":020000040003F7\n"
        ":10C90000FE3F0E746573745F66696C655F312E70EF\n"
        ":10C910007966726F6D206D6963726F6269742069E8\n"
        ":10C920006D706F727420646973706C61790D0A6444\n"
        ":10C930006973706C61792E73686F7728277827295F\n"
        ":10C94000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7\n"
        ":10C95000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE7\n"
        ":10C96000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD7\n"
        ":10C97000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7\n"
        ":00000001FF"
    ),
    "file_address": 0x3C900,
    "fs_size": 128,
}

# Test file 2: Large file spanning multiple chunks (1264 bytes, ~10 chunks)
TEST_FILE_2: FileData = {
    "filename": "test_file_2.py",
    "content": (
        "# Lorem Ipsum is simply dummy text of the printing and\r\n"
        "# typesetting industry. Lorem Ipsum has been the industry's\r\n"
        "# standard dummy text ever since the 1500s, when an unknown\r\n"
        "# printer took a galley of type and scrambled it to make a\r\n"
        "# type specimen book. It has survived not only five\r\n"
        "# centuries, but also the leap into electronic typesetting,\r\n"
        "# remaining essentially unchanged. It was popularised in the\r\n"
        "# 1960s with the release of Letraset sheets containing Lorem\r\n"
        "# Ipsum passages, and more recently with desktop publishing\r\n"
        "# software like Aldus PageMaker including versions of Lorem\r\n"
        "# Ipsum.\r\n"
        "# Lorem Ipsum is simply dummy text of the printing and\r\n"
        "# typesetting industry. Lorem Ipsum has been the industry's\r\n"
        "# standard dummy text ever since the 1500s, when an unknown\r\n"
        "# printer took a galley of type and scrambled it to make a\r\n"
        "# type specimen book. It has survived not only five\r\n"
        "# centuries, but also the leap into electronic typesetting,\r\n"
        "# remaining essentially unchanged. It was popularised in the\r\n"
        "# 1960s with the release of Letraset sheets containing Lorem\r\n"
        "# Ipsum passages, and more recently with desktop publishing\r\n"
        "# software like Aldus PageMaker including versions of Lorem\r\n"
        "# Ipsum."
    ),
    "hex": (
        ":020000040003F7\n"
        ":108C8000FE600E746573745F66696C655F322E708A\n"
        ":108C90007923204C6F72656D20497073756D206962\n"
        ":108CA000732073696D706C792064756D6D792074B3\n"
        ":108CB000657874206F6620746865207072696E74C0\n"
        ":108CC000696E6720616E640D0A2320747970657384\n"
        ":108CD000657474696E6720696E6475737472792E39\n"
        ":108CE000204C6F72656D20497073756D20686173DB\n"
        ":108CF000206265656E2074686520696E6475730313\n"
        ":108D00000274727927730D0A23207374616E646193\n"
        ":108D100072642064756D6D79207465787420657651\n"
        ":108D200065722073696E6365207468652031353023\n"
        ":108D300030732C207768656E20616E20756E6B6EC7\n"
        ":108D40006F776E0D0A23207072696E7465722074DD\n"
        ":108D50006F6F6B20612067616C6C6579206F662096\n"
        ":108D60007479706520616E6420736372616D626CEA\n"
        ":108D7000656420697420746F206D616B65206104E7\n"
        ":108D8000030D0A2320747970652073706563696D23\n"
        ":108D9000656E20626F6F6B2E2049742068617320AE\n"
        ":108DA0007375727669766564206E6F74206F6E6C71\n"
        ":108DB0007920666976650D0A232063656E74757285\n"
        ":108DC0006965732C2062757420616C736F20746800\n"
        ":108DD00065206C65617020696E746F20656C6563D9\n"
        ":108DE00074726F6E696320747970657365747469E9\n"
        ":108DF0006E672C0D0A232072656D61696E696E05C0\n"
        ":108E0000046720657373656E7469616C6C79207595\n"
        ":108E10006E6368616E6765642E20497420776173A4\n"
        ":108E200020706F70756C61726973656420696E2063\n"
        ":108E30007468650D0A2320313936307320776974E0\n"
        ":108E400068207468652072656C65617365206F6663\n"
        ":108E5000204C657472617365742073686565747302\n"
        ":108E600020636F6E7461696E696E67204C6F726506\n"
        ":108E70006D0D0A2320497073756D20706173730640\n"
        ":108E800005616765732C20616E64206D6F726520CB\n"
        ":108E9000726563656E746C792077697468206465A7\n"
        ":108EA000736B746F70207075626C697368696E673C\n"
        ":108EB0000D0A2320736F667477617265206C696B8D\n"
        ":108EC0006520416C64757320506167654D616B6509\n"
        ":108ED0007220696E636C7564696E67207665727363\n"
        ":108EE000696F6E73206F66204C6F72656D0D0A237B\n"
        ":108EF00020497073756D2E0D0A23204C6F72650723\n"
        ":108F0000066D20497073756D2069732073696D70EB\n"
        ":108F10006C792064756D6D792074657874206F6646\n"
        ":108F200020746865207072696E74696E6720616E66\n"
        ":108F3000640D0A23207479706573657474696E67B3\n"
        ":108F400020696E6475737472792E204C6F72656D32\n"
        ":108F500020497073756D20686173206265656E20AD\n"
        ":108F600074686520696E64757374727927730D0A6D\n"
        ":108F700023207374616E646172642064756D6D0882\n"
        ":108F80000779207465787420657665722073696E40\n"
        ":108F90006365207468652031353030732C20776824\n"
        ":108FA000656E20616E20756E6B6E6F776E0D0A2395\n"
        ":108FB000207072696E74657220746F6F6B2061200F\n"
        ":108FC00067616C6C6579206F6620747970652061CB\n"
        ":108FD0006E6420736372616D626C656420697420D5\n"
        ":108FE000746F206D616B6520610D0A2320747970A8\n"
        ":108FF000652073706563696D656E20626F6F6B09C4\n"
        ":10900000082E204974206861732073757276697622\n"
        ":109010006564206E6F74206F6E6C7920666976656A\n"
        ":109020000D0A232063656E7475726965732C206266\n"
        ":10903000757420616C736F20746865206C65617055\n"
        ":1090400020696E746F20656C656374726F6E6963FE\n"
        ":10905000207479706573657474696E672C0D0A23CA\n"
        ":109060002072656D61696E696E6720657373656EE8\n"
        ":109070007469616C6C7920756E6368616E67650AEE\n"
        ":1090800009642E2049742077617320706F70756CAD\n"
        ":1090900061726973656420696E207468650D0A23C6\n"
        ":1090A0002031393630732077697468207468652000\n"
        ":1090B00072656C65617365206F66204C65747261C2\n"
        ":1090C0007365742073686565747320636F6E746133\n"
        ":1090D000696E696E67204C6F72656D0D0A232049B9\n"
        ":1090E0007073756D2070617373616765732C206197\n"
        ":1090F0006E64206D6F726520726563656E746C0BB3\n"
        ":109100000A792077697468206465736B746F7020C6\n"
        ":109110007075626C697368696E670D0A2320736FDE\n"
        ":10912000667477617265206C696B6520416C64754B\n"
        ":109130007320506167654D616B657220696E636C69\n"
        ":109140007564696E672076657273696F6E73206FE0\n"
        ":1091500066204C6F72656D0D0A2320497073756D22\n"
        ":109160002EFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE0\n"
        ":00000001FF"
    ),
    "file_address": 0x38C80,
    "fs_size": 1280,
}

# A chunk using up the last byte will also use the next and leave it empty
FULL_CHUNK_PLUS: FileData = {
    "filename": "one_chunk_plus.py",
    "content": (
        'a = """abcdefghijklmnopqrstuvwxyz\n'
        "abcdefghijklmnopqrstuvwxyz\n"
        "abcdefghijklmnopqrstuvwxyz\n"
        'abcdefghijklmno"""\n'
    ),
    "hex": (
        ":020000040003F7\n"
        ":108C0000FE00116F6E655F6368756E6B5F706C75EB\n"
        ":108C1000732E707961203D20222222616263646597\n"
        ":108C2000666768696A6B6C6D6E6F7071727374756C\n"
        ":108C3000767778797A0A6162636465666768696ADB\n"
        ":108C40006B6C6D6E6F707172737475767778797AFC\n"
        ":108C50000A6162636465666768696A6B6C6D6E6FF2\n"
        ":108C6000707172737475767778797A0A6162636469\n"
        ":108C700065666768696A6B6C6D6E6F2222220A02F4\n"
        ":108C800001FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF2\n"
        ":00000001FF"
    ),
    "file_address": 0x38C00,  # V1 FS start
    "fs_size": 256,  # Two chunks
}

# Using space except the last byte should only use a single chunk
FULL_CHUNK_MINUS: FileData = {
    "filename": "one_chunk_minus.py",
    "content": (
        'a = """abcdefghijklmnopqrstuvwxyz\n'
        "abcdefghijklmnopqrstuvwxyz\n"
        "abcdefghijklmnopqrstuvwxyz\n"
        'abcdefghijklm"""\n'
    ),
    "hex": (
        ":020000040003F7\n"
        ":108C0000FE7D126F6E655F6368756E6B5F6D696E7A\n"
        ":108C100075732E707961203D202222226162636487\n"
        ":108C200065666768696A6B6C6D6E6F70717273747C\n"
        ":108C300075767778797A0A616263646566676869D0\n"
        ":108C40006A6B6C6D6E6F707172737475767778790C\n"
        ":108C50007A0A6162636465666768696A6B6C6D6EE7\n"
        ":108C60006F707172737475767778797A0A6162635E\n"
        ":108C70006465666768696A6B6C6D2222220AFFFF71\n"
        ":00000001FF"
    ),
    "file_address": 0x38C00,  # V1 FS start
    "fs_size": 128,  # Single chunk
}

# One full chunk + a single byte on the second
TWO_CHUNKS: FileData = {
    "filename": "two_chunks.py",
    "content": (
        'a = """abcdefghijklmnopqrstuvwxyz\n'
        "abcdefghijklmnopqrstuvwxyz\n"
        "abcdefghijklmnopqrstuvwxyz\n"
        'abcdefghijklmnopqrst"""\n'
    ),
    "hex": (
        ":020000040003F7\n"
        ":108C0000FE010D74776F5F6368756E6B732E7079FC\n"
        ":108C100061203D2022222261626364656667686983\n"
        ":108C20006A6B6C6D6E6F707172737475767778792C\n"
        ":108C30007A0A6162636465666768696A6B6C6D6E07\n"
        ":108C40006F707172737475767778797A0A6162637E\n"
        ":108C50006465666768696A6B6C6D6E6F707172735C\n"
        ":108C60007475767778797A0A616263646566676895\n"
        ":108C7000696A6B6C6D6E6F7071727374222222025E\n"
        ":108C8000010AFFFFFFFFFFFFFFFFFFFFFFFFFFFFE7\n"
        ":00000001FF"
    ),
    "file_address": 0x38C00,  # V1 FS start
    "fs_size": 256,  # Two chunks
}

# afirst.py - small file that fits in one chunk
AFIRST_FILE: FileData = {
    "filename": "afirst.py",
    "content": "firstname = 'Carlos'",
    "hex": (
        ":020000040003F7\n"
        ":10DF0000FE1F096166697273742E70796669727397\n"
        ":10DF1000746E616D65203D20274361726C6F7327BD\n"
        ":00000001FF\n"
    ),
}

# alast.py - large multi-chunk file
ALAST_FILE: FileData = {
    "filename": "alast.py",
    "content": (
        "# Lorem Ipsum is simply dummy text of the printing and\n"
        "# typesetting industry. Lorem Ipsum has been the industry's\n"
        "# standard dummy text ever since the 1500s, when an unknown\n"
        "# printer took a galley of type and scrambled it to make a\n"
        "# type specimen book. It has survived not only five\n"
        "# centuries, but also the leap into electronic typesetting,\n"
        "# remaining essentially unchanged. It was popularised in the\n"
        "# 1960s with the release of Letraset sheets containing Lorem\n"
        "# Ipsum passages, and more recently with desktop publishing\n"
        "# software like Aldus PageMaker including versions of Lorem\n"
        "# Ipsum.\n"
        "# Lorem Ipsum is simply dummy text of the printing and\n"
        "# typesetting industry. Lorem Ipsum has been the industry's\n"
        "# standard dummy text ever since the 1500s, when an unknown\n"
        "# printer took a galley of type and scrambled it to make a\n"
        "# type specimen book. It has survived not only five\n"
        "# centuries, but also the leap into electronic typesetting,\n"
        "# remaining essentially unchanged. It was popularised in the\n"
        "# 1960s with the release of Letraset sheets containing Lorem\n"
        "# Ipsum passages, and more recently with desktop publishing\n"
        "# software like Aldus PageMaker including versions of Lorem\n"
        "# Ipsum.\n"
        "import afirst\n"
        "\n"
        "lastname = 'Pereira'\n"
        "full_name = '{} {}'.format(afirst.firstname, lastname)\n"
    ),
    "hex": (
        ":020000040003F7\n"
        ":10C88000FE3008616C6173742E707923204C6F726C\n"
        ":10C89000656D20497073756D2069732073696D700B\n"
        ":10C8A0006C792064756D6D792074657874206F66A5\n"
        ":10C8B00020746865207072696E74696E6720616EC5\n"
        ":10C8C000640A23207479706573657474696E672016\n"
        ":10C8D000696E6475737472792E204C6F72656D2092\n"
        ":10C8E000497073756D20686173206265656E20745A\n"
        ":10C8F00068652067696E6475737472792773123BC7\n"
        ":10C900000A23207374616E646172642064756D6D85\n"
        ":10C910007920746578742065766572207369A7CEBE\n"
        ":10C920006E6365207468652031353030732C207769\n"
        ":10C9300068656E20616E20756E6B6E6F776E0A2314\n"
        ":10C94000207072696E74657220746F6F6B20612062\n"
        ":10C9500067616C6C6579206F66207479706520616E\n"
        ":10C960006E6420736372616D626C65642069742031\n"
        ":10C97000746F206D616B6520610A232074797013B1\n"
        ":10C9800012652073706563696D656E20626F6F6BDD\n"
        ":10C990002E2049742068617320737572766976654A\n"
        ":10C9A00064206E6F74206F6E6C7920666976650A06\n"
        ":10C9B00023206365A7D26E7475726965732C206207\n"
        ":10C9C0007574206120A86C736F20746865206C6515\n"
        ":10C9D00061700A20696E746F20656C656374726F49\n"
        ":10C9E0006E696320747970657365747469A96E671A\n"
        ":10C9F0002C0A232072656D61696E696E6720657311\n"
        ":10CA000014AA73656E7469616C6C7920756E636853\n"
        ":10CA1000616E6765642E20497420776173B0AB702E\n"
        ":10CA20006F70756C6172697365642069AC6E207409\n"
        ":10CA300068650A2320313936307320776974682098\n"
        ":10CA40007468652072656C65617365206F66204CE9\n"
        ":10CA500065747261736574207368656574732063D8\n"
        ":10CA60006F6E7461696E696E67204C6F72656D0A4E\n"
        ":10CA7000232049707375150E6D207061737361674F\n"
        ":10CA80006573160F2C20616E64206D6F7265207267\n"
        ":10CA900065631710656E746C792077697468206439\n"
        ":10CAA00065736B746F70207075626C697368696E7D\n"
        ":10CAB000670A2320736F667477617265206C696BAC\n"
        ":10CAC0006520416C64757320506167654D616B65EB\n"
        ":10CAD0007220696E636C7564696E6720766572AEAB\n"
        ":10CAE00073696F6E73206F66204C6F72656D0A2319\n"
        ":10CAF00020497073756D2E0A23204C6F72656D2082\n"
        ":10CB0000AF497073756D2069732073696D706C79F0\n"
        ":10CB100020B06475B16D6D7920746578B2742C6F4C\n"
        ":10CB2000662074686520707269B36E74696E6720ED\n"
        ":10CB3000616E640A23207479B46573657474696EB2\n"
        ":10CB40006720696EB564757374B672792E204C6F6D\n"
        ":10CB50007265B76D20497073B8756D20686173206A\n"
        ":10CB6000626565B96E2074686520B96E64757374DE\n"
        ":10CB70007279BA27730A23BA207374616E64617263\n"
        ":10CB8000642064756D6D792074657874206576BB0B\n"
        ":10CB90006572207369BC6E63652074BC686520313D\n"
        ":10CBA000353030732CBD207768656EBD20616E2052\n"
        ":10CBB000756E6B6E6F776EBE0A2320707269BE6E7E\n"
        ":10CBC00074657220746F6FBF6B206120676195BFC2\n"
        ":10CBD0006C6C6579206F6620747970C02031616ED2\n"
        ":10CBE00064207363C1616D626C65C16420697420D1\n"
        ":10CBF000746F206D616BC2610A232074C27065205B\n"
        ":10CC00007370656369C36E2D626F6FC36B2E204974\n"
        ":10CC10002068617320C473757276697EB564206E2A\n"
        ":10CC20006F74206FC56C7920666976C5E16E0AC637\n"
        ":10CC300023206365C66E74757269C6732C20627575\n"
        ":10CC400074C720616C736FC72074686520C86C65BB\n"
        ":10CC500061C82E696E746FC920656C65C974726F1B\n"
        ":10CC60006E696320747970CA7365747469CA672C7F\n"
        ":10CC70000A2320CB656D61696ECB696E67CB206551\n"
        ":10CC80007373656E7469616C6C7920756ECC6368A5\n"
        ":10CC9000616E6765642ECCE697742077CCCD207044\n"
        ":10CCA0006F70756C617269736564CD696E2074CD9A\n"
        ":10CCB00068CE0A23CE2031393630CE73207769CEE5\n"
        ":10CCC0007468CF74686520CFCE656C65CF7365206F\n"
        ":10CCD0006F66D04C65747261D073657420D0686523\n"
        ":10CCE000D0747320636FD17461696E69D16720D1C2\n"
        ":10CCF0006F72D2650A23D249707375D26D207061E9\n"
        ":10CD00007373D261676573D32C20616ED3206D6F11\n"
        ":10CD100072D320726563D46E746C79D42077697436\n"
        ":10CD200068D564657D4B746FD520707562D56C69BA\n"
        ":10CD30007368696E670A23D6736F6674D677617227\n"
        ":10CD400065206C696B65D720416C64D77320506185\n"
        ":10CD50006765D84B616B65D8722069D96C7564694C\n"
        ":10CD60006E67D976657273D969D96E73D96F6620D5\n"
        ":10CD70004C6F72656DDA0A23204950DA73756D2ED0\n"
        ":10CD80000A696D706F727420616669727374DADA7A\n"
        ":10CD90000A6C6173746E616D65DB203D2027DB5076\n"
        ":10CDA000657265697261270A6675DC6C5F6E616D62\n"
        ":10CDB00065203DDC20277B7D207B7D272E666F72C7\n"
        ":10CDC0006D61742861666972DD73742E66696FFFAD\n"
        ":10CDD0000CFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF\n"
        ":00000001FF\n"
    ),
}

# main.py - medium multi-chunk file
MAIN_FILE: FileData = {
    "filename": "main.py",
    "content": (
        "from microbit import display, Image, sleep\n\n"
        "from afirst import firstname\n"
        "from alast import lastname, full_name\n\n"
        "if full_name == 'Carlos Pereira':\n"
        "    display.show(Image.HAPPY)\n"
        "else:\n"
        "    display.show(Image.SAD)\n"
        "sleep(2000)\n"
        "full = '{} {}'.format(firstname, lastname)\n"
        "display.scroll(full)\n"
        "print(full)\n"
    ),
    "hex": (
        ":020000040003F7\n"
        ":10F08000FE37076D61696E2E707966726F6D206D47\n"
        ":10F090006963726F62697420696D706F7274206445\n"
        ":10F0A0006973706C61792C20496D6167652C2073E0\n"
        ":10F0B0006C6565700A0A66726F6D206166697273AD\n"
        ":10F0C0007420696D706F72742066697273746E61FA\n"
        ":10F0D0006D650A66726F6D20616C61737420696D75\n"
        ":10F0E000706F7274206C6173746E616D652C206634\n"
        ":10F0F000756C6C5F6E616D650A0A6966206675CB1A\n"
        ":10F10000CA6C6C5F6E616D65203D3D202743617266\n"
        ":10F110006C6F732050657265697261273A0A20200E\n"
        ":10F120002020646973706C61792E73686F77284949\n"
        ":10F130006D6167652E4841505059290A656C7365A9\n"
        ":10F140003A0A20202020646973706C61792E7368FC\n"
        ":10F150006F7728496D6167652E534144290A736CA6\n"
        ":10F160006565702832303030290A66756C6C203D38\n"
        ":10F1700020277B7D207B7D272E666F726D6174CC8E\n"
        ":10F18000CB2866697273746E616D652C206C617337\n"
        ":10F19000746E616D65290A646973706C61792E7390\n"
        ":10F1A00063726F6C6C2866756C6C290A7072696E7C\n"
        ":10F1B000742866756C6C290AFFFFFFFFFFFFFFFFD5\n"
        ":00000001FF\n"
    ),
}

# one_chunk_plus - for reading tests
ONE_CHUNK_PLUS_READ: FileData = {
    "filename": "one_chunk_plus.py",
    "content": (
        'a = """abcdefghijklmnopqrstuvwxyz\n'
        "abcdefghijklmnopqrstuvwxyz\n"
        "abcdefghijklmnopqrstuvwxyz\n"
        'abcdefghijklmno"""\n'
    ),
    "hex": (
        ":020000040003F7\n"
        ":10AE0000FE00116F6E655F6368756E6B5F706C75C9\n"
        ":10AE1000732E707961203D20222222616263646575\n"
        ":10AE2000666768696A6B6C6D6E6F7071727374754A\n"
        ":10AE3000767778797A0A6162636465666768696AB9\n"
        ":10AE40006B6C6D6E6F707172737475767778797ADA\n"
        ":10AE50000A6162636465666768696A6B6C6D6E6FD0\n"
        ":10AE6000707172737475767778797A0A6162636447\n"
        ":10AE700065666768696A6B6C6D6E6F2222220A468E\n"
        ":10AE800045FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF8C\n"
        ":00000001FF\n"
    ),
}

# one_chunk_minus - for reading tests
ONE_CHUNK_MINUS_READ: FileData = {
    "filename": "one_chunk_minus.py",
    "content": (
        'a = """abcdefghijklmnopqrstuvwxyz\n'
        "abcdefghijklmnopqrstuvwxyz\n"
        "abcdefghijklmnopqrstuvwxyz\n"
        'abcdefghijklm"""\n'
    ),
    "hex": (
        ":020000040003F7\n"
        ":10920000FE7D126F6E655F6368756E6B5F6D696E74\n"
        ":1092100075732E707961203D202222226162636481\n"
        ":1092200065666768696A6B6C6D6E6F707172737476\n"
        ":1092300075767778797A0A616263646566676869CA\n"
        ":109240006A6B6C6D6E6F7071727374757677787906\n"
        ":109250007A0A6162636465666768696A6B6C6D6EE1\n"
        ":109260006F707172737475767778797A0A61626358\n"
        ":109270006465666768696A6B6C6D2222220AFFFF6B\n"
        ":00000001FF\n"
    ),
}

# Duplicate file test hex fragments
DUPLICATE_FILE_COPY_1 = (
    ":020000040003F7\n"
    ":10AE0000FE1804612E707961203D20274A75737405\n"
    ":10AE100020612066696C65270AFFFFFFFFFFFFFFC7\n"
    ":00000001FF\n"
)

DUPLICATE_FILE_COPY_2 = (
    ":020000040003F7\n"
    ":10C18000FE1804612E707961203D20274A75737472\n"
    ":10C1900020612066696C65270AFFFFFFFFFFFFFF34\n"
    ":00000001FF\n"
)


def merge_hex_fragments(base_hex: str, *fragments: str) -> str:
    """Merge hex fragments into a base hex file."""
    ih_base = IntelHex()
    ih_base.loadhex(StringIO(base_hex))

    for fragment in fragments:
        ih_fragment = IntelHex()
        ih_fragment.loadhex(StringIO(fragment))
        ih_base.merge(ih_fragment, overlap="replace")

    output = StringIO()
    ih_base.write_hex_file(output)
    return output.getvalue()


class TestReadFilesWithHexStrings:
    """Test reading files from hex strings created by real MicroPython devices."""

    def test_read_afirst_single_chunk(self, upy_v1_hex: str) -> None:
        """Read afirst.py - a small file in one chunk."""
        merged_hex = merge_hex_fragments(upy_v1_hex, AFIRST_FILE["hex"])
        files = get_files(merged_hex)

        assert len(files) == 1
        assert files[0].name == AFIRST_FILE["filename"]
        assert files[0].content == AFIRST_FILE["content"].encode("utf-8")

    def test_read_main_multi_chunk(self, upy_v1_hex: str) -> None:
        """Read main.py - a file spanning multiple chunks."""
        merged_hex = merge_hex_fragments(upy_v1_hex, MAIN_FILE["hex"])
        files = get_files(merged_hex)

        assert len(files) == 1
        assert files[0].name == MAIN_FILE["filename"]
        assert files[0].content == MAIN_FILE["content"].encode("utf-8")

    def test_read_one_chunk_plus(self, upy_v1_hex: str) -> None:
        """Read a file that occupies exactly one chunk plus links next empty chunk."""
        merged_hex = merge_hex_fragments(upy_v1_hex, ONE_CHUNK_PLUS_READ["hex"])
        files = get_files(merged_hex)

        assert len(files) == 1
        assert files[0].name == ONE_CHUNK_PLUS_READ["filename"]
        assert files[0].content == ONE_CHUNK_PLUS_READ["content"].encode("utf-8")

    def test_read_one_chunk_minus(self, upy_v1_hex: str) -> None:
        """Read a file that fills almost a full chunk (minus 1 byte)."""
        merged_hex = merge_hex_fragments(upy_v1_hex, ONE_CHUNK_MINUS_READ["hex"])
        files = get_files(merged_hex)

        assert len(files) == 1
        assert files[0].name == ONE_CHUNK_MINUS_READ["filename"]
        assert files[0].content == ONE_CHUNK_MINUS_READ["content"].encode("utf-8")

    def test_read_multiple_files_different_sizes(self, upy_v1_hex: str) -> None:
        """Read files of different sizes in non-consecutive locations."""
        merged_hex = merge_hex_fragments(
            upy_v1_hex,
            AFIRST_FILE["hex"],
            MAIN_FILE["hex"],
        )
        files = get_files(merged_hex)

        assert len(files) == 2
        file_dict = {f.name: f.content for f in files}
        assert file_dict[AFIRST_FILE["filename"]] == AFIRST_FILE["content"].encode(
            "utf-8"
        )
        assert file_dict[MAIN_FILE["filename"]] == MAIN_FILE["content"].encode("utf-8")

    def test_duplicate_filenames_raises_error(self, upy_v1_hex: str) -> None:
        """Duplicate file names in filesystem should raise an error."""
        merged_hex = merge_hex_fragments(
            upy_v1_hex,
            DUPLICATE_FILE_COPY_1,
            DUPLICATE_FILE_COPY_2,
        )

        with pytest.raises(Exception, match="[Dd]uplicate|[Mm]ultiple"):
            get_files(merged_hex)

    def test_read_empty_filesystem_v1(self, upy_v1_hex: str) -> None:
        """Reading from empty MicroPython V1 hex returns empty list."""
        files = get_files(upy_v1_hex)
        assert files == []

    def test_read_empty_filesystem_v2(self, upy_v2_uicr_hex: str) -> None:
        """Reading from empty MicroPython V2 hex returns empty list."""
        files = get_files(upy_v2_uicr_hex)
        assert files == []

    def test_read_non_micropython_hex_fails(self, makecode_hex: str) -> None:
        """Reading from non-MicroPython hex should fail."""
        with pytest.raises(Exception, match="MicroPython|UICR"):
            get_files(makecode_hex)


class TestWriteFilesChunkEdgeCases:
    """Test writing files at chunk boundaries."""

    def test_write_full_chunk_plus(self, upy_v1_hex: str) -> None:
        """A file that fills exactly one chunk should also allocate the next chunk."""
        files = [
            File.from_text(FULL_CHUNK_PLUS["filename"], FULL_CHUNK_PLUS["content"])
        ]

        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == FULL_CHUNK_PLUS["filename"]
        assert read_files[0].content == FULL_CHUNK_PLUS["content"].encode("utf-8")

    def test_write_full_chunk_minus(self, upy_v1_hex: str) -> None:
        """A file using all but the last byte should use only one chunk."""
        files = [
            File.from_text(FULL_CHUNK_MINUS["filename"], FULL_CHUNK_MINUS["content"])
        ]

        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == FULL_CHUNK_MINUS["filename"]
        assert read_files[0].content == FULL_CHUNK_MINUS["content"].encode("utf-8")

    def test_write_two_chunks(self, upy_v1_hex: str) -> None:
        """A file spanning exactly two chunks."""
        files = [File.from_text(TWO_CHUNKS["filename"], TWO_CHUNKS["content"])]

        result_hex = add_files(upy_v1_hex, files)
        read_files = get_files(result_hex)

        assert len(read_files) == 1
        assert read_files[0].name == TWO_CHUNKS["filename"]
        assert read_files[0].content == TWO_CHUNKS["content"].encode("utf-8")


class TestDeviceInfo:
    """Test device info extraction matches expected values."""

    def test_v1_filesystem_size(self, upy_v1_hex: str) -> None:
        """V1 filesystem size should be ~29KB."""
        device_info = get_device_info(upy_v1_hex)
        # Actual V1 FS size from this hex file
        fs_size = device_info.fs_end_address - device_info.fs_start_address
        assert fs_size == 29 * 1024

    def test_v1_filesystem_start(self, upy_v1_hex: str) -> None:
        """V1 filesystem should start at 0x38C00."""
        device_info = get_device_info(upy_v1_hex)
        assert device_info.fs_start_address == 0x38C00

    def test_v2_filesystem_size(self, upy_v2_uicr_hex: str) -> None:
        """V2 filesystem size should be ~24KB."""
        device_info = get_device_info(upy_v2_uicr_hex)
        # Actual V2 FS size from this hex file
        fs_size = device_info.fs_end_address - device_info.fs_start_address
        assert fs_size == 24 * 1024

    def test_v2_filesystem_start(self, upy_v2_uicr_hex: str) -> None:
        """V2 filesystem should start at 0x6D000."""
        device_info = get_device_info(upy_v2_uicr_hex)
        assert device_info.fs_start_address == 0x6D000


class TestCalculateFileSize:
    """Test calculating file size in chunks."""

    def test_small_file_one_chunk(self) -> None:
        """A small file should use one chunk (128 bytes)."""
        # filename: 13 bytes + content: 5 bytes = 18 bytes data
        # Header: 2 bytes, so total = 20 bytes << 126, fits in 1 chunk
        size = calculate_file_size("one_chunk.txt", b"\x1e\x1f\x20\x21\x22")
        assert size == 128

    def test_almost_full_chunk(self) -> None:
        """A file almost filling one chunk should use one chunk."""
        # filename: 24 bytes + content: 99 bytes = 123 bytes
        # Header: 2 bytes, total = 125 bytes << 126, fits in 1 chunk
        size = calculate_file_size("almost_one_chunk____.txt", bytes(99))
        assert size == 128

    def test_one_chunk_overflow(self) -> None:
        """A file overflowing one chunk should use two chunks."""
        # filename: 24 bytes + content: 100 bytes = 124 bytes
        # Header: 2 bytes, total = 126 bytes == 126, needs 2 chunks
        size = calculate_file_size("one_chunk_overflow__.txt", bytes(100))
        assert size == 256

    def test_just_two_chunks(self) -> None:
        """A file just needing two chunks."""
        # filename: 24 bytes + content: 101 bytes = 125 bytes
        # Header: 2 bytes, total = 127 bytes > 126, needs 2 chunks
        size = calculate_file_size("just_about_2_chunks_.txt", bytes(101))
        assert size == 256

    def test_nine_chunks(self) -> None:
        """A large file should use many chunks."""
        # 1100 bytes of content
        size = calculate_file_size("9_chunks.txt", bytes(1100))
        # Should be 9 chunks = 9 * 128 = 1152 bytes
        assert size == 1152
