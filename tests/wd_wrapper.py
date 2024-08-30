"""Class for working with pytest and git.

.. seealso:

   class WorkDir
   `[source] <https://github.com/pypa/setuptools_scm/blob/main/testing/wd_wrapper.py>`_
   `[license:MIT] <https://github.com/pypa/setuptools_scm/blob/main/LICENSE>`_

"""

from __future__ import annotations

import itertools
import os
import platform
import shlex
import subprocess as sp  # noqa: S404
from pathlib import Path, WindowsPath
from typing import Dict, List


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

    def git_config_list(self) -> Dict[str, str]:
        """:code:`git` returns a line seperated list, parse it.

        Extract the :code:`key=value` pairs.

        Returns
        -------
            Dict[str, str] -- git config dotted keys and each respective value

        """
        cmd = "git config --list"
        cp_out = run(cmd, cwd=self.cwd)
        is_key_exists = cp_out is not None and isinstance(cp_out, sp.CompletedProcess)
        d_ret = {}
        if is_key_exists:
            str_blob = cp_out.stdout
            key_val_pairs = str_blob.split(os.linesep)
            for key_val_pair in key_val_pairs:
                if len(key_val_pair) != 0:
                    pair = key_val_pair.split("=")
                    if len(pair) == 2:
                        key = pair[0]
                        val = pair[1]
                        d_ret[key] = val
        else:
            # no git config settings? Hmmm ...
            pass

        return d_ret

    def git_config_get(
        self,
        dotted_key: str,
    ) -> str | None:
        """From :code:`git`, get a config setting value.

        .. seealso:

           git_config_list

        Parameters
        ----------
        dotted_key
            |str| -- a valid :code:`git config` key. View known keys
            :code:`git config --list`

        Returns
        -------
            [str] | |None| -- If the key has a value, the value otherwise |None|

        """
        # Getting all the key value pairs, can be sure the setting exists
        # cmd if went the direct route: :code:`git config [dotted key]`
        d_pairs = self.git_config_list()
        if dotted_key in d_pairs.keys():
            ret = d_pairs[dotted_key]
        else:
            ret = None

        return ret

    def git_config_set(
        self,
        dotted_key: str,
        val: str,
        is_path: bool = False,
    ) -> bool:
        """Set a :code:`git` config setting.

        Parameters
        ----------
        dotted_key
            |str| -- a valid :code:`git config` key. View known keys
            :code:`git config --list`

        val
            |str| -- Value to set

        is_path
            |bool| -- On windows, the path needs to be backslash escaped

        Returns
        -------
            [bool| -- |True| on success otherwise |False|

        - On Windows, the executable path must be resolved

        - On Windows, Inventory path must be surrounded by single quotes so the
          backslashes are not removed by bash

        - On Windows, double quotes does not do the backslash escaping

        - On Windows, assume no space in the path

        """
        is_win = platform.system().lower() == "windows"
        cmd = [
            "git",
            "config",
            dotted_key,
        ]
        if is_path and is_win:
            # In Bash, single quotes protect (Windows path) backslashes
            # Does not deal with escaping spaces
            # `Path is Windows safe <https://stackoverflow.com/a/68555279>`_
            escaped_val = "'" + str(WindowsPath(val)) + "'"
            cmd.append(escaped_val)
        else:
            cmd.append(val)
        # Sphinx hates \$
        # It's non-obvious if the above solution is viable.
        # git config diff.inv.textconv "sh -c 'sphobjinv co plain \"\$0\" -'"
        # git config diff.inv.textconv "sh -c 'sphobjinv-textconv \"\$0\"'"
        cp_out = run(cmd, cwd=self.cwd)
        if cp_out is None or cp_out.returncode != 0:
            ret = False
        else:
            ret = True

        return ret
