# -*- coding: UTF-8 -*-
"""
Name: pictures_exporting.py
Porpose: FFmpeg long processing task on save as pictures
Compatibility: Python3, wxPython4 Phoenix (OS Unix-like only)
Author: Gianluca Pernigotto <jeanlucperni@gmail.com>
Copyleft - 2024 Gianluca Pernigotto <jeanlucperni@gmail.com>
license: GPL3
Rev: Mar.08.2024
Code checker: flake8, pylint

This file is part of Videomass.

   Videomass is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   Videomass is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with Videomass.  If not, see <http://www.gnu.org/licenses/>.
"""
from threading import Thread
import time
import subprocess
import platform
import wx
from pubsub import pub
from videomass.vdms_utils.utils import Popen
from videomass.vdms_io.make_filelog import logwrite
if not platform.system() == 'Windows':
    import shlex


class PicturesFromVideo(Thread):
    """
    This class represents a separate thread for running simple
    single processes to save video sequences as pictures.

    NOTE capturing output in real-time (Windows, Unix):

    https://stackoverflow.com/questions/1388753/how-to-get-output-
    from-subprocess-popen-proc-stdout-readline-blocks-no-dat?rq=1
    """
    get = wx.GetApp()  # get videomass wx.App attribute
    appdata = get.appset
    NOT_EXIST_MSG = _("Is 'ffmpeg' installed on your system?")
    # ------------------------------------------------------

    def __init__(self, *args, **kwargs):
        """
        Called from `long_processing_task.topic_thread`.
        Also see `main_frame.switch_to_processing`.

        """
        self.stop_work_thread = False  # process terminate
        self.fname = kwargs['filename']
        self.outputdir = kwargs['outputdir']  # output directory
        self.cmd = kwargs['args']  # comand set on single pass
        self.duration = kwargs['duration'][0]  # duration list
        self.count = 0  # count first for loop
        self.logfile = args[0]  # log filename
        self.kwa = kwargs

        Thread.__init__(self)
        self.start()  # self.run()

    def run(self):
        """
        Subprocess initialize thread.
        """
        filedone = []
        cmd = (f'"{PicturesFromVideo.appdata["ffmpeg_cmd"]}" '
               f'{self.kwa["start-time"]} '
               f'{self.kwa["end-time"]} '
               f'{PicturesFromVideo.appdata["ffmpeg_default_args"]} '
               f'{self.kwa["pre-input-1"]} '
               f'-i "{self.kwa["filename"]}" '
               f'{self.cmd}'
               )
        count1 = (f'File 1/1\nSource: "{self.fname}"\n'
                  f'Destination: "{self.outputdir}"')
        com = f'{count1}\n\n[COMMAND]:\n{cmd}'

        wx.CallAfter(pub.sendMessage,
                     "COUNT_EVT",
                     count=count1,
                     duration=self.duration,
                     end='',
                     )
        logwrite(com, '', self.logfile)  # write n/n + command only

        if not PicturesFromVideo.appdata['ostype'] == 'Windows':
            cmd = shlex.split(cmd)
        try:
            with Popen(cmd,
                       stderr=subprocess.PIPE,
                       bufsize=1,
                       universal_newlines=True,
                       encoding='utf8',
                       ) as proc:
                for line in proc.stderr:
                    wx.CallAfter(pub.sendMessage,
                                 "UPDATE_EVT",
                                 output=line,
                                 duration=self.duration,
                                 status=0,
                                 )
                    if self.stop_work_thread:  # break second 'for' loop
                        proc.terminate()
                        break

                if proc.wait():  # error
                    wx.CallAfter(pub.sendMessage,
                                 "UPDATE_EVT",
                                 output='',
                                 duration=self.duration,
                                 status=proc.wait(),
                                 )
                    logwrite('',
                             f"Exit status: {proc.wait()}",
                             self.logfile,
                             )  # append exit error number

                else:  # status ok
                    filedone.append(self.fname)
                    wx.CallAfter(pub.sendMessage,
                                 "COUNT_EVT",
                                 count='',
                                 duration='',
                                 end='Done'
                                 )
        except (OSError, FileNotFoundError) as err:
            excepterr = f"{err}\n  {PicturesFromVideo.NOT_EXIST_MSG}"
            wx.CallAfter(pub.sendMessage,
                         "COUNT_EVT",
                         count=excepterr,
                         duration=0,
                         end='error',
                         )
        time.sleep(.5)
        wx.CallAfter(pub.sendMessage, "END_EVT", filetotrash=filedone)
    # --------------------------------------------------------------------#

    def stop(self):
        """
        Sets the stop work thread to terminate the process
        """
        self.stop_work_thread = True
