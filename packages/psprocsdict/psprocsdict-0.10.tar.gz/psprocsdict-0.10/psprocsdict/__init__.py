import numpy as np
from numpyslicesplit import np_slice_split
import subprocess
from ast import literal_eval
from numpytypechecker import dtypecheck

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}


def split_table(utf8textlist, sep=" ", percentage=100, stripspaces=True):
    a = np.array(utf8textlist)
    sepino = ord(sep)
    asint8 = (
        a.view(f"V{a.dtype.base.itemsize}")
        .view(np.uint8)
        .reshape((a.shape[0], a.dtype.base.itemsize))
    ).view(np.uint32)
    ampt = np.zeros(asint8.shape, dtype=np.uint8)
    for q in range((asint8.shape[0])):
        for j in range((asint8.shape[1])):
            if asint8[q][j] == sepino:
                ampt[q][j] = 1

    sumli = np.sum(ampt, axis=0)
    matches = np.where(sumli >= len(a) * (percentage / 100))[0]
    vtu = asint8.view("V1")

    matches = matches * 4
    newmatches = np.concatenate(
        [matches, matches + 1, matches + 2, matches + 3], axis=0
    )
    splitresults = np.vstack(
        [
            np.concatenate(tog)
            for tog in [
                [
                    h.view(f"U{len(h)//4}")
                    for h in np_slice_split(u, newmatches, delete=True)
                ]
                for u in vtu
            ]
        ]
    )

    if stripspaces:
        splitresults = np.array(np.char.array(splitresults).strip())
    return splitresults


def execute_command(
    cmd: str, format_powershell: bool = False, cols: int = 9999999, lines: int = 1
) -> list:
    """
    Executes a command and returns the output as a list of strings.

    Args:
        cmd (str): The command to be executed.
        format_powershell (bool, optional): Indicates whether the command should be formatted for PowerShell. Defaults to False.
        cols (int, optional): The number of columns. Defaults to 9999999.
        lines (int, optional): The number of lines. Defaults to 1.

    Returns:
        list: The output of the command as a list of strings.
    """

    if format_powershell:
        cmd = f'powershell "{cmd} | Format-Table *"'
    p = subprocess.Popen(
        f"cmd.exe /w=mode con:cols={cols} lines={lines}",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        **invisibledict,
    )
    cmdbytes = cmd.encode()
    p.stdin.write(cmdbytes + b"\n")
    p.stdin.flush()
    stdo, stde = p.communicate()
    cmdlen = len(cmd)
    indexofcmd = stdo.find(cmdbytes)
    indextocut = indexofcmd + cmdlen
    stdo = stdo[indextocut:]
    assplitlines = stdo.splitlines()
    cutvalue_end = len(assplitlines)
    for q in range(len(assplitlines) - 1, 0, -1):
        if not assplitlines[q].strip():
            cutvalue_end = q
            break

    assplitlines = assplitlines[:cutvalue_end]
    return [x.decode("utf-8", "replace") for x in assplitlines if x.strip(b" -")]


def astfu(alllists):
    resultlist = []
    for x in alllists:
        try:
            resultlist.append(literal_eval(x))
        except Exception:
            resultlist.append(x)
    try:
        return np.array(resultlist)
    except Exception:
        return np.array(resultlist, dtype=object)


def get_dict_from_command(
    cmd,
    convert_dtypes_with_ast=True,
    format_powershell=False,
    cols=9999999,
    lines=1,
    sep=" ",
    percentage=100,
    stripspaces=True,
) -> dict:
    """
    A function that takes a command string, executes it, and returns the output formatted as a dictionary.

    Parameters:
        cmd (str): The command string to execute.
        convert_dtypes_with_ast (bool): Whether to convert data types using ast library (default is True).
        format_powershell (bool): Whether to format the command as a PowerShell command (default is False).
        cols (int): Number of columns for cmd.exe (default is 9999999).
        lines (int): Number of lines for cmd.exe (default is 1).
        sep (str): Separator used to split the command output into columns (default is " ").
        percentage (int): Percentage of data to consider for conversion (default is 100).
        stripspaces (bool): Whether to strip spaces from the command output (default is True).

    Returns:
        dict: A dictionary containing the processed output of the command.
    """

    utf8textlist = execute_command(
        cmd=cmd, format_powershell=format_powershell, cols=cols, lines=lines
    )
    tab = split_table(
        utf8textlist, sep=sep, percentage=percentage, stripspaces=stripspaces
    )
    outdict = {}
    for t in range(tab.shape[1]):
        if convert_dtypes_with_ast:
            conv = dtypecheck(
                tab[..., t][1:],
                filterna=True,
                float2int=True,
                show_exceptions=False,
                dtypes=(np.int64, np.float64, np.datetime64),
            )
            if conv.dtype not in [np.int64, np.float64, np.datetime64]:
                conv = astfu(conv)
            for cou in range(len(conv)):
                didi = outdict.setdefault(cou, {})
                didi[tab[:1][..., t][0]] = conv[cou]
        else:
            for cou in range(1, len(tab)):
                didi = outdict.setdefault(cou, {})
                didi[tab[:1][..., t][0]] = tab[..., t][cou]

    return outdict

