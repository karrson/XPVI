@echo off
pushd "%~dp0"
python3 --version >nul 2>&1 && (
    python3 XPVI.py %*
) || (
    python XPVI.py %*
)
popd