#/********************************************************************
# libonvif/onvif-gui/gui/onvif/videotab.py 
#
# Copyright (c) 2023  Stephen Rhodes
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#*********************************************************************/

from PyQt6.QtWidgets import QComboBox, QLineEdit, QSpinBox, \
    QGridLayout, QWidget, QLabel, QCheckBox, QPushButton
from PyQt6.QtCore import Qt
from loguru import logger

class SpinBox(QSpinBox):
    def __init__(self, qle):
        super().__init__()
        self.setLineEdit(qle)

class VideoTab(QWidget):
    def __init__(self, cp):
        super().__init__()
        self.cp = cp
        self.videoChanged = False
        self.audioChanged = False

        self.cmbProfiles = QComboBox()
        self.cmbProfiles.currentIndexChanged.connect(self.cmbProfilesChanged)
        self.cmbProfiles.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lblProfiles = QLabel("Profile")

        self.cmbResolutions = QComboBox()
        self.cmbResolutions.currentTextChanged.connect(self.cp.onEdit)
        self.cmbResolutions.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lblResolutions = QLabel("W x H")

        self.chkDisableAudio = QCheckBox("No Audio")
        self.chkDisableAudio.clicked.connect(self.chkDisableAudioChanged)
        self.chkDisableAudio.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.chkAnalyzeVideo = QCheckBox("Video Alarm")
        self.chkAnalyzeVideo.clicked.connect(self.chkAnalyzeVideoChecked)
        self.chkAnalyzeVideo.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.chkAnalyzeAudio = QCheckBox("Audio Alarm")
        self.chkAnalyzeAudio.clicked.connect(self.chkAnalyzeAudioChecked)
        self.chkAnalyzeAudio.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        txtFrameRate = QLineEdit()
        self.spnFrameRate = SpinBox(txtFrameRate)
        self.spnFrameRate.textChanged.connect(self.cp.onEdit)
        self.lblFrameRate = QLabel("FPS")

        txtGovLength = QLineEdit()
        self.spnGovLength = SpinBox(txtGovLength)
        self.spnGovLength.textChanged.connect(self.cp.onEdit)
        self.lblGovLength = QLabel("GOP")

        txtBitrate = QLineEdit()
        self.spnBitrate = SpinBox(txtBitrate)
        self.spnBitrate.textChanged.connect(self.cp.onEdit)
        self.lblBitrate = QLabel("Bitrate")

        self.lblCacheSize = QLabel("Cache:")
        self.btnClearCache = QPushButton("Clear")
        self.btnClearCache.clicked.connect(self.btnClearCacheClicked)
        self.btnClearCache.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.cmbAspect = QComboBox()
        self.cmbAspect.addItems(["16 : 9", "4 : 3", "11 : 9", "3 : 2", "5 : 4", "22 : 15", "UNKN"])
        self.cmbAspect.setCurrentText("UNKN")
        self.cmbAspect.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.cmbAspect.currentTextChanged.connect(self.cmbAspectChanged)
        self.lblAspect = QLabel("Aspect  ")

        self.cmbAudio = QComboBox()
        self.cmbAudio.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.cmbAudio.currentTextChanged.connect(self.cmbAudioChanged)
        self.cmbAudio.currentTextChanged.connect(self.cp.onEdit)
        self.lblAudio = QLabel("Audio")
        self.cmbSampleRates = QComboBox()
        self.cmbSampleRates.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.cmbSampleRates.currentTextChanged.connect(self.cp.onEdit)
        self.cmbSampleRates.setMaximumWidth(50)
        self.lblSampleRates = QLabel("Samples")

        pnlRow1 = QWidget()
        lytRow1 = QGridLayout(pnlRow1)
        lytRow1.addWidget(self.lblResolutions,  0, 0, 1, 1)
        lytRow1.addWidget(self.cmbResolutions,  0, 1, 1, 1)
        lytRow1.addWidget(self.lblAspect,       0, 2 ,1, 1)
        lytRow1.addWidget(self.cmbAspect,       0, 3, 1, 1)
        lytRow1.setColumnStretch(1, 10)
        lytRow1.setColumnStretch(3, 5)
        lytRow1.setContentsMargins(0, 0, 0, 0)

        pnlRow2 = QWidget()
        lytRow2 = QGridLayout(pnlRow2)
        lytRow2.addWidget(self.lblFrameRate,  0, 0, 1, 1)
        lytRow2.addWidget(self.spnFrameRate,  0, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        lytRow2.addWidget(self.lblGovLength,  0, 2, 1, 1)
        lytRow2.addWidget(self.spnGovLength,  0, 3, 1, 1, Qt.AlignmentFlag.AlignLeft)
        lytRow2.addWidget(self.lblCacheSize,  0, 4, 1, 1)
        lytRow2.addWidget(self.btnClearCache, 0, 5, 1, 1)
        lytRow2.setColumnStretch(4, 5)
        lytRow2.setContentsMargins(0, 0, 0, 0)

        pnlRow3 = QWidget()
        lytRow3 = QGridLayout(pnlRow3)
        lytRow3.addWidget(self.lblBitrate,     0, 0, 1, 1)
        lytRow3.addWidget(self.spnBitrate,     0, 1, 1, 1)
        lytRow3.addWidget(self.lblProfiles,    0, 2, 1, 1)
        lytRow3.addWidget(self.cmbProfiles,    0, 3, 1, 1)
        lytRow3.setColumnStretch(1, 6)
        lytRow3.setColumnStretch(3, 10)
        lytRow3.setContentsMargins(0, 0, 0, 0)

        pnlRow4 = QWidget()
        lytRow4 = QGridLayout(pnlRow4)
        lytRow4.addWidget(self.lblAudio,         0, 0, 1, 1)
        lytRow4.addWidget(self.cmbAudio,         0, 1, 1, 1)
        lytRow4.addWidget(self.lblSampleRates,   0, 2, 1, 1)
        lytRow4.addWidget(self.cmbSampleRates,   0, 3, 1, 1)
        lytRow4.addWidget(QLabel("  "),          0, 4, 1, 1)
        lytRow4.addWidget(self.chkDisableAudio,  0, 5, 1, 1)
        lytRow4.setContentsMargins(0, 0, 0, 0)

        pnlRow5 = QWidget()
        lytRow5 = QGridLayout(pnlRow5)
        lytRow5.addWidget(QLabel(),              0, 0, 1, 1)
        lytRow5.addWidget(self.chkAnalyzeVideo,  0, 1, 1, 1)
        lytRow5.addWidget(QLabel(),              0, 2, 1, 1)
        lytRow5.addWidget(self.chkAnalyzeAudio,  0, 3, 1, 1)
        lytRow5.setColumnStretch(0, 10)
        lytRow5.setContentsMargins(0, 0, 0, 0)

        lytMain = QGridLayout(self)
        lytMain.addWidget(pnlRow1,             1, 0, 1, 2)
        lytMain.addWidget(pnlRow2,             2, 0, 1, 2)
        lytMain.addWidget(pnlRow3,             3, 0, 1, 2)
        lytMain.addWidget(pnlRow4,             4, 0, 1, 2)
        lytMain.addWidget(pnlRow5,             5, 0, 1, 2)

    def fill(self, onvif_data):
        self.cmbResolutions.disconnect()
        self.cmbResolutions.clear()
        i = 0
        while len(onvif_data.resolutions_buf(i)) > 0 and i < 16:
            self.cmbResolutions.addItem(onvif_data.resolutions_buf(i))
            i += 1
        current_resolution = str(onvif_data.width()) + " x " + str(onvif_data.height())
        self.cmbResolutions.setCurrentText(current_resolution)
        self.cmbResolutions.currentTextChanged.connect(self.cp.onEdit)

        self.cmbProfiles.disconnect()
        self.cmbProfiles.clear()
        for profile in onvif_data.profiles:
            self.cmbProfiles.addItem(profile.profile())

        self.cmbProfiles.setCurrentText(onvif_data.profile())
        self.cmbProfiles.currentIndexChanged.connect(self.cmbProfilesChanged)

        self.spnFrameRate.setMaximum(onvif_data.frame_rate_max())
        self.spnFrameRate.setMinimum(onvif_data.frame_rate_min())
        self.spnFrameRate.setValue(onvif_data.frame_rate())

        self.spnGovLength.setMaximum(min(onvif_data.gov_length_max(), 250))
        self.spnGovLength.setMinimum(onvif_data.gov_length_min())
        self.spnGovLength.setValue(onvif_data.gov_length())

        self.spnBitrate.setMaximum(min(onvif_data.bitrate_max(), 16384))
        self.spnBitrate.setMinimum(onvif_data.bitrate_min())
        self.spnBitrate.setValue(onvif_data.bitrate())

        self.cmbAudio.disconnect()
        encoders = onvif_data.audio_encoders()
        encoding = onvif_data.audio_encoding()
        self.cmbAudio.clear()
        self.cmbAudio.addItems(encoders)
        if len(encoding) and not len(encoders):
            self.cmbAudio.addItem(encoding)
        self.cmbAudio.setCurrentText(encoding)
        self.cmbAudio.currentTextChanged.connect(self.cmbAudioChanged)
        self.setAudioOptions(onvif_data)

        self.lblCacheSize.setText("Cache:")
        self.setEnabled(onvif_data.width())
        self.videoChanged = False
        self.audioChanged = False
        self.syncGUI()

    def edited(self, onvif_data):
        result = False
        if self.isEnabled():
            current_resolution = str(onvif_data.width()) + " x " + str(onvif_data.height())
            if not current_resolution == self.cmbResolutions.currentText():
                self.videoChanged = True
                result = True
            if not onvif_data.frame_rate() == self.spnFrameRate.value():
                self.videoChanged = True
                result = True
            if not onvif_data.gov_length() == self.spnGovLength.value():
                if onvif_data.gov_length() > onvif_data.gov_length_min() and onvif_data.gov_length() < max(onvif_data.gov_length_max(), 250):
                    self.videoChanged = True
                    result = True
            if not onvif_data.bitrate() == self.spnBitrate.value():
                if onvif_data.bitrate() > onvif_data.bitrate_min() and onvif_data.bitrate() < max(onvif_data.bitrate_max(), 16384):
                    self.videoChanged = True
                    result = True
            if onvif_data.audio_bitrate():
                if not str(onvif_data.audio_sample_rate()) == self.cmbSampleRates.currentText():
                    selections = []
                    for i in range(self.cmbSampleRates.count()):
                        selections.append(int(self.cmbSampleRates.itemText(i)))
                    if onvif_data.audio_sample_rate() in selections:
                        self.audioChanged = True
                        result = True
                if not onvif_data.audio_encoding() == self.cmbAudio.currentText():
                    self.audioChanged = True
                    result = True

        return result

    def update(self, onvif_data):
        if self.edited(onvif_data):
            self.setEnabled(False)
            if self.videoChanged:
                dims = self.cmbResolutions.currentText().split('x')
                if len(dims) != 2:
                    logger.error("Incorrect onvif data for resolution")                
                    return
                onvif_data.setWidth(int(dims[0]))
                onvif_data.setHeight(int(dims[1]))
                onvif_data.setFrameRate(self.spnFrameRate.value())
                onvif_data.setGovLength(self.spnGovLength.value())
                onvif_data.setBitrate(self.spnBitrate.value())
                onvif_data.startUpdateVideo()
            if self.audioChanged:
                onvif_data.setAudioEncoding(self.cmbAudio.currentText())
                onvif_data.setAudioSampleRate(int(self.cmbSampleRates.currentText()))
                onvif_data.startUpdateAudio()

    def syncGUI(self):
        ratio = self.getCurrentAspect()
        profile = self.cp.getCurrentProfile()
        if profile:

            if profile.getDesiredAspect():
                ratio = profile.getDesiredAspect()

            if profile.audio_bitrate():
                self.chkDisableAudio.setEnabled(True)
                self.cmbAudio.setEnabled(True)
                self.lblAudio.setEnabled(True)
                self.cmbSampleRates.setEnabled(True)
                self.lblSampleRates.setEnabled(True)
                self.chkAnalyzeAudio.setEnabled(True)
            else:
                self.chkDisableAudio.setChecked(False)
                self.chkDisableAudio.setEnabled(False)
                self.cmbAudio.setEnabled(False)
                self.lblAudio.setEnabled(False)
                self.cmbSampleRates.setEnabled(False)
                self.lblSampleRates.setEnabled(False)
                self.chkAnalyzeAudio.setEnabled(False)

            self.chkDisableAudio.setChecked(profile.getDisableAudio())
            if self.chkDisableAudio.isChecked():
                self.cmbAudio.setEnabled(False)
                self.lblAudio.setEnabled(False)
                self.cmbSampleRates.setEnabled(False)
                self.lblSampleRates.setEnabled(False)
                self.chkAnalyzeAudio.setEnabled(False)

            self.chkAnalyzeVideo.setChecked(profile.getAnalyzeVideo())
            self.chkAnalyzeAudio.setChecked(profile.getAnalyzeAudio())

        self.cmbAspect.disconnect()
        found = False
        if ratio >= 176 and ratio <= 178:
            found = True
            self.cmbAspect.setCurrentIndex(0)
        if ratio == 133:
            found = True
            self.cmbAspect.setCurrentIndex(1)
        if ratio == 122:
            found = True
            self.cmbAspect.setCurrentIndex(2)
        if ratio == 150:
            found = True
            self.cmbAspect.setCurrentIndex(3)
        if ratio == 125:
            found = True
            self.cmbAspect.setCurrentIndex(4)
        if ratio == 146:
            found = True
            self.cmbAspect.setCurrentIndex(5)

        camera = self.cp.getCurrentCamera()
        if not found:
            name = ""
            if camera:
                name = camera.name()
            logger.debug(f'The settings for aspect ratio {ratio/100} were not found for camera {name}')
            self.cmbAspect.setCurrentIndex(6)

        if ratio != self.getCurrentAspect():
            self.lblAspect.setText("Aspect*")
        else:
            self.lblAspect.setText("Aspect  ")

        self.cmbAspect.currentTextChanged.connect(self.cmbAspectChanged)

        if camera:
            self.cp.mw.audioConfigure.setCamera(camera)

    def getCurrentAspect(self):
        ratio = 0
        text = self.cmbResolutions.currentText()
        if len(text):
            dims = self.cmbResolutions.currentText().split('x')
            if dims[1]:
                ratio = int(100.0 * float(dims[0]) / float(dims[1]))
        return ratio
    
    def getSelectedAspect(self):
        ratio = 0
        text = self.cmbAspect.currentText()
        if len(text):
            if text != "UNKN":
                dims = self.cmbAspect.currentText().split(':')
                if dims[1]:
                    ratio = int(100.0 * float(dims[0]) / float(dims[1])) 
        return ratio

    def cmbAspectChanged(self):
        desiredAspect = self.getSelectedAspect()
        player = self.cp.getCurrentPlayer()
        if player:
            player.desired_aspect = desiredAspect

        profile = self.cp.getCurrentProfile()
        if profile:
            profile.setDesiredAspect(desiredAspect)

        self.syncGUI()

    def cmbProfilesChanged(self, index):
        camera = self.cp.getCurrentCamera()
        if camera:
            players = self.cp.mw.pm.getStreamPairPlayers(camera.uri())
            camera.setDisplayProfile(index)
            self.cp.signals.fill.emit(camera.onvif_data)
            if len(players):
                for player in players:
                    self.cp.mw.pm.playerShutdownWait(player.uri)
                self.cp.onItemDoubleClicked(camera)

    def chkDisableAudioChanged(self, state):
        profile = self.cp.getCurrentProfile()
        if profile:
            profile.setDisableAudio(state)
        player = self.cp.getCurrentPlayer()
        if player:
            player.disable_audio = bool(state)
            if not player.disable_audio:
                player.request_reconnect = True
                player.running = False
        self.cp.syncGUI()
        self.syncGUI()

    def chkAnalyzeVideoChecked(self, state):
        profile = self.cp.getCurrentProfile()
        if profile:
            profile.setAnalyzeVideo(state)

        player = self.cp.getCurrentPlayer()
        if player:
            player.setAlarmState(0)
            player.analyze_video = bool(state)
            player.boxes = []
            player.labels = []
            player.scores = []

        camera = self.cp.getCurrentCamera()
        if camera:
            self.cp.mw.videoConfigure.setCamera(camera)
        
    def chkAnalyzeAudioChecked(self, state):
        profile = self.cp.getCurrentProfile()
        if profile:
            profile.setAnalyzeAudio(state)
        player = self.cp.getCurrentPlayer()
        if player:
            player.setAlarmState(0)
            player.analyze_audio = bool(state)
        camera = self.cp.getCurrentCamera()
        if camera:
            self.cp.mw.audioConfigure.setCamera(camera)

    def chkRecordMainChanged(self, state):
        profile = self.cp.getCurrentProfile()
        if profile:
            profile.setRecordMain(state)

        if state:
            player = self.cp.getCurrentPlayer()
            if player:
                worker = self.cp.mw.videoPanel.cmbWorker.currentText()
                self.cp.mw.loadVideoWorker(worker)
                self.cp.mw.videoWorker = None

    def updateCacheSize(self, size):
        arg = str(size)
        if size == -1:
            arg = "  "
        self.lblCacheSize.setText("Cache: " + arg)

    def btnClearCacheClicked(self):
        player = self.cp.getCurrentPlayer()
        if player:
            player.clearCache()

    def cmbAudioChanged(self):
        profile = self.cp.getCurrentProfile()
        if profile:
            self.setAudioOptions(profile)

    def setAudioOptions(self, onvif_data):
        index = self.cmbAudio.currentIndex()
        self.cmbSampleRates.clear()
        sample_rates = sorted(onvif_data.audio_sample_rates(index))
        self.cmbSampleRates.addItems([str(item) for item in sample_rates])
        sample_rate = onvif_data.audio_sample_rate()
        if (sample_rate and not len(sample_rates)):
            self.cmbSampleRates.addItem(str(sample_rate))
        self.cmbSampleRates.setCurrentText(str(sample_rate))
