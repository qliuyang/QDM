import shutil
from pathlib import Path
import compileall


class Builder:
    def __init__(self):
        self.src = Path('src').resolve()
        self.build = Path('build').resolve()

        compileall.compile_dir('src', force=True)
        self.move_files_with_extension(self.src / '__pycache__', self.build / 'script', '.pyc')

    def move_files_with_extension(self, source_dir, target_dir, extension):
        """
        将 source_dir 文件夹下指定后缀的文件移动到 target_dir 文件夹。

        参数:
        source_dir (str): 源文件夹路径
        target_dir (str): 目标文件夹路径
        extension (str): 文件后缀，例如 '.txt'
        """
        # 创建 Path 对象
        target_path = Path(target_dir)

        # 确保目标文件夹存在
        target_path.mkdir(parents=True, exist_ok=True)

        # 遍历源文件夹中的所有文件
        for file_path in source_dir.glob(f'*{extension}'):
            file_name = self.getClearFileName(file_path.name)
            # 构建目标文件路径
            new_file_path = target_path / file_name

            # 移动文件
            shutil.move(str(file_path), str(new_file_path))
            print(f'Moved: {file_path} -> {new_file_path}')

    @staticmethod
    def getClearFileName(fileName: str):
        fileNameList = fileName.split('.')
        return fileNameList[0] + '.pyc'


if __name__ == '__main__':
    b = Builder()
