import pytest
import os
import re
import shutil
from unittest.mock import Mock

import massrename as mr


@pytest.fixture
def test_dir(tmp_path):
    d = tmp_path / "testdir"
    d.mkdir()
    (d / "file1.txt").touch()
    (d / "file2.log").touch()
    (d / "another file.txt").touch()
    sd = d / "subdir"
    sd.mkdir()
    (sd / "subfile1.txt").touch()
    return d


def test_basic_rename(test_dir):
    args = Mock(
        verbose=False,
        ignorecase=False,
        recursive=False,
        force=True,
        directory=str(test_dir),
        pattern="file(.*)\\.txt",
        replacement="newfile\\1.txt",
    )
    mr.run(args)
    assert not (test_dir / "file1.txt").exists()
    assert (test_dir / "newfile1.txt").exists()
    assert (test_dir / "file2.log").exists()
    assert (test_dir / "another file.txt").exists()
    assert (test_dir / "subdir" / "subfile1.txt").exists()


def test_recursive_rename(test_dir):
    args = Mock(
        verbose=False,
        ignorecase=False,
        recursive=True,
        force=True,
        directory=str(test_dir),
        pattern="(.*)\\.txt",
        replacement="\\1.bak",
    )
    mr.run(args)
    assert not (test_dir / "file1.txt").exists()
    assert (test_dir / "file1.bak").exists()
    assert (test_dir / "file2.log").exists()
    assert not (test_dir / "another file.txt").exists()
    assert (test_dir / "another file.bak").exists()
    assert not (test_dir / "subdir" / "subfile1.txt").exists()
    assert (test_dir / "subdir" / "subfile1.bak").exists()


def test_ignore_case(test_dir):
    (test_dir / "FILE3.TXT").touch()
    args = Mock(
        verbose=False,
        ignorecase=True,
        recursive=False,
        force=True,
        directory=str(test_dir),
        pattern="file(.*)\\.txt",
        replacement="newfile\\1.txt",
    )
    mr.run(args)
    assert not (test_dir / "file1.txt").exists()
    assert (test_dir / "newfile1.txt").exists()
    assert not (test_dir / "FILE3.TXT").exists()
    assert (test_dir / "newfile3.txt").exists()


def test_collision_detection(test_dir):
    (test_dir / "a.txt").touch()
    (test_dir / "b.txt").touch()
    args = Mock(
        verbose=True, # to capture debug output
        ignorecase=False,
        recursive=False,
        force=True,
        directory=str(test_dir),
        pattern=".*\\.txt",
        replacement="c.txt",
    )
    mr.run(args)
    # The outcome is a bit tricky to predict, but we can check
    # that not everything was renamed to c.txt
    renamed_files = [f for f in os.listdir(test_dir) if f.endswith(".txt")]
    assert "c.txt" in renamed_files
    assert len(renamed_files) > 1


def test_confirm_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert mr.confirm("Test prompt") is True


def test_confirm_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert mr.confirm("Test prompt") is False


def test_confirm_default_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert mr.confirm("Test prompt", resp=True) is True


def test_confirm_default_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert mr.confirm("Test prompt", resp=False) is False
