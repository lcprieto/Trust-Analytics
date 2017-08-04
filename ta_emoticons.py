# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 13:34:39 2017

@author: Luis Carlos Prieto
"""

import ta_ConfigManager

class EmoticonDetector:
    emoticons = {}
    miConf = ta_ConfigManager.Configuracion()
    def __init__(self, emoticon_file=miConf.m_Emoticonos):
        from pathlib import Path
        content = Path(emoticon_file).read_text()
        positive = True
        for line in content.split("\n"):
            if "positivo" in line.lower():
                positive = True
                continue
            elif "negativo" in line.lower():
                positive = False
                continue

            self.emoticons[line] = positive

    def is_positive(self, emoticon):
        if emoticon in self.emoticons:
            return self.emoticons[emoticon]
        return False

    def is_emoticon(self, to_check):
        return to_check in self.emoticons