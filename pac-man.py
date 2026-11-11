"""Entry point required by the subject: ``python3 pac-man.py config.json``."""
import runpy

if __name__ == '__main__':
    runpy.run_module('src', run_name='__main__', alter_sys=True)
