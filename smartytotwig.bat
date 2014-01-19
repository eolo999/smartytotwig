set PYTHONPATH=%PYTHONPATH%;%~dp0
python %~dp0\smartytotwig\main.py --smarty-file=%1 --twig-file=%1.twig
