"""
Linux Terminal Simulator
=======================

This program simulates a simple Linux-like shell with a GUI built on Tkinter.
It supports basic filesystem commands (ls, cd, mkdir, touch, rm, cp, mv, cat,
pwd), text utilities (echo, head, tail, grep, wc), system info (date, whoami,
hostname), and permissions changes (chmod). The GUI provides a console-style
experience: a single text widget acts as both output and input, with an inline
prompt at the bottom of the window.

Key implementation details:
- ANSI coloring: We embed simple ANSI escape sequences in output and interpret
  them inside the GUI to colorize entries (e.g., directories vs files in ls).
- Inline prompt: We track the index where the current input begins to prevent
  editing the prompt and to capture the command line when Enter is pressed.
- Quoted arguments: Command parsing uses shlex to support filenames with spaces
  when quoted.
- Cross-platform: Works on Windows (PowerShell/Windows Terminal) and other OSes.

Author: Md Ahsan Ahmed Samdany
"""

__author__ = "Md Ahsan Ahmed Samdany"
__version__ = "1.0.0"
__email__ = "mds22@utas.edu.au"
__status__ = "Development"


import os
import shutil
import sys
import atexit
import stat as stat_module
from datetime import datetime
from typing import List, Tuple
from shlex import split as shlex_split
import getpass
import platform
import re
try:
    import tkinter as tk
    from tkinter import scrolledtext
except Exception:
    tk = None
    scrolledtext = None

# =====================
# Parsing and Utilities
# =====================

def parse_command(user_input: str) -> Tuple[str, List[str]]:
    """
    Parses user input into command name and arguments, supporting quoted paths with spaces.
    """
    try:
        parts = shlex_split(user_input.strip())
    except ValueError:
        parts = user_input.strip().split()
    return parts[0] if parts else "", parts[1:]

def _is_hidden(name: str) -> bool:
    """Return True if the filename is a Unix-style hidden file (starts with '.')."""
    return name.startswith('.')

def _mode_to_string(mode: int, is_dir: bool) -> str:
    """Return a Unix-like permission string (e.g., -rwxr-xr-x) for ls -l output."""
    file_type = 'd' if is_dir else '-'
    perms = ''
    for who in (stat_module.S_IRUSR, stat_module.S_IWUSR, stat_module.S_IXUSR,
                stat_module.S_IRGRP, stat_module.S_IWGRP, stat_module.S_IXGRP,
                stat_module.S_IROTH, stat_module.S_IWOTH, stat_module.S_IXOTH):
        if mode & who:
            if who in (stat_module.S_IRUSR, stat_module.S_IRGRP, stat_module.S_IROTH):
                perms += 'r'
            elif who in (stat_module.S_IWUSR, stat_module.S_IWGRP, stat_module.S_IWOTH):
                perms += 'w'
            else:
                perms += 'x'
        else:
            perms += '-'
    return file_type + perms

def ls(args: List[str]) -> None:
    """List directory contents. Supports -l, -a, -la/-al. Use ? for help.

    - Colors: directories cyan, files green (handled by ANSI codes in GUI).
    - Filenames with spaces are supported by quoting at input parsing.
    """
    if any(arg in ('?', '-h', '--help') for arg in args):
        print("Usage: ls [-l] [-a] [-la|-al]\nList directory contents. Colors indicate type: dirs cyan, files green.")
        return
    show_all = any(arg in ('-a', '-la', '-al') for arg in args)
    long_format = any(arg in ('-l', '-la', '-al') for arg in args)
    try:
        entries = sorted(os.listdir(os.getcwd()))
        display_names = []
        for name in entries:
            if not show_all and _is_hidden(name):
                continue
            display_names.append(name)

        if not long_format:
            # Colorize: directories in cyan, files in light green
            colored = []
            for name in display_names:
                path = os.path.join(os.getcwd(), name)
                is_dir = os.path.isdir(path)
                if is_dir:
                    colored.append(f"\033[96m{name}\033[32m")
                else:
                    colored.append(f"{name}")
            print(" ".join(colored))
            return

        for name in display_names:
            path = os.path.join(os.getcwd(), name)
            try:
                st = os.lstat(path)
            except Exception as e:
                print(f"ls: cannot access '{name}': {e}")
                continue
            is_dir = stat_module.S_ISDIR(st.st_mode)
            mode_str = _mode_to_string(st.st_mode, is_dir)
            size = st.st_size
            mtime = datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M')
            # Colorize name by type
            name_colored = f"\033[96m{name}\033[32m" if is_dir else name
            print(f"{mode_str} {size:>10} {mtime} {name_colored}")
    except Exception as e:
        print(f"ls: {e}")

def cd(args: List[str]) -> None:
    """Changes the current directory based on the given path. With no args, go home. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: cd [dir]\nChange directory. With no argument, go to home directory.")
        return
    if not args:
        try:
            os.chdir(os.path.expanduser("~"))
        except Exception as e:
            print(f"cd: {e}")
        return
    path = args[0]
    try:
        os.chdir(path)
    except FileNotFoundError:
        print(f"cd: {path}: No such file or directory")
    except NotADirectoryError:
        print(f"cd: {path}: Not a directory")
    except Exception as e:
        print(f"cd: {e}")

def mkdir(args: List[str]) -> None:
    """Creates a new directory in the current directory. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: mkdir <name>\nCreate a directory.")
        return
    if not args:
        print("mkdir: missing operand")
        return
    path = args[0]
    try:
        os.mkdir(path)
    except FileExistsError:
        print(f"mkdir: cannot create directory '{path}': File exists")
    except Exception as e:
        print(f"mkdir: {e}")

def touch(args: List[str]) -> None:
    """Creates a new empty file in the current directory. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: touch <file>\nCreate an empty file (overwrite if exists).")
        return
    if not args:
        print("touch: missing operand")
        return
    path = args[0]
    try:
        with open(path, 'w') as f:
            pass
    except Exception as e:
        print(f"touch: {e}")

def rm(args: List[str]) -> None:
    """Removes a file or directory from the current directory. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: rm <path>\nRemove file or directory (recursively for directories).")
        return
    if not args:
        print("rm: missing operand")
        return
    path = args[0]
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    except FileNotFoundError:
        print(f"rm: cannot remove '{path}': No such file or directory")
    except Exception as e:
        print(f"rm: {e}")

def cp(args: List[str]) -> None:
    """Copies a file or directory to a specified destination. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: cp <src> <dst>\nCopy file or directory (recursively).")
        return
    if len(args) < 2:
        print("cp: missing file operand")
        return
    source = args[0]
    dest = args[1]
    try:
        if os.path.isdir(source):
            shutil.copytree(source, dest)
        else:
            shutil.copy(source, dest)
    except FileNotFoundError:
        print(f"cp: cannot stat '{source}': No such file or directory")
    except FileExistsError:
        print(f"cp: '{dest}' already exists")
    except Exception as e:
        print(f"cp: {e}")

def mv(args: List[str]) -> None:
    """Moves or renames a file or directory to a specified destination. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: mv <src> <dst>\nMove or rename.")
        return
    if len(args) < 2:
        print("mv: missing file operand")
        return
    source = args[0]
    dest = args[1]
    try:
        shutil.move(source, dest)
    except FileNotFoundError:
        print(f"mv: cannot stat '{source}': No such file or directory")
    except Exception as e:
        print(f"mv: {e}")

def cat(args: List[str]) -> None:
    """Displays the content of a specified file. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: cat <file>\nPrint file contents.")
        return
    if not args:
        print("cat: missing operand")
        return
    path = args[0]
    try:
        with open(path, 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print(f"cat: {path}: No such file or directory")
    except IsADirectoryError:
        print(f"cat: {path}: Is a directory")
    except Exception as e:
        print(f"cat: {e}")

def pwd(args: List[str]) -> None:
    """Displays the current working directory path. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: pwd\nPrint current working directory.")
        return
    print(os.getcwd())

def help_cmd(args: List[str]) -> None:
    """Display available commands and brief usage documentation."""
    print("Available commands:")
    print("  ls [-l] [-a] [-la|-al]     List directory contents")
    print("  cd [dir]                    Change directory (no arg goes home)")
    print("  mkdir <name>                Create directory")
    print("  touch <file>                Create empty file")
    print("  rm <path>                   Remove file or directory")
    print("  cp <src> <dst>              Copy file or directory")
    print("  mv <src> <dst>              Move or rename")
    print("  cat <file>                  Show file contents")
    print("  pwd                         Print working directory")
    print("  echo [-n] <text>            Print text (-n: no newline)")
    print("  clear                       Clear the screen")
    print("  head [-n N] <file>          Print first N lines (default 10)")
    print("  tail [-n N] <file>          Print last N lines (default 10)")
    print("  grep [-i] [-n] <pat> <file> Search file for pattern")
    print("  wc [-l] [-w] [-c] <file>    Count lines/words/bytes")
    print("  date                        Show current date/time")
    print("  whoami                      Show current user")
    print("  hostname                    Show host name")
    print("  chmod [-R] <mode> <path..>  Change file modes (numeric or symbolic)")
    print("  help                        Show this help")

def echo(args: List[str]) -> None:
    """Echo text to output. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: echo [-n] <text>")
        return
    newline = True
    if args and args[0] == '-n':
        newline = False
        args = args[1:]
    text = " ".join(args)
    if newline:
        print(text)
    else:
        print(text, end="")

def clear_cmd(args: List[str]) -> None:
    """Clear the screen. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: clear")
        return
    global GUI_CLEAR
    if GUI_MODE and GUI_CLEAR:
        GUI_CLEAR()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')

def head_cmd(args: List[str]) -> None:
    """Print first N lines of a file. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: head [-n N] <file>")
        return
    n = 10
    i = 0
    while i < len(args) and args[i].startswith('-'):
        if args[i] == '-n' and i + 1 < len(args):
            try:
                n = int(args[i+1])
            except ValueError:
                print("head: invalid number")
                return
            i += 2
        else:
            break
    if i >= len(args):
        print("head: missing file operand")
        return
    path = args[i]
    try:
        with open(path, 'r', errors='replace') as f:
            for idx, line in enumerate(f):
                if idx >= n:
                    break
                print(line.rstrip('\n'))
    except Exception as e:
        print(f"head: {e}")

def tail_cmd(args: List[str]) -> None:
    """Print last N lines of a file. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: tail [-n N] <file>")
        return
    n = 10
    i = 0
    while i < len(args) and args[i].startswith('-'):
        if args[i] == '-n' and i + 1 < len(args):
            try:
                n = int(args[i+1])
            except ValueError:
                print("tail: invalid number")
                return
            i += 2
        else:
            break
    if i >= len(args):
        print("tail: missing file operand")
        return
    path = args[i]
    try:
        with open(path, 'r', errors='replace') as f:
            lines = f.readlines()
        for line in lines[-n:]:
            print(line.rstrip('\n'))
    except Exception as e:
        print(f"tail: {e}")

def grep_cmd(args: List[str]) -> None:
    """Search for pattern in file. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: grep [-i] [-n] <pattern> <file>")
        return
    import re as _re
    ignore_case = False
    show_line_numbers = False
    i = 0
    while i < len(args) and args[i].startswith('-'):
        if args[i] == '-i':
            ignore_case = True
            i += 1
        elif args[i] == '-n':
            show_line_numbers = True
            i += 1
        else:
            break
    if i + 1 >= len(args):
        print("grep: missing pattern or file")
        return
    pattern = args[i]
    path = args[i+1]
    flags = _re.IGNORECASE if ignore_case else 0
    try:
        regex = _re.compile(pattern, flags)
    except _re.error as e:
        print(f"grep: invalid pattern: {e}")
        return
    try:
        with open(path, 'r', errors='replace') as f:
            for idx, line in enumerate(f, start=1):
                if regex.search(line):
                    prefix = f"{idx}:" if show_line_numbers else ""
                    print(f"{prefix}{line.rstrip('\n')}")
    except Exception as e:
        print(f"grep: {e}")

def wc_cmd(args: List[str]) -> None:
    """Count lines/words/bytes. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: wc [-l] [-w] [-c] [file ...]\nWith no file, counts all regular files in current directory.")
        return
    count_lines = count_words = count_bytes = False
    i = 0
    while i < len(args) and args[i].startswith('-'):
        if args[i] == '-l':
            count_lines = True
        elif args[i] == '-w':
            count_words = True
        elif args[i] == '-c':
            count_bytes = True
        else:
            break
        i += 1
    # Determine target files
    paths: List[str] = []
    if i < len(args):
        paths = args[i:]
    else:
        # No files specified: use all regular files in current directory
        try:
            for name in os.listdir(os.getcwd()):
                full = os.path.join(os.getcwd(), name)
                if os.path.isfile(full):
                    paths.append(name)
        except Exception as e:
            print(f"wc: {e}")
            return

    if not (count_lines or count_words or count_bytes):
        count_lines = count_words = count_bytes = True

    total_lines = total_words = total_bytes = 0
    multiple = len(paths) > 1

    for path in paths:
        try:
            if os.path.isdir(path):
                # Skip directories with a note
                print(f"wc: {path}: Is a directory")
                continue
            with open(path, 'rb') as f:
                data = f.read()
            text = data.decode(errors='replace')
            lines = text.splitlines()
            words = text.split()
            ln = len(lines)
            wn = len(words)
            bn = len(data)
            total_lines += ln
            total_words += wn
            total_bytes += bn
            parts = []
            if count_lines:
                parts.append(str(ln))
            if count_words:
                parts.append(str(wn))
            if count_bytes:
                parts.append(str(bn))
            print(" \t".join(parts) + f" {path}")
        except FileNotFoundError:
            print(f"wc: {path}: No such file or directory")
        except Exception as e:
            print(f"wc: {e}")

    if multiple:
        parts = []
        if count_lines:
            parts.append(str(total_lines))
        if count_words:
            parts.append(str(total_words))
        if count_bytes:
            parts.append(str(total_bytes))
        print(" \t".join(parts) + " total")

def date_cmd(args: List[str]) -> None:
    """Print current date/time. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: date")
        return
    now = datetime.now().strftime('%a %b %d %H:%M:%S %Y')
    print(now)

def whoami_cmd(args: List[str]) -> None:
    """Print current user. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: whoami")
        return
    try:
        import getpass as _getpass
        print(_getpass.getuser())
    except Exception:
        print("unknown")

def hostname_cmd(args: List[str]) -> None:
    """Print host name. Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: hostname")
        return
    import platform as _platform
    print(_platform.node())

def _apply_symbolic_mode(current_mode: int, spec: str) -> int:
    """Apply a single symbolic mode spec like 'u+x', 'g-w', 'a=r' to current_mode."""
    who_map = {
        'u': (stat_module.S_IRUSR, stat_module.S_IWUSR, stat_module.S_IXUSR),
        'g': (stat_module.S_IRGRP, stat_module.S_IWGRP, stat_module.S_IXGRP),
        'o': (stat_module.S_IROTH, stat_module.S_IWOTH, stat_module.S_IXOTH),
        'a': (
            stat_module.S_IRUSR, stat_module.S_IWUSR, stat_module.S_IXUSR,
            stat_module.S_IRGRP, stat_module.S_IWGRP, stat_module.S_IXGRP,
            stat_module.S_IROTH, stat_module.S_IWOTH, stat_module.S_IXOTH,
        ),
    }
    # Parse who
    idx = 0
    who_chars = []
    while idx < len(spec) and spec[idx] in 'ugoa':
        who_chars.append(spec[idx])
        idx += 1
    if not who_chars:
        who_chars = ['a']
    if idx >= len(spec) or spec[idx] not in '+-=':
        raise ValueError("invalid symbolic mode")
    op = spec[idx]
    idx += 1
    perms = spec[idx:]
    perm_set = set(perms)
    if not perm_set.issubset({'r', 'w', 'x'}):
        raise ValueError("invalid permissions in symbolic mode")

    # Build masks
    add_mask = 0
    rem_mask = 0
    eq_mask = 0
    for who in who_chars:
        r, w, x = who_map['u']
        if who == 'g':
            r, w, x = who_map['g']
        elif who == 'o':
            r, w, x = who_map['o']
        elif who == 'a':
            pass  # handled by mapping above
        if who == 'a':
            targets = who_map['a']
            # Expand targets in triples
            for j, mask in enumerate(targets):
                pass
        # Compute per who mask
        per_who_mask = 0
        if 'r' in perm_set:
            per_who_mask |= r
        if 'w' in perm_set:
            per_who_mask |= w
        if 'x' in perm_set:
            per_who_mask |= x

        if op == '+':
            add_mask |= per_who_mask
        elif op == '-':
            rem_mask |= per_who_mask
        else:  # '='
            eq_mask |= per_who_mask

    if op == '+':
        return current_mode | add_mask
    if op == '-':
        return current_mode & ~rem_mask
    # '=': clear corresponding bits then set
    clear_mask = 0
    for who in who_chars:
        if who == 'u':
            clear_mask |= (stat_module.S_IRUSR | stat_module.S_IWUSR | stat_module.S_IXUSR)
        elif who == 'g':
            clear_mask |= (stat_module.S_IRGRP | stat_module.S_IWGRP | stat_module.S_IXGRP)
        elif who == 'o':
            clear_mask |= (stat_module.S_IROTH | stat_module.S_IWOTH | stat_module.S_IXOTH)
        elif who == 'a':
            clear_mask |= (
                stat_module.S_IRUSR | stat_module.S_IWUSR | stat_module.S_IXUSR |
                stat_module.S_IRGRP | stat_module.S_IWGRP | stat_module.S_IXGRP |
                stat_module.S_IROTH | stat_module.S_IWOTH | stat_module.S_IXOTH
            )
    current_mode &= ~clear_mask
    return current_mode | eq_mask

def _parse_mode_spec(spec: str, current_mode: int) -> int:
    """Return new mode from spec which can be numeric (e.g., 755) or symbolic (e.g., u+x,g-w)."""
    # Numeric
    if spec.isdigit():
        try:
            value = int(spec, 8)
        except Exception:
            raise ValueError("invalid numeric mode")
        # Preserve file type bits
        return (current_mode & 0o170000) | value
    # Symbolic (may be comma-separated)
    parts = spec.split(',')
    mode = current_mode
    for part in parts:
        part = part.strip()
        if not part:
            continue
        mode = _apply_symbolic_mode(mode, part)
    return mode

def _chmod_path(path: str, mode_spec: str, recursive: bool) -> None:
    try:
        st = os.lstat(path)
        new_mode = _parse_mode_spec(mode_spec, st.st_mode)
        os.chmod(path, new_mode)
    except PermissionError:
        print(f"chmod: changing permissions of '{path}': Permission denied")
        return
    except FileNotFoundError:
        print(f"chmod: cannot access '{path}': No such file or directory")
        return
    except ValueError as e:
        print(f"chmod: {e}")
        return
    except Exception as e:
        print(f"chmod: {e}")
        return

    if recursive and os.path.isdir(path) and not os.path.islink(path):
        try:
            for root, dirs, files in os.walk(path):
                for name in dirs + files:
                    _chmod_path(os.path.join(root, name), mode_spec, False)
        except Exception as e:
            print(f"chmod: {e}")

def chmod_cmd(args: List[str]) -> None:
    """Change file modes. Supports numeric (e.g., 755) and symbolic (e.g., u+x). Use ? for help."""
    if args and args[0] in ('?', '-h', '--help'):
        print("Usage: chmod [-R] <mode> <path...>\nModes: numeric (e.g., 755) or symbolic (e.g., u+x,g-w,a=r)")
        return
    recursive = False
    i = 0
    if i < len(args) and args[i] == '-R':
        recursive = True
        i += 1
    if i >= len(args):
        print("chmod: missing mode operand")
        return
    mode_spec = args[i]
    i += 1
    if i >= len(args):
        print("chmod: missing file operand")
        return
    paths = args[i:]
    for p in paths:
        _chmod_path(p, mode_spec, recursive)

def _set_terminal_colors() -> None:
    """Set terminal to black background and green foreground using ANSI codes."""
    # Black background (40), Green foreground (32)
    try:
        print("\033[40m\033[32m", end="")
    except Exception:
        pass

def _reset_terminal_colors() -> None:
    """Reset terminal colors to defaults."""
    try:
        print("\033[0m", end="")
    except Exception:
        pass

# GUI integration flags/callbacks
GUI_MODE = False
GUI_ON_EXIT = None
GUI_CLEAR = None

def execute_command(command: str, args: List[str]) -> None:
    """
    Dispatches the command to the appropriate handler function.
    
    Args:
        command: The command name (e.g., 'ls').
        args: List of arguments.
    """
    if command == "ls":
        ls(args)
    elif command == "cd":
        cd(args)
    elif command == "mkdir":
        mkdir(args)
    elif command == "touch":
        touch(args)
    elif command == "rm":
        rm(args)
    elif command == "cp":
        cp(args)
    elif command == "mv":
        mv(args)
    elif command == "cat":
        cat(args)
    elif command == "pwd":
        pwd(args)
    elif command == "echo":
        echo(args)
    elif command == "clear":
        clear_cmd(args)
    elif command == "head":
        head_cmd(args)
    elif command == "tail":
        tail_cmd(args)
    elif command == "grep":
        grep_cmd(args)
    elif command == "wc":
        wc_cmd(args)
    elif command == "date":
        date_cmd(args)
    elif command == "whoami":
        whoami_cmd(args)
    elif command == "hostname":
        hostname_cmd(args)
    elif command == "chmod":
        chmod_cmd(args)
    elif command == "help":
        help_cmd(args)
    elif command == "exit":
        if GUI_MODE and GUI_ON_EXIT:
            GUI_ON_EXIT()
        else:
            _reset_terminal_colors()
        sys.exit(0)
    else:
        print(f"{command}: command not found")

def print_prompt() -> None:
    """Displays the current working directory as a prompt (e.g., '/home/user$')."""
    print(f"{os.getcwd()}$ ", end="")

class _TextRedirector:
    """Redirect printed text into the Tk Text widget with basic ANSI color support.

    We handle a minimal subset of ANSI SGR codes used in this app:
    - "\x1b[32m" (green) and "\x1b[96m" (cyan), and reset "\x1b[0m".
    Unknown codes are ignored and text is printed using the current tag.
    """
    def __init__(self, text_widget: 'tk.Text') -> None:
        self.text_widget = text_widget
        # Current ANSI color tag; default to green (ansi32)
        self.current_tag = 'ansi32'

    def write(self, s: str) -> None:
        if not s:
            return
        # Parse simple ANSI color sequences: \033[96m, \033[32m, \033[0m
        i = 0
        # Ensure widget is editable for output
        try:
            self.text_widget.configure(state=tk.NORMAL)
        except Exception:
            pass
        while i < len(s):
            esc_idx = s.find('\x1b[', i)
            if esc_idx == -1:
                # No more escapes; insert the remainder
                self.text_widget.insert(tk.END, s[i:], (self.current_tag,))
                break
            # Insert text before escape
            if esc_idx > i:
                self.text_widget.insert(tk.END, s[i:esc_idx], (self.current_tag,))
            # Parse the escape code ending with 'm'
            m_idx = s.find('m', esc_idx)
            if m_idx == -1:
                # Malformed; insert rest and stop
                self.text_widget.insert(tk.END, s[esc_idx:], (self.current_tag,))
                break
            code = s[esc_idx+2:m_idx]
            # Update current tag based on code
            if code == '96':
                self.current_tag = 'ansi96'
            elif code == '32':
                self.current_tag = 'ansi32'
            elif code == '0':
                self.current_tag = 'ansi32'
            # Move past the escape
            i = m_idx + 1
        self.text_widget.see(tk.END)
        # Keep widget editable for user input
        try:
            self.text_widget.configure(state=tk.NORMAL)
        except Exception:
            pass

    def flush(self) -> None:
        pass

class LinuxSimulatorApp:
    """GUI application providing a console-like Linux terminal simulator.

    The single ScrolledText acts as both output and input. We keep track of
    the index where the user's current input starts (input_start_index) to
    constrain editing and to capture the line when Enter is pressed.
    """
    def __init__(self) -> None:
        global GUI_MODE, GUI_ON_EXIT, GUI_CLEAR
        if tk is None:
            print("Tkinter not available. GUI mode cannot start.")
            sys.exit(1)
        self.root = tk.Tk()
        self.root.title("Linux Terminal Simulator")
        self.root.configure(bg="#0b0f10")
        try:
            self.root.iconbitmap(False, default='')
        except Exception:
            pass

        # Header bar
        header = tk.Frame(self.root, bg="#11161a")
        header.pack(fill=tk.X)
        title = tk.Label(header, text="Linux Terminal Simulator", fg="#58ff6b", bg="#11161a", font=("Consolas", 12, "bold"))
        title.pack(side=tk.LEFT, padx=8, pady=6)

        # Console area (single text widget acts as terminal)
        self.text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=28, font=("Consolas", 11))
        self.text.configure(bg="#0b0f10", fg="#00ff00", insertbackground="#00ff00", relief=tk.FLAT)
        self.text.configure(state=tk.NORMAL)
        self.text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        # ANSI color tags
        self.text.tag_config('ansi32', foreground="#00ff00")
        self.text.tag_config('ansi96', foreground="#55ffff")

        # Bind keys to emulate terminal behavior
        self.text.bind("<Return>", self.on_return)
        self.text.bind("<BackSpace>", self.on_backspace)
        self.text.bind("<Home>", self.on_home)
        self.text.bind("<Control-l>", self.clear_screen)
        self.text.bind("<Button-1>", self.on_click)
        self.text.bind("<Key>", self.on_key)

        # Redirect stdout/stderr to Text
        sys.stdout = _TextRedirector(self.text)
        sys.stderr = _TextRedirector(self.text)

        # Set mode and exit callback
        GUI_MODE = True
        GUI_ON_EXIT = self.root.destroy
        GUI_CLEAR = self.clear_screen

        # Start in home directory
        try:
            os.chdir(os.path.expanduser("~"))
        except Exception:
            pass

        # Initial prompt
        self.input_start_index = None
        self.render_prompt()
        self.text.focus_set()

        # Ensure colors reset if the process exits (harmless in GUI)
        atexit.register(_reset_terminal_colors)

    def render_prompt(self) -> None:
        """Print a new prompt at the end of the console and mark input start."""
        prompt = f"{os.getcwd()}$ "
        self.text.insert(tk.END, prompt, ('ansi32',))
        self.text.see(tk.END)
        # Mark where user input begins on this line
        self.input_start_index = self.text.index(tk.INSERT)

    def on_return(self, event=None) -> str:
        """Handle Enter: read the current line, execute, and print a new prompt."""
        # Get current input from prompt to end of line
        line_start = self.input_start_index
        line_end = self.text.index("end-1c")
        user_input = self.text.get(line_start, line_end).rstrip("\n")
        # Move cursor to end and add newline
        self.text.insert(tk.END, "\n")
        # Execute command
        command, args = parse_command(user_input)
        execute_command(command, args)
        # New prompt
        self.render_prompt()
        return "break"

    def clear_screen(self, event=None) -> None:
        """Clear the console and reprint the prompt."""
        self.text.delete('1.0', tk.END)
        self.render_prompt()

    def on_backspace(self, event=None) -> str:
        # Prevent deleting into the prompt
        if self.text.compare(tk.INSERT, "<=", self.input_start_index):
            return "break"
        return None

    def on_home(self, event=None) -> str:
        # Move cursor to just after the prompt
        self.text.mark_set(tk.INSERT, self.input_start_index)
        return "break"

    def on_click(self, event=None) -> None:
        # Ensure clicks before prompt move cursor to end
        idx = self.text.index(f"@{event.x},{event.y}")
        if self.text.compare(idx, "<", self.input_start_index):
            self.text.mark_set(tk.INSERT, tk.END)

    def on_key(self, event=None) -> None:
        # Keep cursor at or after prompt
        if self.text.compare(tk.INSERT, "<", self.input_start_index):
            self.text.mark_set(tk.INSERT, tk.END)

    def run(self) -> None:
        self.root.mainloop()

def main() -> None:
    """Launch GUI Linux Simulator window."""
    app = LinuxSimulatorApp()
    app.run()

if __name__ == "__main__":
    main()
