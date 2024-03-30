# -*- coding: UTF-8 -*-
"""
Name: setting_profiles.py
Porpose: profiles storing and profiles editing dialog
Compatibility: Python3, wxPython Phoenix
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
import os
import webbrowser
import wx
from videomass.vdms_utils.presets_manager_utils import write_new_profile
from videomass.vdms_utils.presets_manager_utils import edit_existing_profile


class SettingProfile(wx.Dialog):
    """
    Show dialog to store and edit profiles of a selected preset.

    """
    PASS_1 = _("One-Pass, Do not start with `ffmpeg "
               "-i filename`; do not end with "
               "`output-filename`"
               )
    PASS_2 = _("Two-Pass (optional), Do not start with "
               "`ffmpeg -i filename`; do not end with "
               "`output-filename`"
               )
    SUPFORMAT = _("Supported Formats list (optional). Do not include the `.`")
    OUTFORMAT = _("Output Format. Empty to copy format and codec. "
                  "Do not include the `.`")
    # ------------------------------------------------------------------

    def __init__(self, parent, arg, filename, array, title):
        """
        arg: evaluate if this dialog is used for add new profile or
             edit a existing profiles from three message strings:
        arg = 'newprofile'  from preset manager
        arg = 'edit' from preset manager
        arg = 'addprofile' from video and audio conversions

        """
        get = wx.GetApp()
        self.appdata = get.appset
        self.path_prst = os.path.join(self.appdata['confdir'], 'presets',
                                      f'{filename}.json')
        self.arg = arg  # evaluate if 'edit', 'newprofile', 'addprofile'
        self.array = array  # param list [name,descript,cmd1,cmd2,supp,ext,..]

        wx.Dialog.__init__(self, parent, -1, title,
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        size_base = wx.BoxSizer(wx.VERTICAL)
        size_namedescr = wx.BoxSizer(wx.HORIZONTAL)
        size_base.Add(size_namedescr, 0, wx.ALL | wx.EXPAND, 0)
        box_name = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY,
                                                  _("Profile Name")),
                                     wx.VERTICAL)
        size_namedescr.Add(box_name, 1, wx.ALL | wx.EXPAND, 5)
        self.txt_name = wx.TextCtrl(self, wx.ID_ANY, "")
        box_name.Add(self.txt_name, 0, wx.ALL | wx.EXPAND, 5)
        box_descr = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY,
                                                   _("Description")),
                                      wx.VERTICAL
                                      )
        size_namedescr.Add(box_descr, 1, wx.ALL | wx.EXPAND, 5)
        self.txt_descript = wx.TextCtrl(self, wx.ID_ANY, "")
        box_descr.Add(self.txt_descript, 0, wx.ALL | wx.EXPAND, 5)
        box_pass1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY,
                                                   SettingProfile.PASS_1),
                                      wx.VERTICAL
                                      )
        size_base.Add(box_pass1, 1, wx.ALL | wx.EXPAND, 5)
        self.pass_1_cmd = wx.TextCtrl(self, wx.ID_ANY, "",
                                      style=wx.TE_MULTILINE
                                      )
        box_pass1.Add(self.pass_1_cmd, 1, wx.ALL | wx.EXPAND, 5)
        self.pass_1_pre = wx.TextCtrl(self, wx.ID_ANY, "")
        box_pass1.Add(self.pass_1_pre, 0, wx.ALL | wx.EXPAND, 5)
        box_pass2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY,
                                                   SettingProfile.PASS_2),
                                      wx.VERTICAL
                                      )
        size_base.Add(box_pass2, 1, wx.ALL | wx.EXPAND, 5)
        self.pass_2_cmd = wx.TextCtrl(self, wx.ID_ANY, "",
                                      style=wx.TE_MULTILINE
                                      )
        box_pass2.Add(self.pass_2_cmd, 1, wx.ALL | wx.EXPAND, 5)
        self.pass_2_pre = wx.TextCtrl(self, wx.ID_ANY, "")
        box_pass2.Add(self.pass_2_pre, 0, wx.ALL | wx.EXPAND, 5)
        size_formats = wx.BoxSizer(wx.HORIZONTAL)
        size_base.Add(size_formats, 0, wx.ALL | wx.EXPAND, 0)
        box_supp = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY,
                                                  SettingProfile.SUPFORMAT),
                                     wx.VERTICAL
                                     )
        size_formats.Add(box_supp, 1, wx.ALL | wx.EXPAND, 5)

        self.txt_supp = wx.TextCtrl(self, wx.ID_ANY, "")
        box_supp.Add(self.txt_supp, 0, wx.ALL | wx.EXPAND, 5)
        box_format = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY,
                                                    SettingProfile.OUTFORMAT),
                                       wx.VERTICAL
                                       )
        size_formats.Add(box_format, 1, wx.ALL | wx.EXPAND, 5)

        self.txt_ext = wx.TextCtrl(self, wx.ID_ANY, "")
        box_format.Add(self.txt_ext, 0, wx.ALL | wx.EXPAND, 5)
        # ----- confirm buttons section
        grdBtn = wx.GridSizer(1, 2, 0, 0)
        grdhelp = wx.GridSizer(1, 1, 0, 0)
        btn_help = wx.Button(self, wx.ID_HELP, "")
        grdhelp.Add(btn_help, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        grdBtn.Add(grdhelp)
        grdexit = wx.BoxSizer(wx.HORIZONTAL)
        btn_canc = wx.Button(self, wx.ID_CANCEL, "")
        grdexit.Add(btn_canc, 0, wx.ALIGN_CENTER_VERTICAL)
        btn_save = wx.Button(self, wx.ID_OK)
        grdexit.Add(btn_save, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
        grdBtn.Add(grdexit, 0, wx.ALL | wx.ALIGN_RIGHT | wx.RIGHT, border=5)
        size_base.Add(grdBtn, 0, wx.EXPAND)

        # ----- set_properties:
        if self.appdata['ostype'] == 'Darwin':
            self.pass_1_cmd.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE,
                                            wx.NORMAL, wx.NORMAL))
            self.pass_2_cmd.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE,
                                            wx.NORMAL, wx.NORMAL))
            self.pass_1_pre.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE,
                                            wx.NORMAL, wx.NORMAL))
            self.pass_2_pre.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE,
                                            wx.NORMAL, wx.NORMAL))
        else:
            self.pass_1_cmd.SetFont(wx.Font(8, wx.FONTFAMILY_TELETYPE,
                                            wx.NORMAL, wx.NORMAL))
            self.pass_2_cmd.SetFont(wx.Font(8, wx.FONTFAMILY_TELETYPE,
                                            wx.NORMAL, wx.NORMAL))
            self.pass_1_pre.SetFont(wx.Font(8, wx.FONTFAMILY_TELETYPE,
                                            wx.NORMAL, wx.NORMAL))
            self.pass_2_pre.SetFont(wx.Font(8, wx.FONTFAMILY_TELETYPE,
                                            wx.NORMAL, wx.NORMAL))

        self.txt_name.SetToolTip(_('A short profile name'))
        self.txt_descript.SetToolTip(_('A long description of the profile'))
        self.pass_1_cmd.SetToolTip(_('FFmpeg arguments for one-pass encoding'))
        self.pass_2_cmd.SetToolTip(_('FFmpeg arguments for two-pass encoding'))
        self.txt_supp.SetToolTip(_('One or more comma-separated format names '
                                   'that are not compatible with this '
                                   'profile.'))
        self.txt_ext.SetToolTip(_('Output format extension. Leave empty to '
                                  'copy codec and format'))

        tip = (_('Any optional arguments to add before input file on the '
                 'two-pass encoding, e.g required names of some hardware '
                 'accelerations like -hwaccel to use with CUDA.'))
        self.pass_1_pre.SetToolTip(tip)
        tip = (_('Any optional arguments to add before input file on the '
                 'two-pass encoding, e.g required names of some hardware '
                 'accelerations like -hwaccel to use with CUDA.'))
        self.pass_2_pre.SetToolTip(tip)
        # ------ Set Layout
        self.SetMinSize((950, 550))
        self.SetSizer(size_base)
        self.Fit()
        self.Layout()

        # ----------------------Binder (EVT)----------------------#
        self.Bind(wx.EVT_TEXT, self.on_Name, self.txt_name)
        self.Bind(wx.EVT_TEXT, self.on_Descript, self.txt_descript)
        self.Bind(wx.EVT_TEXT, self.on_Pass1, self.pass_1_cmd)
        self.Bind(wx.EVT_BUTTON, self.on_close, btn_canc)
        self.Bind(wx.EVT_BUTTON, self.on_help, btn_help)
        self.Bind(wx.EVT_BUTTON, self.on_apply, btn_save)

        # -------------------Binder (EVT) End --------------------#
        if arg == 'edit':
            self.array[5] = '' if array[5] == 'copy' else array[5]
            self.change()
        elif arg == 'addprofile':
            self.pass_1_cmd.AppendText(self.array[0])  # command or param
            self.pass_2_cmd.AppendText(self.array[1])
            self.txt_ext.AppendText(self.array[2])  # extension

    def change(self):
        """
        In edit mode only, paste the array items on text boxes

        """
        self.txt_name.AppendText(self.array[0])  # name
        self.txt_descript.AppendText(self.array[1])  # descript
        self.pass_1_cmd.AppendText(self.array[2])  # command 1
        self.pass_2_cmd.AppendText(self.array[3])  # command 2
        self.txt_supp.AppendText(self.array[4])  # file supportted
        self.txt_ext.AppendText(self.array[5])  # extension
        self.pass_1_pre.AppendText(self.array[6])  # input 1
        self.pass_2_pre.AppendText(self.array[7])  # input 2
    # ---------------------Callbacks (event handler)----------------------#

    def on_Name(self, event):
        """Set default background"""
        if self.txt_name.GetBackgroundColour() == (152, 131, 19, 255):
            # html: ('#988313') == rgb: (152, 131, 19, 255) =
            self.txt_name.SetBackgroundColour(wx.NullColour)
    # ------------------------------------------------------------------#

    def on_Descript(self, event):
        """Set default background"""
        if self.txt_descript.GetBackgroundColour() == (152, 131, 19, 255):
            # html: ('#988313') == rgb: (152, 131, 19, 255) =
            self.txt_descript.SetBackgroundColour(wx.NullColour)
    # ------------------------------------------------------------------#

    def on_Pass1(self, event):
        """Set default background"""
        if self.pass_1_cmd.GetBackgroundColour() == (152, 131, 19, 255):
            # html: ('#988313') == rgb: (152, 131, 19, 255) =
            self.pass_1_cmd.SetBackgroundColour(wx.NullColour)
    # ------------------------------------------------------------------#

    def on_help(self, event):
        """
        Open default web browser via Python Web-browser controller.
        see <https://docs.python.org/3.8/library/webbrowser.html>
        """
        if self.appdata['GETLANG'] in self.appdata['SUPP_LANGs']:
            lang = self.appdata['GETLANG'].split('_')[0]
            page = (f'https://jeanslack.github.io/Videomass/Pages/User-guide-'
                    f'languages/{lang}/3-Presets_Manager_{lang}.pdf')
        else:
            page = ('https://jeanslack.github.io/Videomass/Pages/User-guide-'
                    'languages/en/3-Presets_Manager_en.pdf')

        webbrowser.open(page)
    # ------------------------------------------------------------------#

    def on_close(self, event):
        """
        Close this dialog without saving anything
        """
        event.Skip()
    # ------------------------------------------------------------------#

    def on_apply(self, event):
        """
        Apply changes
        """
        name = self.txt_name.GetValue()
        descript = self.txt_descript.GetValue()
        pass_1 = self.pass_1_cmd.GetValue()
        pass_2 = self.pass_2_cmd.GetValue()
        file_support = self.txt_supp.GetValue().strip()
        extens = self.txt_ext.GetValue().strip()
        extens = 'copy' if not extens else extens
        preinput1 = self.pass_1_pre.GetValue()
        preinput2 = self.pass_2_pre.GetValue()

        # ---------------------------------------------------------------
        if [txt for txt in [name, descript, pass_1] if txt.strip() == '']:
            if not name.strip():
                self.txt_name.SetBackgroundColour('#988313')
            if not descript.strip():
                self.txt_descript.SetBackgroundColour('#988313')
            if not pass_1.strip():
                self.pass_1_cmd.SetBackgroundColour('#988313')

            wx.MessageBox(_("Incomplete profile assignments"),
                          "Videomass ", wx.ICON_WARNING, self)
            return

        if len(file_support.split()) > 1:
            supp = ''.join(file_support.split())
            if [i for i in supp.split() if ',' not in i]:
                wx.MessageBox(_("Formats must be comma-separated"),
                              "Videomass ", wx.ICON_WARNING, self)
                return

        if self.arg in ('newprofile', 'addprofile'):
            writenewprf = write_new_profile(self.path_prst,
                                            Name=name.strip(),
                                            Description=descript,
                                            First_pass=pass_1,
                                            Second_pass=pass_2,
                                            Supported_list=file_support,
                                            Output_extension=extens,
                                            Preinput_1=preinput1,
                                            Preinput_2=preinput2,
                                            )
            if writenewprf == 'already exist':
                wx.MessageBox(_("Profile already stored with same name"),
                              "Videomass", wx.ICON_WARNING, self)
                return

            wx.MessageBox(_("Successful storing!"))

        elif self.arg == 'edit':
            editprf = edit_existing_profile(self.path_prst,
                                            self.array[0],
                                            Name=name.strip(),
                                            Description=descript,
                                            First_pass=pass_1,
                                            Second_pass=pass_2,
                                            Supported_list=file_support,
                                            Output_extension=extens,
                                            Preinput_1=preinput1,
                                            Preinput_2=preinput2,
                                            )
            if editprf == 'already exist':
                wx.MessageBox(_("Profile already stored with same name"),
                              "Videomass", wx.ICON_WARNING, self)
                return
            wx.MessageBox(_("Successful changes!"))
            # self.Destroy() # con ID_OK e ID_CANCEL non serve

        event.Skip()
