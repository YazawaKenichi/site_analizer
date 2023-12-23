#!/usr/bin/env python3
# coding : utf-8
# main.py

import os
import sys

import FDEditor as fde
import PDFEditor as pdfe
import PathEditor as pe

from optparse import OptionParser
from PrintMaster import Printer
from URLMaster import URL

from bestchai import Bestchai
from buhidoh import Buhidoh
from erodoujinshi_world import ErodoujinshiWorld
from eromanga_milf import EromangaMilfs
from eromanga_sora import EromangaSoras
from eromangaselect import EromangaSelect
from mangalear import Mangalear
from shikotch import Shikotch
from moeero_library import MoeeroLibrary
from momon_ga import MomonGa
from eromanga_celeb import EromangaCeleb
from eromanga_life import EromangaLife
from eromanga_platinum import EromangaPlatinum
from nuki_dokoro import NukiDokoro
from doujin_dolci import DoujinDolci
from krov23 import Krov23
from dojinwatch import DojinWatch

class Manga2PDF:
    def __init__(self):
        optiondict, args = self.get_args()
        self.download_dir = optiondict.dir
        self.listpath = optiondict.list
        self.skip = optiondict.skip
        self.skipped_url_file = optiondict.skipped_url_path
        self.log = optiondict.log
        self.detail = optiondict.detail
        self.ui = optiondict.visible or detail
        self.delay = optiondict.delay
        self.delete = optiondict.delete
        self.addresses = fde.file2list(self.listpath, args)

        self.printer = Printer()
        config = {"name" : "MAIN", "screen-full" : True}
        self.printer.setConfig(config)

    def get_args(self):
        usage = "%prog"
        parser = OptionParser(usage = usage)

        parser.add_option(
                "-v",
                action = "store_true",
                default = False,
                dest = "visible",
                help = "デバッグモード"
                )
        parser.add_option(
                "-l", "--list",
                default = "./url",
                type = "string",
                dest = "list",
                help = "URL のリストを記述したファイル"
                )
        parser.add_option(
                "--dir",
                default = "./downloads",
                type = "string",
                dest = "dir",
                help = "ダウンロード先ディレクトリ"
                )
        parser.add_option(
                "-s", "--skip",
                action = "store_true",
                default = False,
                dest = "skip",
                help = "すでにパスが存在する場合はスキップ"
                )
        parser.add_option(
                "--delete",
                action = "store_true",
                default = False,
                dest = "delete",
                help = "ダウンロードが完了したら URL のリストから URL を削除"
                )
        parser.add_option(
                "--skipped-log",
                default = "./skipped-log",
                type = "string",
                dest = "skipped_url_path",
                help = "スキップされた URL のリスト"
                )
        parser.add_option(
                "--log",
                default = "./log",
                type = "string",
                dest = "log",
                help = "ダウンロードが完了した URL のリスト"
                )
        parser.add_option(
                "--detail",
                action = "store_true",
                default = False,
                dest = "detail",
                help = "処理の詳細を表示"
                )
        parser.add_option(
                "--delay",
                default = 5,
                type = "int",
                dest = "delay",
                help = "画像をダウンロードする時間間隔"
                )
        return parser.parse_args()

    def discrimination(self, a, ui = False):
        s = URL(a).fqdn
        r = None
        if "buhidoh" in s:
            r = Buhidoh(a, ui = ui)
        if "bestchai" in s:
            r = Bestchai(a, ui = ui)
        if "erodoujinshi-world" in s:
            r = ErodoujinshiWorld(a, ui = ui)
        if "eromanga-milf" in s:
            r = EromangaMilfs(a, ui = ui)
        if "eromanga-sora" in s:
            r = EromangaSoras(a, ui = ui)
        if "eromanga-select" in s:
            r = EromangaSelect(a, ui = ui)
        if "mangalear" in s:
            r = Mangalear(a, ui = ui)
        if "shikotch" in s:
            r = Shikotch(a, ui = ui)
        if "moeero-library" in s:
            r = MoeeroLibrary(a, ui = ui)
        if "momon-ga" in s:
            r = MomonGa(a, ui = ui)
        if "eromanga-celeb" in s:
            r = EromangaCeleb(a, ui = ui)
        if "eromanga-life" in s:
            r = EromangaLife(a, ui = ui)
        if "ero-manga-platinum" in s:
            r = EromangaPlatinum(a, ui = ui)
        if "nuki-dokoro" in s:
            r = NukiDokoro(a, ui = ui)
        if "doujin-dolci" in s:
            r = DoujinDolci(a, ui = ui)
        if "krov23" in s:
            r = Krov23(a, ui = ui)
        if "dojinwatch" in s:
            r = DojinWatch(a, ui = ui)
        if r is None:
            self.printer.print("[Error] Undefined Web Site")
        return r
    
    def generatePDF(self, path, srcs, address):
        error = False
        if not (fde.check_string_in_file(self.log, address) and os.path.exists(path) and self.skip):
            try:
                pdfe.imgurllist2pdf(srcs, path)
            except OSError:
                error = True
        return error

    def main(self):
        for address_index, address in enumerate(self.addresses):
            errored = False
            if not "end" in address.lower():
                self.printer.print("Next ...")
                self.printer.print(f"[Address] {address}")
                manga = self.discrimination(address, ui = self.detail)
                if not manga is None:
                    if not manga.notfound:
                        self.printer.print(f"[Title] {manga.title}")
                        title = pe.path_short(manga.title)
                        site = pe.path_short(manga.sitename)
                        category = pe.path_short(manga.category)
                        subdir = os.path.join(f"{self.download_dir}", f"{site}", f"{category}")
                        fde.mkdir(subdir)
                        path = os.path.join(f"{subdir}", f"{title}.pdf")
                        errored = self.generatePDF(path, manga.srcs, address)
                        if not errored:
                            if self.ui:
                                self.printer.print(f"[Address] {address}")
                                self.printer.print(f"[  Path ] {path}")
                            rensaku = []
                            try:
                                rensaku = manga.rensaku
                            except:
                                rensaku = [address]
                            for add in rensaku:
                                fde.add_file_end(self.log, add, duplicate = False)
                    else:
                        self.printer.print("[Error] NotFound")
                else:
                    self.printer.print("[Error] Undefined Site", file = sys.stderr)
            if errored:
                fde.add_file_end(self.skipped_url_file, address, duplicate = False)
            if self.delete:
                fde.delinefromfile(self.listpath, address)
            if "end" in address.lower():
                return

