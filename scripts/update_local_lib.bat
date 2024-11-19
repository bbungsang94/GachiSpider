echo %cd%
call ".\temp\Scripts\activate.bat"
if %ERRORLEVEL% NEQ 0 (
	echo Failed activate python environmnet
	timeout /t 5
	exit /b 1
)
echo Activated temp environmnet to install latest version
echo Check your path

cd ..\
echo %cd%

timeout /t 5
echo Install latest version

pip install --upgrade pip
pip install . --target ./aws/lambda/Lib --upgrade

echo Sweep dump files
rmdir /s /q "./build"
rmdir /s /q "./spider.egg-info"
rmdir /s /q "./aws/lambda/Lib/spider-1.2.dist-info"

timeout /t 30