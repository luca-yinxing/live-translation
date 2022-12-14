# Copyright (C) 2021 Luca Gasperini <luca.gasperini@xsoftware.it>
#
# This file is part of Live Translation.
#
# Live Translation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Live Translation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Live Translation.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import enum
import os
import threading

import wave

import config

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication

# NOTE: No more used, debug purpose


def pcm2wav(data, outputfile, channels=1, depth=2, rate=16000):
    with wave.open(outputfile, 'wb') as wavfile:
        wavfile.setparams((channels, depth, rate, 0, 'NONE', 'NONE'))
        wavfile.writeframesraw(data)


class log_code(enum.Enum):
    DEBUG = 0
    LOG = 1
    INFO = 2
    ERROR = 3


def print_log_file(text, code, file):

    if os.path.exists(file):
        if os.path.getsize(file) > config.log_size:
            stream = open(file, "w", encoding="utf-8")
        else:
            stream = open(file, "a", encoding="utf-8")
    else:
        stream = open(file, "w", encoding="utf-8")

    if config.log_thread_name == True:
        msg = "{" + threading.current_thread().name + "} " + text

    msg = "[" + code.name + "] " + msg
    msg = "[" + str(datetime.datetime.now()) + "]" + msg

    stream.write(msg + "\n")
    stream.close()


def print_log(text, code=log_code.LOG, verbose=False, file=""):
    if code.value >= log_code[config.log_level].value:
        msg = "[" + code.name + "] " + text
    else:
        return

    if config.log_stdout_time:
        msg = "[" + str(datetime.datetime.now()) + "]" + msg

    if verbose == True or config.verbose == True:
        print(msg)

    if file == "" and config.log_file != "":
        file = config.log_file

    if file != "":
        print_log_file(text, code, file)


class error_reporting:
    def __init__(self, text, id=None, critical=False):
        self.text = text
        self.id = id
        self.critical = critical

    def show(self, title="", parent=None):
        show_critical_error(title, self.text, parent)


def print_err(text="", qsignal=None, id=None, critical=False, file=""):
    if qsignal != None:
        qsignal.emit(error_reporting(text, id, critical))

    if id:
        text = f"({id}) {text}"

    print_log(text, log_code.ERROR, True, file)


def show_critical_error(title="", text="", parent=None):
    QMessageBox.critical(parent,
                         QApplication.translate(config.APP_I18N, title),
                         QApplication.translate(config.APP_I18N, text),
                         QMessageBox.StandardButton.Ok)
