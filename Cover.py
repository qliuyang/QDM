import subprocess
from typing import List
import os
from pathlib import Path
import sys


class CoverFile:
    def __init__(self):

        self.script_path = Path("src").resolve()
        self.ui_path = Path("ui").resolve()
        self.res_path = Path("res").resolve()
        self.ts_path = Path("ts").resolve()

        self.python_interpreter = Path(sys.executable).parent

        # 动态选择扩展名
        exe_extension = '.exe' if os.name == 'nt' else ''

        self.uic_compiler = self.python_interpreter / f"pyside6-uic{exe_extension}"
        self.rec_compiler = self.python_interpreter / f"pyside6-rcc{exe_extension}"
        self.ts_compiler = self.python_interpreter / f"pyside6-lupdate{exe_extension}"
        self.qm_compiler = self.python_interpreter / f"pyside6-lrelease{exe_extension}"

        # 验证编译器的存在性
        self._verify_tools_exist()

        self.excludeFiles = ['Test.ui',"settingComponent.ui"]

    @staticmethod
    def get_files(path: Path, fileType: str) -> List[Path]:
        return list(path.glob(fileType))

    def cover_ui_file(self):
        ui_files = self.get_files(self.ui_path, "*.ui")
        for file in ui_files:
            if file.name not in self.excludeFiles:
                cmd = [str(self.uic_compiler), str(file), "-o", str(self.script_path / f"Ui_{file.stem}.py")]
                self.cover(cmd)

    def cover_rc_file(self):
        rc_files = self.get_files(self.res_path, "*.qrc")
        for file in rc_files:
            cmd = [str(self.rec_compiler), str(file), "-o", str(self.script_path / f"{file.stem}_rc.py")]
            self.cover(cmd)

    def cover_ts_file(self):
        python_files = self.get_files(self.script_path, "*.py")
        ui_files = self.get_files(self.ui_path, "*.ui")
        cmd = [str(self.ts_compiler), *python_files, *ui_files, "-ts", str(self.ts_path / "main.ts")]
        self.cover(cmd)

    def cover_qm_file(self):
        qm_files = self.get_files(self.ts_path, "*.ts")
        for file in qm_files:
            cmd = [str(self.qm_compiler), str(file), "-qm", str(self.script_path / 'qm' / f"{file.stem}.qm")]
            self.cover(cmd)

    @staticmethod
    def cover(cmd):
        subprocess.run(cmd)

    def _verify_tools_exist(self):
        tools = [self.uic_compiler, self.rec_compiler, self.ts_compiler, self.qm_compiler]
        for tool in tools:
            if not tool.exists():
                raise FileNotFoundError(f"工具 {tool.name} 不存在于 {self.python_interpreter}。")


if __name__ == '__main__':
    cover = CoverFile()
    cover.cover_ui_file()
    # cover.cover_rc_file()
    # cover.cover_ts_file()
    # cover.cover_qm_file()
