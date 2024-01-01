# from ..tool import Tool
# begin code intepreter
import pexpect
from uuid import uuid4
from typing import TYPE_CHECKING, List, Union
import subprocess
import platform
from langchain.utilities import PythonREPL
from langchain.tools.base import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from pydantic import Field, root_validator
from typing import Any, Dict, Optional
from io import StringIO
from contextlib import redirect_stdout
import sys
import re
import asyncio
import ast
import mysql.connector as msql


class CodeInterpreter:
    def __init__(self, timeout=300):
        self.globals = {}
        self.locals = {}
        self.timeout = timeout

    def execute_code(self, code):
        try:
            # Wrap the code in an eval() call to return the result
            wrapped_code = f"__result__ = eval({repr(code)}, globals(), locals())"
            exec(wrapped_code, self.globals, self.locals)
            return self.locals.get('__result__', None)
        except Exception as e:
            try:
                # If eval fails, attempt to exec the code without returning a result
                exec(code, self.globals, self.locals)
                return "Code executed successfully."
            except Exception as e:
                return f"Error: {str(e)}"

    def reset_session(self):
        self.globals = {}
        self.locals = {}


# Usage example


# @tool.get("/execute_code")
def execute_pycode(code: str):
    '''execute Python expressions with Python Interpreter, can be used as a simple calculator e.g., "(123 + 234) / 23 * 19"
    '''
    interpreter = CodeInterpreter()
    return interpreter.execute_code(code)

# end code intepreter


# sql intepreter(Mysql)

def execute_mysql_query(sql_cmd: str, password: str, host: str = "localhost", user: str = "root", database: str = "INFORMATION_SCHEMA"):
    conn = msql.connect(host=host, user=user,
                        password=password, database=database)  # give ur username, password
    try:
        cursor = conn.cursor()
        cursor.execute(sql_cmd)

        column_names = [i[0] for i in cursor.description]
        rows = cursor.fetchall()
        # return rows
        rows_string = []
        for row in rows:
            current_row = [column_names[i]+": " +
                           str(row[i]) for i in range(len(row))]
            current_row = ', '.join(current_row)
            rows_string.append(current_row)
        rows_string = '\n'.join(rows_string)
        return rows_string

    except msql.Error as e:
        print(f"Error connecting to MySQL: {e}")

# end


# python--REPL

"""A tool for running python code in a REPL."""


def _get_default_python_repl() -> PythonREPL:
    return PythonREPL(_globals=globals(), _locals=None)


def sanitize_input(query: str) -> str:
    """Sanitize input to the python REPL.
    Remove whitespace, backtick & python (if llm mistakes python console as terminal)

    Args:
        query: The query to sanitize

    Returns:
        str: The sanitized query
    """

    # Removes `, whitespace & python from start
    query = re.sub(r"^(\s|`)*(?i:python)?\s*", "", query)
    # Removes whitespace & ` from end
    query = re.sub(r"(\s|`)*$", "", query)
    return query


class PythonREPLTool(BaseTool):
    """A tool for running python code in a REPL."""

    name = "Python_REPL"
    description = (
        "A Python shell. Use this to execute python commands. "
        "Input should be a valid python command. "
        "If you want to see the output of a value, you should print it out "
        "with `print(...)`."
    )
    python_repl: PythonREPL = Field(default_factory=_get_default_python_repl)
    sanitize_input: bool = True

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        """Use the tool."""
        if self.sanitize_input:
            query = sanitize_input(query)
        return self.python_repl.run(query)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        """Use the tool asynchronously."""
        if self.sanitize_input:
            query = sanitize_input(query)

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self.run, query)

        return result


class PythonAstREPLTool(BaseTool):
    """A tool for running python code in a REPL."""

    name = "python_repl_ast"
    description = (
        "A Python shell. Use this to execute python commands. "
        "Input should be a valid python command. "
        "When using this tool, sometimes output is abbreviated - "
        "make sure it does not look abbreviated before using it in your answer."
    )
    globals: Optional[Dict] = Field(default_factory=dict)
    locals: Optional[Dict] = Field(default_factory=dict)
    sanitize_input: bool = True

    @root_validator(pre=True)
    def validate_python_version(cls, values: Dict) -> Dict:
        """Validate valid python version."""
        if sys.version_info < (3, 9):
            raise ValueError(
                "This tool relies on Python 3.9 or higher "
                "(as it uses new functionality in the `ast` module, "
                f"you have Python version: {sys.version}"
            )
        return values

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        try:
            if self.sanitize_input:
                query = sanitize_input(query)
            tree = ast.parse(query)
            module = ast.Module(tree.body[:-1], type_ignores=[])
            exec(ast.unparse(module), self.globals, self.locals)  # type: ignore
            module_end = ast.Module(tree.body[-1:], type_ignores=[])
            module_end_str = ast.unparse(module_end)  # type: ignore
            io_buffer = StringIO()
            try:
                with redirect_stdout(io_buffer):
                    ret = eval(module_end_str, self.globals, self.locals)
                    if ret is None:
                        return io_buffer.getvalue()
                    else:
                        return ret
            except Exception:
                with redirect_stdout(io_buffer):
                    exec(module_end_str, self.globals, self.locals)
                return io_buffer.getvalue()
        except Exception as e:
            return "{}: {}".format(type(e).__name__, str(e))

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        """Use the tool asynchronously."""

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self._run, query)

        return result

# end


def exectue_pycode_REPL(code: str, sync: bool = True):
    try:
        tool = PythonREPLTool()
        if sync:
            return tool._run(code)
        else:
            return tool._arun(code)
    except Exception as e:
        return f"Error: {str(e)}"


def exectue_pycode_REPL_Ast(code: str, sync: bool = True):
    try:
        tool = PythonAstREPLTool()
        if sync:
            return tool._run(code)
        else:
            return tool._arun(code)
    except Exception as e:
        return f"Error: {str(e)}"


# shell


def _lazy_import_pexpect() -> pexpect:
    """Import pexpect only when needed."""
    if platform.system() == "Windows":
        raise ValueError(
            "Persistent bash processes are not yet supported on Windows.")
    try:
        import pexpect

    except ImportError:
        raise ImportError(
            "pexpect required for persistent bash processes."
            " To install, run `pip install pexpect`."
        )
    return pexpect


class BashProcess:
    """Executes bash commands and returns the output."""

    def __init__(
        self,
        strip_newlines: bool = False,
        return_err_output: bool = False,
        persistent: bool = False,
    ):
        """Initialize with stripping newlines."""
        self.strip_newlines = strip_newlines
        self.return_err_output = return_err_output
        self.prompt = ""
        self.process = None
        # Uncomment code below if not on Windows
        if persistent:
            # uncomment code below if on a Unix machine
            """ self.prompt = str(uuid4())
            self.process = self._initialize_persistent_process_unix(self.prompt)

    @staticmethod
    def _initialize_persistent_process_unix(prompt: str) -> pexpect.spawn:
        # Start bash in a clean environment
        # Doesn't work on windows
        pexpect = _lazy_import_pexpect()
        process = pexpect.spawn(
            "env", ["-i", "bash", "--norc", "--noprofile"], encoding="utf-8"
        )
        # Set the custom prompt
        process.sendline("PS1=" + prompt)

        process.expect_exact(prompt, timeout=10)
        return process """

    def run(self, commands: Union[str, List[str]]) -> str:
        """Run commands and return final output."""
        # print("entering run")
        if isinstance(commands, str):
            commands = [commands]
        commands = ";".join(commands)
        # print(commands)
        if self.process is not None:
            return self._run_persistent(
                commands,
            )
        else:
            return self._run(commands)

    def _run(self, command: str) -> str:
        """Run commands and return final output."""
        # print("entering _run")
        try:
            output = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            ).stdout.decode()
        except subprocess.CalledProcessError as error:
            if self.return_err_output:
                return error.stdout.decode()
            return str(error)
        if self.strip_newlines:
            output = output.strip()
        return output

    def process_output(self, output: str, command: str) -> str:
        # Remove the command from the output using a regular expression
        pattern = re.escape(command) + r"\s*\n"
        output = re.sub(pattern, "", output, count=1)
        return output.strip()

    def _run_persistent(self, command: str) -> str:
        # Run commands and return final output.
        # print("entering _run_persistent")
        pexpect = _lazy_import_pexpect()
        if self.process is None:
            raise ValueError("Process not initialized")
        self.process.sendline(command)

        # Clear the output with an empty string
        self.process.expect(self.prompt, timeout=10)
        self.process.sendline("")

        try:
            self.process.expect([self.prompt, pexpect.EOF], timeout=10)
        except pexpect.TIMEOUT:
            return f"Timeout error while executing command {command}"
        if self.process.after == pexpect.EOF:
            return f"Exited with error status: {self.process.exitstatus}"
        output = self.process.before
        output = self.process_output(output, command)
        if self.strip_newlines:
            return output.strip()
        return output


# @tool.get("/shell_run")
def execute_bash_code(commands: str, strip_newlines: bool = False, return_err_output=True, persistent=False):
    '''Run commands and return final output. 
        Queries to shell_run must ALWAYS have this structure: {\"commands\": query}.\n",
        and query should be a command string.
    '''
    process = BashProcess(strip_newlines=strip_newlines,
                          return_err_output=return_err_output, persistent=persistent)
    return process.run(commands)


if __name__ == '__main__':
    # interpreter.execute_code("print(\"hello world\")")
    """ python_code = "import geopy\nimport geopy.distance\nlatitude = 40.05555\nlongitude = -75.090723\n_, lo_max, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=90)\n_, lo_min, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=270)\nla_max, _, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=0)\nla_min, _, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=180)\nans = (la_max, la_min, lo_max, lo_min)"
    global_var = {"ans": 0}
    answer = execute(python_code)
    print(answer) """
    # sql_cmd = "select * from lib.books"
    # print(msql.__version__)
    # rows = execute_mysql_query(sql_cmd)
    # print(rows)
    # print(exectue_pycode_REPL_Ast('print(1)'))
    # print(execute_bash_code("echo Hello, World!"))
    print(execute_pycode("(123 + 234) / 23 * 19"))
    pass
