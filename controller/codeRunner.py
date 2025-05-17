import subprocess
import os
import tempfile
import shutil
import sqlite3
from contextlib import contextmanager
import streamlit as st

# Default code snippets for each language
default_code = {
    "Python": "# Write your Python code\nprint('Hello, World!')",
    "Streamlit":"import streamlit as st\n st.toast('hello!!')",
    "JavaScript": "// Write your JavaScript code\nconsole.log('Hello, World!');",
    "C++": "#include <iostream>\nusing namespace std;\nint main() {\n    cout << \"Hello, World!\" << endl;\n    return 0;\n}",
    "Java": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}",
    "C": "#include <stdio.h>\nint main() {\n    printf(\"Hello, World!\\n\");\n    return 0;\n}",
    "HTML": "<!DOCTYPE html>\n<html>\n<body>\n    <h1>Hello, World!</h1>\n</body>\n</html>",
    "SQL": "-- Write your SQL queries\nSELECT 'Hello, World!' AS message;",
    "TypeScript": "// Write your TypeScript code\nconsole.log('Hello, World!');"
}

# Context manager for temporary directory
@contextmanager
def temporary_directory():
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

# Function to run Python code
def run_python_code(code):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )
        os.unlink(temp_file)
        return result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timed out."
    except Exception as e:
        return "", f"Error: {str(e)}"
def run_streamlit_code(code):
    if code:
        try:
            # Create a dictionary to capture local variables
            local_vars = {}
            # Execute the code in the context of Streamlit
            exec(code, {"st": st}, local_vars)
            return "", ""
        except Exception as e:
            return "",f"Error executing code: {e}"
    else:
        return "","Please enter a code snippet."
# Function to run JavaScript code
def run_javascript_code(code):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name
        result = subprocess.run(
            ['node', temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )
        os.unlink(temp_file)
        return result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timed out."
    except Exception as e:
        return "", f"Error: {str(e)}"

# Function to run C++ code
def run_cpp_code(code):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name
        executable = temp_file.replace('.cpp', '')
        compile_result = subprocess.run(
            ['g++', temp_file, '-o', executable],
            capture_output=True,
            text=True,
            timeout=10
        )
        if compile_result.returncode != 0:
            os.unlink(temp_file)
            return "", f"Compilation Error:\n{compile_result.stderr}"
        run_result = subprocess.run(
            [executable],
            capture_output=True,
            text=True,
            timeout=10
        )
        os.unlink(temp_file)
        if os.path.exists(executable):
            os.unlink(executable)
        return run_result.stdout, run_result.stderr
    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timed out."
    except Exception as e:
        return "", f"Error: {str(e)}"

# Function to run Java code
def run_java_code(code):
    try:
        with temporary_directory() as temp_dir:
            java_file = os.path.join(temp_dir, 'Main.java')
            with open(java_file, 'w', encoding='utf-8') as f:
                f.write(code)
            compile_result = subprocess.run(
                ['javac', java_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            if compile_result.returncode != 0:
                return "", f"Compilation Error:\n{compile_result.stderr}"
            run_result = subprocess.run(
                ['java', '-cp', temp_dir, 'Main'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return run_result.stdout, run_result.stderr
    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timed out."
    except Exception as e:
        return "", f"Error: {str(e)}"

# Function to run C code
def run_c_code(code):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name
        executable = temp_file.replace('.c', '')
        compile_result = subprocess.run(
            ['gcc', temp_file, '-o', executable],
            capture_output=True,
            text=True,
            timeout=10
        )
        if compile_result.returncode != 0:
            os.unlink(temp_file)
            return "", f"Compilation Error:\n{compile_result.stderr}"
        run_result = subprocess.run(
            [executable],
            capture_output=True,
            text=True,
            timeout=10
        )
        os.unlink(temp_file)
        if os.path.exists(executable):
            os.unlink(executable)
        return run_result.stdout, run_result.stderr
    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timed out."
    except Exception as e:
        return "", f"Error: {str(e)}"

# Function to run HTML code
def run_html_code(code):
    try:
        return code, ""
    except Exception as e:
        return "", f"Error: {str(e)}"

# Function to run SQL code
def run_sql_code(code):
    try:
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        queries = [q.strip() for q in code.split(';') if q.strip()]
        output = []
        for query in queries:
            cursor.execute(query)
            if query.strip().upper().startswith('SELECT'):
                rows = cursor.fetchall()
                if rows:
                    output.append("\n".join([str(row) for row in rows]))
            else:
                conn.commit()
                output.append(f"Query executed successfully: {cursor.rowcount} rows affected.")
        conn.close()
        return "\n\n".join(output), ""
    except sqlite3.Error as e:
        return "", f"SQL Error: {str(e)}"
    except Exception as e:
        return "", f"Error: {str(e)}"

# Function to run TypeScript code
def run_typescript_code(code):
    try:
        with temporary_directory() as temp_dir:
            ts_file = os.path.join(temp_dir, 'main.ts')
            js_file = os.path.join(temp_dir, 'main.js')
            with open(ts_file, 'w', encoding='utf-8') as f:
                f.write(code)
            compile_result = subprocess.run(
                ['tsc', ts_file, '--outFile', js_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            if compile_result.returncode != 0:
                return "", f"Compilation Error:\n{compile_result.stderr}"
            run_result = subprocess.run(
                ['node', js_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            return run_result.stdout, run_result.stderr
    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timed out."
    except Exception as e:
        return "", f"Error: {str(e)}"