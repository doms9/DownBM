#!/usr/bin/env python3

import json
import re
import shutil
import sys
from pathlib import Path
from tkinter import messagebox
from typing import Any

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from remotezip import RemoteZip


class Ui_MainWindow(object):
    def setupUi(self, MainWindow) -> None:
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 700))
        MainWindow.setMaximumSize(QtCore.QSize(1000, 700))
        if Path("./icon.ico").is_file():
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap("./icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off
            )
            MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.apple_firmware_entrybox = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.apple_firmware_entrybox.setGeometry(QtCore.QRect(260, 80, 471, 141))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.apple_firmware_entrybox.setFont(font)
        self.apple_firmware_entrybox.setObjectName("apple_firmware_entrybox")
        self.enterAppleURL_label = QtWidgets.QLabel(self.centralwidget)
        self.enterAppleURL_label.setGeometry(QtCore.QRect(265, 20, 471, 71))
        font = QtGui.QFont()
        font.setFamily("Archivo")
        font.setPointSize(16)
        self.enterAppleURL_label.setFont(font)
        self.enterAppleURL_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.enterAppleURL_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.enterAppleURL_label.setLineWidth(1)
        self.enterAppleURL_label.setAlignment(QtCore.Qt.AlignCenter)
        self.enterAppleURL_label.setObjectName("enterAppleURL_label")
        self.enterappledevice_label = QtWidgets.QLabel(self.centralwidget)
        self.enterappledevice_label.setGeometry(QtCore.QRect(285, 270, 431, 41))
        font = QtGui.QFont()
        font.setFamily("Archivo")
        font.setPointSize(14)
        self.enterappledevice_label.setFont(font)
        self.enterappledevice_label.setAlignment(QtCore.Qt.AlignCenter)
        self.enterappledevice_label.setObjectName("enterappledevice_label")
        self.iPhone_listbox = QtWidgets.QListWidget(self.centralwidget)
        self.iPhone_listbox.setGeometry(QtCore.QRect(270, 310, 451, 181))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.iPhone_listbox.setFont(font)
        self.iPhone_listbox.setObjectName("iPhone_listbox")
        self.DownloadBM_btn = QtWidgets.QPushButton(
            self.centralwidget, clicked=lambda: self.download_manifest()
        )
        self.DownloadBM_btn.setGeometry(QtCore.QRect(230, 550, 261, 101))
        self.DownloadBM_btn.setObjectName("DownloadBM_btn")
        self.ChangePath_btn = QtWidgets.QPushButton(self.centralwidget)
        self.ChangePath_btn.setGeometry(QtCore.QRect(510, 550, 261, 101))
        self.ChangePath_btn.setObjectName("ChangePath_btn")
        self.ChangePath_btn.clicked.connect(pick_new)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Put devices into listbox
        self.iPhone_listbox.addItems([*get_names()])

    def device_id(self) -> Any | None:
        with devices_json_file.open(encoding="utf-8") as f:
            data = json.load(f)
        for dev in data["devices"]:
            if self.iPhone_listbox.currentItem().text().lower() == dev["name"].lower():
                return dev["identifier"]

        return None

    def build_id(self, identifier: str) -> Any | None:
        with devices_json_file.open(encoding="utf8") as f1:
            data_1 = json.load(f1)

        for dev1 in data_1["devices"]:
            if identifier == dev1["identifier"]:
                return dev1["board"]

    def download_manifest(self) -> None:
        firmwares = self.apple_firmware_entrybox.toPlainText().strip().split("|")

        model = self.device_id()

        if self.iPhone_listbox.currentItem().text() == "":
            messagebox.showerror("Error", "Please select an Apple device")

        elif model is None:
            messagebox.showerror("Error", "Please select a valid Apple device")

        elif not download_path().is_dir():
            messagebox.showerror(
                "Error", f'"{download_path()}" is not a valid directory'
            )

        else:
            for firmware in firmwares:
                while firmware != "":
                    try:
                        ipsw_id = firmware.split("_")

                        if len(ipsw_id) == 4:
                            ios_version, ios_build_id = ipsw_id[1], ipsw_id[2]
                        elif (
                            (
                                int(re.sub(r"[^\d]*|\d*$", "", model)) < 7
                                and len(ipsw_id) > 5
                            )
                            or ("P3" == ipsw_id[2])
                            or (len(ipsw_id) == 6)
                        ):
                            ios_version, ios_build_id = ipsw_id[3], ipsw_id[4]
                        else:
                            ios_version, ios_build_id = ipsw_id[2], ipsw_id[3]

                    except Exception:
                        messagebox.showerror(
                            "Error", "The given url is not a valid Apple firmware."
                        )
                        break

                    bm_link = f"{re.sub(r'[^/]*$', '', firmware)}BuildManifest.plist"

                    bm = requests.get(bm_link, timeout=10)

                    if bm.status_code == 200:

                        (download_path() / f"{model}").mkdir(exist_ok=True)

                        (
                            download_path()
                            / f"{model}/{ios_version}-{ios_build_id}-{self.build_id(model)}.plist"
                        ).write_bytes(bm.content)

                        messagebox.showinfo(
                            "Success",
                            f"Downloaded {ios_version}-{ios_build_id}-{self.build_id(model)}.plist",
                        )

                    else:
                        with RemoteZip(firmware) as ipsw_zip:
                            ipsw_zip.extract("BuildManifest.plist")

                        (download_path() / f"{model}").mkdir(exist_ok=True)

                        shutil.move(
                            "./BuildManifest.plist",
                            download_path()
                            / f"{model}/{ios_version}-{ios_build_id}-{self.build_id(model)}.plist",
                        )

                        messagebox.showinfo(
                            "Success",
                            f"Downloaded {ios_version}-{ios_build_id}-{self.build_id(model)}.plist",
                        )

                    break

                else:
                    if len(firmwares) == 1:
                        messagebox.showerror(
                            "Error", "Please enter an Apple firmware URL"
                        )
                        break

    def retranslateUi(self, MainWindow) -> None:
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DownBM"))

        self.enterAppleURL_label.setText(
            _translate("MainWindow", "Enter Apple Firmware URL(s)")
        )
        self.enterappledevice_label.setText(
            _translate("MainWindow", "Select an Apple Device")
        )
        self.DownloadBM_btn.setText(
            _translate("MainWindow", "Download BuildManifest(s)")
        )
        self.ChangePath_btn.setText(_translate("MainWindow", "Change Download Path"))


def download_devices_file() -> None:
    api = requests.get("https://api.ipsw.me/v4/devices", timeout=10)

    device_info = {}

    devices = api.json()

    with devices_json_file.open("w", encoding="utf-8") as a:
        json.dump({"devices": []}, a, indent=2)

    for x in devices:
        model_type = re.sub(r"[^\w]|\d*", "", x["identifier"]).lower()
        if model_type in ("ipod", "iphone", "ipad", "appletv"):
            device_info["name"] = (
                x["name"].replace("generation", "gen.").replace("+", " Plus")
            )
            device_info["identifier"] = x["identifier"]
            device_info["board"] = x["boardconfig"].lower()

        with devices_json_file.open(encoding="utf-8") as b:
            data = json.load(b)
            data["devices"].append(device_info)

        with devices_json_file.open("w", encoding="utf-8") as c:
            json.dump(data, c, indent=2)


def get_names() -> list:
    devices = set()

    with devices_json_file.open(encoding="utf-8") as f:
        data = json.load(f)

        for device in data["devices"]:
            devices.add(device["name"])

    return sorted(devices, reverse=True)


def pick_new() -> None:
    global folder_path
    dialog = QtWidgets.QFileDialog()
    folder_path = dialog.getExistingDirectory(None, "Select Directory")
    folder_path = Path(folder_path).resolve()


def download_path() -> Path | str:
    return folder_path


if __name__ == "__main__":
    devices_json_file = Path("./devices.json").resolve()

    if not devices_json_file.is_file():
        download_devices_file()

    folder_path = Path.cwd()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    raise SystemExit(app.exec_())
