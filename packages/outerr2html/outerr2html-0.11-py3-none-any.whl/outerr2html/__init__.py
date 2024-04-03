import threading
from contextlib import contextmanager
import ctypes
import os
import sys
import asyncio
import aiofiles
from tkkillablethreads import ExecuteAsThreadedTask
import time
import importlib
import io

config = sys.modules[__name__]
config.enco = "utf-8"
windll = ctypes.LibraryLoader(ctypes.WinDLL)
kernel32 = windll.kernel32

try:
    ansi2html = importlib.__import__("ansi2html")
    Ansi2HTMLConverter = ansi2html.Ansi2HTMLConverter
    conv = Ansi2HTMLConverter()
except Exception:
    print("ansi2html not detected, install it: pip install ansi2html")
    conv = None

if sys.version_info < (3, 5):
    libc = ctypes.CDLL(ctypes.util.find_library("c"))
else:
    if hasattr(sys, "gettotalrefcount"):  # debug build
        libc = ctypes.CDLL("ucrtbased")
    else:
        libc = ctypes.CDLL("api-ms-win-crt-stdio-l1-1-0")

STD_OUTPUT_HANDLE = -11
c_stdout = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
STD_ERROR_HANDLE = -12
c_stderr = kernel32.GetStdHandle(STD_ERROR_HANDLE)


async def read_stdout(
    so_list,
    so_file,
    so_sleep,
    so_stoptrigger,
    so_print,
):
    try:
        async with aiofiles.open(
            so_file, encoding=config.enco, errors="backslashreplace"
        ) as f:
            llimit = so_list.pop()

            counter = 0
            filecounter = 0
            while True:
                async for line in f:
                    if any(so_stoptrigger):
                        break
                    if any(so_print):
                        with open(
                            r"CONOUT$",
                            "w",
                            encoding=config.enco,
                            errors="backslashreplace",
                        ) as fox:
                            fox.write(line)
                    if counter >= llimit:
                        filecounter += 1
                        counter = 0
                    ofi = so_file[:-4] + "_" + str(filecounter).zfill(3) + ".txt"
                    if ofi not in so_list:
                        so_list.append(ofi)
                    with open(
                        ofi,
                        "a",
                        encoding=config.enco,
                        errors="backslashreplace",
                    ) as fox2:
                        fox2.write(line)
                        counter += 1
                await asyncio.sleep(so_sleep[0])
    except Exception as e:
        pass


async def read_stderr(
    se_list,
    se_file,
    se_sleep,
    se_stoptrigger,
    se_print,
):
    try:
        async with aiofiles.open(
            se_file, encoding=config.enco, errors="backslashreplace"
        ) as f:
            llimit = se_list.pop()

            counter = 0
            filecounter = 0
            while True:
                async for line in f:
                    if any(se_stoptrigger):
                        break
                    if any(se_print):
                        with open(
                            r"CONOUT$",
                            "w",
                            encoding=config.enco,
                            errors="backslashreplace",
                        ) as fox:
                            fox.write(line)
                    if counter >= llimit:
                        filecounter += 1
                        counter = 0
                    ofi = se_file[:-4] + "_" + str(filecounter).zfill(3) + ".txt"
                    if ofi not in se_list:
                        se_list.append(ofi)
                    with open(
                        ofi,
                        "a",
                        encoding=config.enco,
                        errors="backslashreplace",
                    ) as fox2:
                        fox2.write(line)
                        counter += 1
                await asyncio.sleep(se_sleep[0])
    except Exception as e:
        pass


async def main(
    so_list,
    se_list,
    so_file,
    se_file,
    so_sleep,
    se_sleep,
    so_stoptrigger,
    se_stoptrigger,
    so_print,
    se_print,
):
    try:
        while not os.path.exists(so_file) or not os.path.exists(se_file):
            await asyncio.sleep(1)
        stdout_task = await asyncio.to_thread(
            read_stdout,
            so_list=so_list,
            so_file=so_file,
            so_sleep=so_sleep,
            so_stoptrigger=so_stoptrigger,
            so_print=so_print,
        )
        stderr_task = await asyncio.to_thread(
            read_stderr,
            se_list=se_list,
            se_file=se_file,
            se_sleep=se_sleep,
            se_stoptrigger=se_stoptrigger,
            se_print=se_print,
        )

        await asyncio.gather(stdout_task, stderr_task)
    except Exception as e:
        pass


def run_main(
    so_list,
    se_list,
    so_file,
    se_file,
    so_sleep,
    se_sleep,
    so_stoptrigger,
    se_stoptrigger,
    so_print,
    se_print,
):
    asyncio.run(
        main(
            so_list=so_list,
            se_list=se_list,
            so_file=so_file,
            se_file=se_file,
            so_sleep=so_sleep,
            se_sleep=se_sleep,
            so_stoptrigger=so_stoptrigger,
            se_stoptrigger=se_stoptrigger,
            so_print=so_print,
            se_print=se_print,
        )
    )


def get_timestamp(sep="_"):
    return (
        time.strftime(f"%Y{sep}%m{sep}%d{sep}%H{sep}%M{sep}%S")
        + f"{sep}"
        + (str(time.time()).split(".")[-1] + "0" * 10)[:6]
    )


def killthread(threadobject):
    # based on https://pypi.org/project/kthread/
    if not threadobject.is_alive():
        return True
    tid = -1
    for tid1, tobj in threading._active.items():
        if tobj is threadobject:
            tid = tid1
            break
    if tid == -1:
        sys.stderr.write(f"{threadobject} not found")
        return False
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(SystemExit)
    )
    if res == 0:
        return False
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        return False
    return True


# C and console output crashes on ipython terminal
if sys.modules.get("IPython.terminal.prompts", None):

    @contextmanager
    def stdout_redirector(
        outfolder,
        print_stdout=True,
        print_stderr=True,
        line_limit_out=1000,
        line_limit_err=1000,
        sleep_at_end=1.0,
        convert2html=True,
        delete_txt_files=True,
        sleep_between_checks=0.1,
    ):
        sys.stdout.flush()
        sys.stderr.flush()
        stdoutcopy = sys.stdout
        stderrcopy = sys.stderr
        tstamp = get_timestamp()
        os.makedirs(outfolder, exist_ok=True)
        stdofi = os.path.join(outfolder, f"{tstamp}_std.txt")
        stdofe = os.path.join(outfolder, f"{tstamp}_err.txt")
        stdout_list = [line_limit_out]
        stderr_list = [line_limit_err]
        stdout_sleep = [sleep_between_checks]
        stderr_sleep = [sleep_between_checks]
        stdout_stoptrigger = [False]
        stderr_stoptrigger = [False]
        stdout_print = [print_stdout]
        stderr_print = [print_stderr]
        thread_being_executed = ExecuteAsThreadedTask(
            fu=run_main,
            kwargs={
                "so_list": stdout_list,
                "se_list": stderr_list,
                "so_file": stdofi,
                "se_file": stdofe,
                "so_sleep": stdout_sleep,
                "se_sleep": stderr_sleep,
                "so_stoptrigger": stdout_stoptrigger,
                "se_stoptrigger": stderr_stoptrigger,
                "so_print": stdout_print,
                "se_print": stderr_print,
            },
        )
        try:
            tfile = open(stdofi, "wb", buffering=0)
            sys.stdout = io.TextIOWrapper(
                tfile,
                encoding=config.enco,
                errors="backslashreplace",
                line_buffering=True,
                write_through=True,
            )

            tfileerr = open(stdofe, "wb", buffering=0)

            sys.stderr = io.TextIOWrapper(
                tfileerr,
                encoding=config.enco,
                errors="backslashreplace",
                line_buffering=True,
                write_through=True,
            )
            thread_being_executed()
            yield
        finally:
            time.sleep(sleep_at_end)

            sys.stdout = stdoutcopy
            sys.stderr = stderrcopy

            try:
                stdout_stoptrigger.append(True)
                stderr_stoptrigger.append(True)
            except Exception:
                pass

            if convert2html:
                if conv is None:
                    sys.stderr.write(
                        "Ansi2HTML not installed. No HTML conversion done.\n"
                    )
                    sys.stderr.flush()
                else:
                    for filelists in [stdout_list, stderr_list]:
                        for fi in filelists:
                            with open(
                                fi, "r", encoding=config.enco, errors="backslashreplace"
                            ) as f:
                                with open(
                                    fi[:-4] + ".html",
                                    "w",
                                    encoding=config.enco,
                                    errors="backslashreplace",
                                ) as f2:
                                    f2.write(conv.convert(f.read()))

                    if delete_txt_files:
                        for filelists in [stdout_list, stderr_list]:
                            for fi in filelists:
                                try:
                                    os.remove(fi)
                                except Exception:
                                    pass
            try:
                tfile.close()
            except Exception:
                pass
            try:
                tfileerr.close()
            except Exception as e:
                pass
            thread_being_executed.killthread()
            time.sleep(sleep_at_end)

else:

    @contextmanager
    def stdout_redirector(
        outfolder,
        print_stdout=True,
        print_stderr=True,
        line_limit_out=1000,
        line_limit_err=1000,
        sleep_at_end=1.0,
        convert2html=True,
        delete_txt_files=True,
        sleep_between_checks=0.1,
    ):
        r"""
        Context manager for redirecting stdout and stderr to files.

        This context manager redirects stdout and stderr to specified files while optionally converting them to HTML format
        ( https://pypi.org/project/ansi2html/ needed ). It provides options to control printing stdout and stderr to console, setting line limits for the output files, controlling sleep intervals, and deleting temporary text files after conversion.

        Args:
            outfolder (str): The folder where output files will be stored.
            print_stdout (bool, optional): Whether to print stdout to console (using CONOUT$). Defaults to True.
            print_stderr (bool, optional): Whether to print stderr to console (using CONOUT$). Defaults to True.
            line_limit_out (int, optional): Line limit for stdout in each output file. Defaults to 1000.
            line_limit_err (int, optional): Line limit for stderr in each output file. Defaults to 1000.
            sleep_at_end (float, optional): Time to sleep after context manager exits. Defaults to 1.0.
            convert2html (bool, optional): Whether to convert output files to HTML format. Defaults to True.
            delete_txt_files (bool, optional): Whether to delete temporary text files after conversion. Defaults to True.
            sleep_between_checks (float, optional): Time to sleep (asyncio.sleep) between checks for new output. Defaults to 0.1.

        Yields:
            None: This context manager does not yield any value.

        Example:
            # Redirect stdout and stderr to files
            with stdout_redirector(outfolder="output"):
                print("Hello, world!")  # This will be redirected to a file instead of console
        """

        original_stdout_fd = sys.stdout.fileno()
        original_stderr_fd = sys.stderr.fileno()
        libc.fflush(None)
        sys.stdout.flush()
        sys.stderr.flush()
        stdoutcopy = sys.stdout
        stderrcopy = sys.stderr
        tstamp = get_timestamp()
        os.makedirs(outfolder, exist_ok=True)
        stdofi = os.path.join(outfolder, f"{tstamp}_std.txt")
        stdofe = os.path.join(outfolder, f"{tstamp}_err.txt")
        stdout_list = [line_limit_out]
        stderr_list = [line_limit_err]
        stdout_sleep = [sleep_between_checks]
        stderr_sleep = [sleep_between_checks]
        stdout_stoptrigger = [False]
        stderr_stoptrigger = [False]
        stdout_print = [print_stdout]
        stderr_print = [print_stderr]
        thread_being_executed = ExecuteAsThreadedTask(
            fu=run_main,
            kwargs={
                "so_list": stdout_list,
                "se_list": stderr_list,
                "so_file": stdofi,
                "se_file": stdofe,
                "so_sleep": stdout_sleep,
                "se_sleep": stderr_sleep,
                "so_stoptrigger": stdout_stoptrigger,
                "se_stoptrigger": stderr_stoptrigger,
                "so_print": stdout_print,
                "se_print": stderr_print,
            },
        )
        thread_being_executed()

        # based on https://gist.github.com/natedileas/8eb31dc03b76183c0211cdde57791005
        def _redirect_stdout(to_fd):
            """Redirect stdout to the given file descriptor."""
            # Flush the C-level buffer stdout
            sys.stdout.flush()
            libc.fflush(None)
            # Flush and close sys.stdout - also closes the file descriptor (fd)
            sys.stdout.close()  # works with python.exe, but crashes ipython
            # Make original_stdout_fd point to the same file as to_fd
            os.dup2(to_fd, original_stdout_fd)
            # Create a new sys.stdout that points to the redirected fd
            sys.stdout = io.TextIOWrapper(
                os.fdopen(original_stdout_fd, "wb"),
                encoding=config.enco,
                errors="backslashreplace",
                line_buffering=True,
                write_through=True,
            )

        def _redirect_stderr(to_fd):
            """Redirect stdout to the given file descriptor."""
            # Flush the C-level buffer stdout
            sys.stderr.flush()
            libc.fflush(None)  #### CHANGED THIS ARG TO NONE #############
            # Flush and close sys.stdout - also closes the file descriptor (fd)
            sys.stderr.close()
            # Make original_stdout_fd point to the same file as to_fd
            os.dup2(to_fd, original_stderr_fd)
            # Create a new sys.stdout that points to the redirected fd
            sys.stderr = io.TextIOWrapper(
                os.fdopen(original_stderr_fd, "wb"),
                encoding=config.enco,
                errors="backslashreplace",
                line_buffering=True,
                write_through=True,
            )

        # Save a copy of the original stdout fd in saved_stdout_fd
        saved_stdout_fd = os.dup(original_stdout_fd)
        saved_stderr_fd = os.dup(original_stderr_fd)
        try:
            # Create a temporary file and redirect stdout to it

            tfile = open(stdofi, "wb", buffering=0)
            _redirect_stdout(tfile.fileno())
            # Yield to caller, then redirect stdout back to the saved fd
            tfileerr = open(stdofe, "wb", buffering=0)
            _redirect_stderr(tfileerr.fileno())
            yield
            _redirect_stdout(saved_stdout_fd)
            _redirect_stderr(saved_stderr_fd)
        finally:
            time.sleep(sleep_at_end)
            tfile.close()
            os.close(saved_stdout_fd)
            tfileerr.close()
            os.close(saved_stderr_fd)
            try:
                stdout_stoptrigger.append(True)
                stderr_stoptrigger.append(True)
            except Exception:
                pass
            if convert2html:
                if conv is None:
                    sys.stderr.write(
                        "Ansi2HTML not installed. No HTML conversion done.\n"
                    )
                    sys.stderr.flush()
                else:
                    for filelists in [stdout_list, stderr_list]:
                        for fi in filelists:
                            with open(
                                fi, "r", encoding=config.enco, errors="backslashreplace"
                            ) as f:
                                with open(
                                    fi[:-4] + ".html",
                                    "w",
                                    encoding=config.enco,
                                    errors="backslashreplace",
                                ) as f2:
                                    f2.write(conv.convert(f.read()))

                    if delete_txt_files:
                        for filelists in [stdout_list, stderr_list]:
                            for fi in filelists:
                                try:
                                    os.remove(fi)
                                except Exception:
                                    pass
