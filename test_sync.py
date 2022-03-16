import tempfile
from pathlib import Path
import shutil
from sync import sync, determine_actions, read_paths_and_hashes
from filesystem import FileSystem, FakeFileSystem


class TestE2E:

    @staticmethod
    def test_when_a_file_has_been_renamed_in_the_source():
        try:
            source = tempfile.mkdtemp()
            dest = tempfile.mkdtemp()

            content = "I am a file that was renamed"
            source_path = Path(source) / "source-filename"
            old_dest_path = Path(dest) / "dest-filename"
            expected_dest_path = Path(dest) / "source-filename"
            source_path.write_text(content)
            old_dest_path.write_text(content)

            sync(read_paths_and_hashes, FileSystem(), source, dest)

            assert old_dest_path.exists() is False
            assert expected_dest_path.read_text() == content

        finally:
            shutil.rmtree(source)
            shutil.rmtree(dest)


def test_when_a_file_exists_in_the_source_but_not_the_destination():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        content = "I am a very useful file"
        (Path(source) / "my-file").write_text(content)

        fs = FileSystem()

        sync(read_paths_and_hashes, fs, source, dest)
        print("_"*100)
        print(fs)

        expected_path = Path(dest) / "my-file"
        assert expected_path.exists()
        assert expected_path.read_text() == content

    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)

def test_when_a_file_exists_in_the_source_but_not_the_destination_fake():
    try:
        source = {'hash1': 'myfile.txt'}
        dest =  {'hash2': 'myfile.txt'}

        reader = {"/source": source, "/target": dest}

        fs = FakeFileSystem()

        sync(reader.get, fs, '/source', '/target')



        assert fs == [('COPY',Path('/source/myfile.txt'),Path('/target/myfile.txt')),
                      ('DELETE',Path('/target/myfile.txt'))]

    finally:
        pass



def test_when_a_file_exists_in_the_source_but_not_the_destination():
    source_hashes = {"hash1": "fn1"}
    dest_hashes = {}
    actions = determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))
    assert list(actions) == [("COPY", Path("/src/fn1"), Path("/dst/fn1"))]


def test_when_a_file_has_been_renamed_in_the_source():
    source_hashes = {"hash1": "fn1"}
    dest_hashes = {"hash1": "fn2"}
    actions = determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))
    assert list(actions) == [("MOVE", Path("/dst/fn2"), Path("/dst/fn1"))]
