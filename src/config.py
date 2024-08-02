import json
import logging
import re
from pathlib import Path
from typing import Dict, List


class Config:
    CONFIG_PATH = "config/config.json"

    def __init__(self):
        self.config = self.readJson(self.CONFIG_PATH)

        self._state = {}
        self._configTran = []

        self._downloadConfig = self.config['download']
        self._windowConfig = self.config['window']

        self.initDownloadConfig()

    @staticmethod
    def readJson(filePath: str | Path) -> Dict:
        try:
            with open(filePath, "r", encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(e)

    def initDownloadConfig(self):
        self._setDefaultIfEmpty('tempPath', Path.home() / "Temp")
        self._setDefaultIfEmpty('downloadInfoPath', Path.cwd() / 'info')
        self._setDefaultIfEmpty('output', Path.home() / 'Downloads' / 'output')
        self.save()

    def _setDefaultIfEmpty(self, key, default_path):
        """
        如果配置项为空，则设置为默认值
        :param key: 配置项的键
        :param default_path: 默认路径
        """
        if self._downloadConfig[key] == "":
            self._downloadConfig[key] = str(default_path)

    def save(self):
        with open(self.CONFIG_PATH, "w", encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)

    def setConfigTran(self, configTran: List):
        self._configTran = configTran

    def setStateConfig(self, state: Dict):
        self._state = state

    def getConfigTran(self):
        return self._configTran

    def getStateConfig(self) -> Dict:
        return self._state

    def getDownloadConfig(self) -> Dict:
        return self.config['download']

    def getWindowConfig(self) -> Dict:
        return self.config['window']

    def getWindowStyleConfig(self) -> Dict:
        return self.config['window']['windowStyle']


class ConfigContext:
    def __init__(self):
        self.config = Config()


class StyleTextCompiler:
    def __init__(self):
        self.pattern = re.compile(r'\${\b([a-zA-Z0-9-]+)\b}')

    def replaceVariable(self, windowStyleConfig: Dict, style: str):
        def replaceCallback(match):
            key = match.group(1)
            return windowStyleConfig.get(key, match.group(0))

        return self.pattern.sub(replaceCallback, style, count=100)


class Style:
    STYLE_PATH = Path("style")

    def __init__(self, className: str, styleTheme: str, config: Config):
        self._config = config

        self._className = className
        self._styleTheme = styleTheme

        self._resultStyle = ""
        self._mainStyle = ""
        self._style = ""

        self._windowStyleConfig = self._config.getWindowStyleConfig()

    def compileStyle(self):
        styleCompiler = StyleTextCompiler()

        result = styleCompiler.replaceVariable(self._windowStyleConfig, self._mainStyle)
        if result == self._mainStyle:
            raise Exception("Failed to compile style")
        else:
            return result

    def buildStyle(self):
        self._style = self._load_style(f"{self._className}-{self._styleTheme}.qss")
        self._mainStyle = self._load_style("main.qss") + self._style if self._style else ""
        self._resultStyle = self.compileStyle()

    def _load_style(self, fileName: str) -> str:
        styleFilePath = self.STYLE_PATH / fileName
        try:
            with open(styleFilePath, "r", encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logging.error(f"Failed to load style file {styleFilePath}: {e}")
            return ""

    def getClickedStyle(self):
        color = self._windowStyleConfig.get(f"{self._styleTheme}-clickedBtn-color", "")
        style = f"""
            background-color: {color};
            border-left: 4px solid #009faa;
        """
        return style

    @property
    def styleTheme(self):
        return self._styleTheme

    @property
    def style(self):
        return self._resultStyle
