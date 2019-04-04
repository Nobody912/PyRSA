from pylint import epylint as lint

(pylint_stdout, pylint_stderr) = lint.py_run('module_name.py', return_std=True)