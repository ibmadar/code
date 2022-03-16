class FakeFileSystem(list):
    def copy(self, src, dest):
        self.append(('COPY',src,dest))

    def move(self, src, dest):
        self.append(('MOVE',src,dest))

    def delete(self, src):
        self.append(('DELETE', src))


import os
import shutil
class FileSystem():
    def copy(self, src, dest):
        shutil.copy(src,dest)

    def move(self, src, dest):
        shutil.move(src, dest)

    def delete(self, src):
        os.remove(src)