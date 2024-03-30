# powershell/wmic to dict

## pip install psprocsdict

### Tested against Windows 10 / Python 3.11 / Anaconda


```PY
from psprocsdict import get_dict_from_command

data = get_dict_from_command(
    cmd=f'powershell "Get-Process | Select-Object Name, Id, PriorityClass, HandleCount, WorkingSet, PagedMemorySize, PrivateMemorySize, VirtualMemorySize, PeakVirtualMemorySize, PeakPagedMemorySize, PeakWorkingSet | Format-Table *"',
    convert_dtypes_with_ast=True,
    format_powershell=False,
    cols=9999999,
    lines=1,
    sep=" ",
    percentage=100,
    stripspaces=True,
)


data2 = get_dict_from_command(
    cmd=f'powershell "Get-Process | Select-Object Name, Id, PriorityClass, HandleCount, WorkingSet, PagedMemorySize, PrivateMemorySize, VirtualMemorySize, PeakVirtualMemorySize, PeakPagedMemorySize, PeakWorkingSet | Format-Table *"',
    convert_dtypes_with_ast=False,
    format_powershell=False,
    cols=9999999,
    lines=1,
    sep=" ",
    percentage=100,
    stripspaces=True,
)
```