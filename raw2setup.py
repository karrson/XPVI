with open('setup_raw.py', 'r') as a:
    setup_raw = a.read()
    with open('XPVI.bat', 'r') as b:
        bat = b.read()
        with open('XPVI.sh', 'r') as c:
            shell = c.read()
            with open('XPVI.py', 'r') as d:
                py = d.read()
                with open('setup.py', 'w') as e:
                    e.write(setup_raw.replace(
                        'BATCH_CODE', str(bat.encode(
                            'unicode_escape'))[2:-1].replace('\\\\', '\\')
                    ).replace(
                        'SHELL_CODE', str(shell.encode(
                            'unicode_escape'))[2:-1].replace('\\\\', '\\')
                    ).replace(
                        'PYTHON_CODE', str(py.encode(
                            'unicode_escape'))[2:-1].replace('\\\\', '\\')
                    ))
