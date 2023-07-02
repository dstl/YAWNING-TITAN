@ECHO OFF

setlocal EnableDelayedExpansion

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=.
set BUILDDIR=_build

set AUTOSUMMARYDIR="%cd%\source\_autosummary\"

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.https://www.sphinx-doc.org/
	exit /b 1
)

if "%1" == "" goto help

REM delete autosummary if it exists

IF EXIST %AUTOSUMMARYDIR% (
    echo deleting %AUTOSUMMARYDIR%
    RMDIR %AUTOSUMMARYDIR% /s /q
)

REM print the YT licenses
set YTLICENSEBUILD=pip-licenses --format=rst --with-urls
set YTDEPS="%cd%\source\yt-dependencies.rst"

%YTLICENSEBUILD% --output-file=%YTDEPS%

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:clean
IF EXIST %AUTOSUMMARYDIR% (
    echo deleting %AUTOSUMMARYDIR%
    RMDIR %AUTOSUMMARYDIR% /s /q
)

:end
popd
