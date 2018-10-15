@echo off & color 0A
rem 读取配置


set file=D:\test\config.ini
set adb=D:\test\adb.exe
for /f "skip=1 tokens=1,2 delims==" %%i IN (%file%) do (
	
	rem echo %%i
	rem echo %%j
	if "%%i"=="impath" set value=%%j 
	if "%%i"=="phone_storage" set phone_storage=%%j
)


rem echo %value%
rem pause>null


for /R %value% %%f in (*.*) do (
%adb% push %%f %phone_storage%
)