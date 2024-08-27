"""Class for working with pytest and git.

.. seealso:

   class WorkDir
   `[source] <https://github.com/pypa/setuptools_scm/blob/main/testing/wd_wrapper.py>`_
   `[license:MIT] <https://github.com/pypa/setuptools_scm/blob/main/LICENSE>`_

"""

from __future__ import annotations

import itertools
import os
import shlex
import subprocess as sp  # noqa: S404
from pathlib import Path
from typing import List


def run(
    cmd: List[str] | str,
    cwd: Path = None,
) -> sp.CompletedProcess | None:
    """Run a command.

    Parameters
    ----------
    cmd

        |str| or |list| -- The command to run within a subprocess

    cwd

        |Path| or |str| or |None| -- base folder path. |None| current process cwd


    Returns
    -------
    cp

        subprocess.CompletedProcess or |None| -- Subprocess results

    """
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    else:
        cmd = [os.fspath(x) for x in cmd]

    try:
        p_out = sp.run(cmd, cwd=cwd, text=True, capture_output=True)  # noqa: S603
    except sp.CalledProcessError:
        ret = None
    else:
        ret = p_out

    return ret


class WorkDir:
    """a simple model for working with git."""

    #: set the git commit command
    commit_command: str
    #: if signed is True, use this alternative git commit command
    signed_commit_command: str
    #: set the git add command
    add_command: str

    def __repr__(self) -> str:
        """Representation capable of reinstanciating an instance copy.

        Does not remember the add, commit, or signed commit commands

        Returns
        -------
        Representation str

            |str| -- representation str of class and state

        """
        return f"<WD {self.cwd}>"

    def __init__(self, cwd: Path) -> None:
        """Class instance constructor.

        Parameters
        ----------
        cwd

        |Path| -- Base folder

        """
        self.cwd = cwd
        self.__counter = itertools.count()

    def __call__(self, cmd: List[str] | str, **kw: object) -> str:
        """Run a cmd.

        Parameters
        ----------
        cmd

            list[str] or |str| -- Command to run

        kw

            Only applies if command is a |str|. :func:`str.format` parameters

        Returns
        -------
        cp

            subprocess.CompletedProcess -- Subprocess results

        """
        if kw:
            assert isinstance(cmd, str), "formatting the command requires text input"
            cmd = cmd.format(**kw)

        return run(cmd, cwd=self.cwd).stdout

    def write(self, name: str, content: str | bytes) -> Path:
        """Create a file within the cwd.

        Parameters
        ----------
        name

            |str| -- file name

        content

            |str| or |bytes| -- content to write to file

        Returns
        -------
        AbsolutePath

            |Path| -- Absolute file path

        """
        path = self.cwd / name
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        return path

    def _reason(self, given_reason: str | None) -> str:
        """Format commit reason.

        Parameters
        ----------
        given_reason

            |str| or |None| -- commit reason. If |None|, message will
            be ``number-[instance count]``.

        Returns
        -------
        FormattedReason

            |str| -- formatted reason

        """
        if given_reason is None:
            return f"number-{next(self.__counter)}"
        else:
            return given_reason

    def add_and_commit(
        self, reason: str | None = None, signed: bool = False, **kwargs: object
    ) -> None:
        """Add files and create a commit.

        Parameters
        ----------
        reason

            |str| or None -- Default |None|. Reason for commit. If |None|,
            use default reason

        signed

            |bool| -- Default |False|. If True use signed commit command
            otherwise use not signed commit command.

        kwargs

            object -- Unused parameter. Probably a placeholder to conform to
            abc method signature

        """
        self(self.add_command)
        self.commit(reason=reason, signed=signed, **kwargs)

    def commit(self, reason: str | None = None, signed: bool = False) -> None:
        """Commit message.

        Parameters
        ----------
        reason

            |str| or None -- Default |None|. Reason for commit. If |None|,
            use default reason

        signed

            |bool| -- Default |False|. If True use signed commit command
            otherwise use not signed commit command.

        """
        reason = self._reason(reason)
        self(
            self.commit_command if not signed else self.signed_commit_command,
            reason=reason,
        )

    def commit_testfile(self, reason: str | None = None, signed: bool = False) -> None:
        """Commit a test.txt file.

        Parameters
        ----------
        reason

            |str| or None -- Default |None|. Reason for commit. If |None|,
            use default reason

        signed

            |bool| -- Default |False|. If True use signed commit command
            otherwise use not signed commit command.

        """
        reason = self._reason(reason)
        self.write("test.txt", f"test {reason}")
        self(self.add_command)
        self.commit(reason=reason, signed=signed)
