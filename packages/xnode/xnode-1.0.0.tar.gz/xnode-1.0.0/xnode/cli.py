import os
import platform
import posixpath
import re
import serial.serialutil

import click
import dotenv

config = dotenv.find_dotenv(filename=".xnode", usecwd=True)
if config:
    dotenv.load_dotenv(dotenv_path=config)

import xnode.files as files
import xnode.pyboard as pyboard

_board = None

def windows_full_port_name(portname):
    m = re.match("^COM(\d+)$", portname)
    if m and int(m.group(1)) < 10:
        return portname
    else:
        return "\\\\.\\{0}".format(portname)

@click.group()
@click.option(
    "--sport",
    envvar="SERIAL_PORT",
    required=True,
    type=click.STRING,
    help="Name of serial port for connected board.",
    metavar="SPORT",
)
@click.option(
    "--baud",
    envvar="SERIAL_BAUD",
    default=115200,
    type=click.INT,
    help="Baud rate for the serial connection (default 115200).",
    metavar="BAUD",
)
def cli(sport, baud):
    global _board

    if platform.system() == "Windows":
        port = windows_full_port_name(sport)
        
    _board = pyboard.Pyboard(sport, baud)

@cli.command()
@click.argument("remote_file")
@click.argument("local_file", type=click.File("wb"), required=False)
def get(remote_file, local_file):
    board_files = files.Files(_board)
    contents = board_files.get(remote_file)

    if local_file is None:
        print(contents.decode("utf-8"))
    else:
        local_file.write(contents)

@cli.command()
@click.option(
    "--exists-okay", is_flag=True, help="Ignore if the directory already exists."
)
@click.argument("directory")
def mkdir(directory, exists_okay):
    board_files = files.Files(_board)
    board_files.mkdir(directory, exists_okay=exists_okay)

@cli.command()
@click.argument("directory", default="/")
@click.option(
    "--long_format",
    "-l",
    is_flag=True,
    help="Print long format info including size of files.",
)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="recursively list all files and (empty) directories.",
)
def ls(directory, long_format, recursive):
    board_files = files.Files(_board)
    for f in board_files.ls(directory, long_format=long_format, recursive=recursive):
        print(f)

def __dir_put(local, remote):
    board_files = files.Files(_board)
    for parent, child_dirs, child_files in os.walk(local, followlinks=True):
        remote_parent = posixpath.normpath(
            posixpath.join(remote, os.path.relpath(parent, local))
        )
        try:
            board_files.mkdir(remote_parent)
        except files.DirectoryExistsError:
            pass
        for filename in child_files:
            with open(os.path.join(parent, filename), "rb") as infile:
                remote_filename = posixpath.join(remote_parent, filename)
                board_files.put(remote_filename, infile.read())

@cli.command()
@click.argument("local", type=click.Path(exists=True))
@click.argument("remote", required=False)
def put(local, remote):
    if remote is None:
        remote = os.path.basename(os.path.abspath(local))
    if os.path.isdir(local):
        __dir_put(local, remote)
    else:
        with open(local, "rb") as infile:
            board_files = files.Files(_board)
            board_files.put(remote, infile.read())
    
@cli.command()
@click.argument("remote_file")
def rm(remote_file):
    board_files = files.Files(_board)
    board_files.rm(remote_file)

@cli.command()
@click.option(
    "--missing-okay", is_flag=True, help="Ignore if the directory does not exist."
)
@click.argument("remote_folder")
def rmdir(remote_folder, missing_okay):
    board_files = files.Files(_board)
    board_files.rmdir(remote_folder, missing_okay=missing_okay)

@cli.command()
@click.argument("type")
def format(type):
    board_files = files.Files(_board)
    if type.lower() == 'a':
        board_files.format_a()
    elif type.lower() == 'b':
        board_files.format_b()
    else:
        print("failed type")

@cli.command()
@click.argument("local_file")
@click.option(
    "--no-stream",
    "-n",
    is_flag=True,
    help="No input/output stream connections",
)
@click.option(
    "--input-on",
    "-i",
    is_flag=True,
    help="Input stream connection",
)
def run(local_file, no_stream, input_on):
    board_files = files.Files(_board)
    try:
        board_files.run(local_file, not no_stream, input_on)
    except IOError:
        click.echo(
            "Failed to find or read input file: {0}".format(local_file), err=True
        )

@cli.command()
@click.option(
    "--hard",
    "mode",
    flag_value="NORMAL",
    help="Perform a hard reboot, including running init.py",
)
@click.option(
    "--repl",
    "mode",
    flag_value="SOFT",
    default=True,
    help="Perform a soft reboot, entering the REPL  [default]",
)
def reset(mode):
    _board.enter_raw_repl()
    if mode == "SOFT":
        _board.exit_raw_repl()
        return

    _board.exec_(
    """if 1:
        def reset():
            import machine
            machine.reset()
        """
    )

    try:
         _board.exec_raw_no_follow("reset()")
    except serial.serialutil.SerialException as e:
        pass

@cli.command()
def scan():
    pass

@cli.command()
def init():
    print("Fromat XNode...")
    board_files = files.Files(_board)
    board_files.format_b()
    
    print("Install pop library on XNode...")        
    local = os.path.join(os.path.dirname(__file__), "pop")
    remote =  "/flash/lib/pop"
    __dir_put(local, remote)
    
    print("The job is done!")          