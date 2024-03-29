#********************************************************************
# libonvif/onvif-gui/gui/components/thresholdslider.py
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

from PyQt6.QtWidgets import QWidget, QSlider, QLabel, QGridLayout
from PyQt6.QtCore import Qt
from gui.onvif.datastructures import MediaSource

class ThresholdSlider(QWidget):
    def __init__(self, mw, title, module):
        super().__init__()
        self.mw = mw
        self.module = module
        self.sldThreshold = QSlider(Qt.Orientation.Horizontal)
        self.sldThreshold.valueChanged.connect(self.sldThresholdChanged)
        lblThreshold = QLabel(title)
        self.lblValue = QLabel(str(self.sldThreshold.value()))
        lytThreshold = QGridLayout(self)
        lytThreshold.addWidget(lblThreshold,          0, 0, 1, 1)
        lytThreshold.addWidget(self.sldThreshold,     0, 1, 1, 1)
        lytThreshold.addWidget(self.lblValue,         0, 2, 1, 1)
        lytThreshold.setContentsMargins(0, 0, 0, 0)

    def sldThresholdChanged(self, value):
        self.lblValue.setText(str(value))
        match self.mw.videoConfigure.source:
            case MediaSource.CAMERA:
                camera = self.mw.cameraPanel.getCurrentCamera()
                if camera:
                    camera.videoModelSettings.setModelConfidence(value)
                '''
                profile = self.mw.cameraPanel.getCurrentProfile()
                if profile:
                    profile.setModelConfidence(value, self.module)
                '''
            case MediaSource.FILE:
                #self.mw.filePanel.setModelConfidence(value, self.module)
                self.mw.filePanel.videoModelSettings.setModelConfidence(value)

        '''
        player = self.mw.pm.getCurrentPlayer()
        if player:
            player.model_confidence = value / 100
        '''

    def value(self):
        # return a value between 0 and 1
        return self.sldThreshold.value() / 100
    
    def setValue(self, value):
        self.sldThreshold.setValue(value)

