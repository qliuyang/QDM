import shutil
import subprocess
from pathlib import Path


class Builder:
    def __init__(self):
        self.src = Path('src')
        cmd = ['easycython']
        for file in self.src.glob('*.py'):
            cmd.append(str(file))
        subprocess.run(cmd)

        for file in self.src.glob('*.c'):
            file.unlink()
        for file in self.src.glob('*.html'):
            file.unlink()

        self.move_files_with_extension(Path.cwd(), 'PyStand-py38-pyside2-lite/script', '.pyd')

    @staticmethod
    def move_files_with_extension(source_dir, target_dir, extension):
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
            # 构建目标文件路径
            new_file_path = target_path / file_path.name

            # 移动文件
            shutil.move(str(file_path), str(new_file_path))
            print(f'Moved: {file_path} -> {new_file_path}')


if __name__ == '__main__':
    b = Builder()
