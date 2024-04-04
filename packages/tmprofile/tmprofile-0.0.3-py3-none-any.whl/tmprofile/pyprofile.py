""" Inspired from Thomas Rouch:
    https://betterprogramming.pub/ram-and-vram-profiling-in-python-bf99876e985f
"""
from __future__ import annotations
import os
import re
import time
import json
import psutil
import inspect
from functools import wraps
from pathlib import Path
from datetime import timedelta
from matplotlib import pyplot as plt
from IPython import get_ipython  # type: ignore
from typing import cast, Any, Callable, TypeVar, Optional, Iterable
from multiprocessing import Event
from multiprocessing import Process
from multiprocessing.synchronize import Event as EventClass

from prettytable import PrettyTable
import numpy as np
import nvidia_smi  # nvidia-ml-py3


# __________________________________________ Utilities __________________________________________ #


def alphanumeric_sort(iterable: Iterable[str | Path]) -> list[str]:
    """ Sort the given iterable in alphanumeric order, e.g. ['string1', 'string2', 'string10'].

    Args:
        iterable (Iterable[str]): Any iterable sequence of strings.

    Returns:
        list[str]: List of alphanumeric ordered strings.
    """
    iterable = [str(x) for x in iterable]
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(iterable, key=alphanum_key)


def get_total_ram_available_bytes() -> int:
    """ Return the total number of bytes available on the platform. """
    return int(psutil.virtual_memory().total)


def get_total_ram_used_bytes() -> int:
    """ Return the number of bytes currently used on the platform. """
    return int(psutil.virtual_memory().used)


def get_pid_ram_used_bytes(pid: int) -> int:
    """ Return the number of bytes currently used by a given process.
        (Use os.getpid() to get current process ID)
    """
    return int(psutil.Process(pid).memory_info().rss)


def bytes2human(number: int, decimal_unit: bool = True) -> str:
    """ Convert number of bytes in a human readable string.
    >>> bytes2human(10000, True)
    '10.00 KB'
    >>> bytes2human(10000, False)
    '9.77 KiB'
    Args:
        number (int): Number of bytes
        decimal_unit (bool): If specified, use 1 kB (kilobyte)=10^3 bytes.
            Otherwise, use 1 KiB (kibibyte)=1024 bytes
    Returns:
        str: Bytes converted in readable string
    """
    symbols = ['K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
    symbol_values = [(symbol,
                      1000 ** (i + 1) if decimal_unit else (1 << (i + 1) * 10))
                     for i, symbol in enumerate(symbols)]

    for symbol, value in reversed(symbol_values):
        if number >= value:
            suffix = "B" if decimal_unit else "iB"
            return f"{float(number)/value:.2f}{symbol}{suffix}"

    return f"{number} B"


# _______________________________________ parallel logger _______________________________________ #

def _monitor(pid: int, stop_event: EventClass,
             gpu_idx: int, time_delta: float, output_file: str | Path) -> None:
    """ Monitor Memory consumption in parallel to a given process (RAM and VRAM).

    Args:
        pid (int): ID of the Process to monitor
        stop_event (EventClass): Shared event triggered when the monitoring has to stop
        gpu_idx (int): Which gpu's VRAM consumption has to be monitored.
        time_delta (float): Time to wait between two RAM / VRAM consumption logging.
        output_file (_type_): Where to write the logged values (as json).
    """
    # 1. prepare containers
    ram_pid_values = list()
    ram_values = list()
    vram_values = list()
    # 2. init NVIDIA GPU logger
    nvidia_smi.nvmlInit()
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(gpu_idx)
    # 3. get base values
    total_ram_value = get_total_ram_available_bytes()
    total_vram_value = int(nvidia_smi.nvmlDeviceGetMemoryInfo(handle).total)
    # 4. monitor
    tic = time.perf_counter()
    while not stop_event.is_set():
        ram_pid_values.append(get_pid_ram_used_bytes(pid))
        ram_values.append(get_total_ram_used_bytes())
        gpu_info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
        vram_values.append(gpu_info.used)
        time.sleep(time_delta)  # in s
    toc = time.perf_counter()
    elapsed_time = toc - tic
    # 5. shutdown NVIDIA GPU logger
    nvidia_smi.nvmlShutdown()
    # 6. save logged values
    data = dict(ram=ram_values, ram_pid=ram_pid_values, vram=vram_values,
                total_ram=total_ram_value, total_vram=total_vram_value,
                elapsed_time=elapsed_time, time_delta=time_delta)
    json_object = json.dumps(data, indent=4)
    with open(output_file, "w") as outfile:
        outfile.write(json_object)


# _______________________________________ Context manager _______________________________________ #

class Profile:

    def __init__(
        self,
        name: str,
        verbose: bool = False,
        gpu_idx: int = 0,
        time_delta: float = 0.2,
        output_dir: str | Path = '.tmprofile',
        filename: Optional[str | Path] = None
    ) -> None:
        """ Create a context usable as `with MemoryScope(name, ...) as profiler:`.

        Args:
            name (str): Name of the profiler. Will be used to name the saved file.
            verbose (bool, optional): If True, will print logged values on exit. Defaults to False.
            gpu_idx (int, optional): Which gpu's VRAM consumption has to be monitored.
                Defaults to 0.
            time_delta (float, optional): Time to wait (in second) between two RAM / VRAM
                consumption logging. Defaults to 0.2.
            output_dir (str | Path, optional): Directory in which to write the logged values
                (as json). Defaults to '.tmprofile'.
            filename (str | Path, optional):Name of the saved json file. If no name is given, will
                use the profiler name (see `name` above). Defaults to None.
        """
        self._stop_event = Event()
        self._monitor_process: Optional[Process] = None
        self._name = name
        self._verbose = verbose
        self._gpu_idx = gpu_idx
        self._time_delta = time_delta
        self._output_file = self._prepare_output(output_dir, filename)

    def get_run_idx(self, output_dir: Path) -> int:
        runs = alphanumeric_sort(Path(output_dir).glob(f"run*_profile__{self._name}.json"))
        if len(runs) == 0:
            return 1
        return int(Path(runs[-1]).stem.split('run')[1].split('_')[0]) + 1

    def _prepare_output(self, output_dir: str | Path, filename: Optional[str | Path]) -> Path:
        output_dir = Path(output_dir).resolve()
        output_dir.mkdir(exist_ok=True)
        filename = filename if filename is not None else f'profile__{self._name}'
        filename = Path(Path(filename).stem).with_suffix('.json')  # works w/ or w/o extension
        if (output_dir / filename).exists():
            idx = self.get_run_idx(output_dir)
            filename = f'run{idx}_{filename.stem}'
            filename = Path(Path(filename).stem).with_suffix('.json')
        return output_dir / filename

    def print(self) -> None:
        table = PrettyTable(["Memory", "Min", "Median", "Max", "Average"])
        for memory in ('ram', 'vram'):
            total = self.data[f'total_{memory}']
            usage = np.array(self.data[memory])
            values = np.quantile(usage, np.array([0, 0.5, 1]))
            percents = values / total
            row = [memory.upper()]
            for value, percent in zip(values, percents):
                row.append(f"{bytes2human(value)} ({100 * percent:.2f}%)")
            row.append(f"{bytes2human(usage.mean())} ({100 * usage.mean() / total:.2f}%)")
            table.add_row(row)
        time = str(timedelta(seconds=self.data["elapsed_time"])).split(':')
        time_string = f'{time[0]} h {time[1]} m {time[2]} s'
        table.title = f'PROFILE : {self._name} | elapsed time: {time_string} s'
        print('\n' + str(table))
        with open(self._output_file.with_suffix('.txt'), 'w') as openfile:
            openfile.write(str(table))

    def plot(self, percent: bool = False):
        t = len(self.data['ram']) * self.data['time_delta']
        x = np.arange(0, t, self.data['timedelta'])
        ram, vram = np.array(self.data['ram']), np.array(self.data['vram'])
        if percent:
            ram /= self.data['total_ram']
            vram /= self.data['total_vram']
        fig, ax1 = plt.subplots()
        ax1.plot(x, vram, c='red')
        ax1.set_ylabel('VRAM', color='red')
        ax1.tick_params(axis='y', labelcolor='red')
        ax2 = ax1.twinx()
        ax2.plot(x, ram, c='blue')
        ax2.set_ylabel('RAM', color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')
        ax1.set_xlabel('time (s)')
        plt.show()

    def __enter__(self) -> Profile:
        pid = os.getpid()
        args = (pid, self._stop_event, self._gpu_idx, self._time_delta, self._output_file)
        self._monitor_process = Process(target=_monitor, args=args)
        self._monitor_process.start()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback) -> None:
        self._stop_event.set()  # Signal the monitor process to stop
        assert self._monitor_process is not None
        self._monitor_process.join()
        with open(self._output_file, 'r') as openfile:
            self.data = json.load(openfile)
        if not self._verbose:
            return
        try:
            self.print()
        except IndexError:  # wrapped function crashed before any values was recorded
            pass


# __________________________________________ Decorator __________________________________________ #

def is_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


def get_function_name(func: Callable) -> str:
    """Get file and function name."""
    if is_notebook():
        return 'notebook'
    module_name = func.__module__.split('.')[-1]
    if module_name == "__main__":
        module_name = os.path.splitext(os.path.basename(inspect.getfile(func)))[0]
    return f"{module_name}::{func.__name__}"


FuncT = TypeVar('FuncT', bound=Callable[..., Any])


def profile(
    name: Optional[str] = None,
    *,
    verbose: bool = False,
    gpu_idx: int = 0,
    time_delta: float = 0.2,
    output_dir: str | Path = '.tmprofile',
    filename: Optional[str | Path] = None
) -> FuncT:  # type: ignore
    """ A decorator to profile any function, e.g. :

    ```
    @profile(verbose=True)
    def f(...):
    ```

    Args:
        name (str): Name of the profiler. Will be used to name the saved file.
        verbose (bool, optional): If True, will print logged values on exit. Defaults to False.
        gpu_idx (int, optional): Which gpu's VRAM consumption has to be monitored.
            Defaults to 0.
        time_delta (float, optional): Time to wait (in second) between two RAM / VRAM
            consumption logging. Defaults to 0.2.
        output_dir (str | Path, optional): Directory in which to write the logged values
            (as json). Defaults to '.tmprofile'.
        name (str | Path, optional): Name of the saved json file. If no name is given, will use the
            decorated function's name and module as module::function_name. Defaults to None.

    Returns:
        FuncT: Function to be profiled.
    """
    def profile_inner(func: FuncT) -> FuncT:
        """ Time & Memory (RAM and VRAM) Profiling decorator. """
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal name
            name = name if name is not None else get_function_name(func)
            with Profile(name, verbose, gpu_idx, time_delta, output_dir, filename):
                retval = func(*args, **kwargs)
            return retval
        return cast(FuncT, wrapper)
    return cast(FuncT, profile_inner)
