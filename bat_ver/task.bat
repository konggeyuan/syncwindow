@echo off & color 0A
rem 添加任务

set file=config.ini

rem 读取配置文件
for /f "skip=1 tokens=1,2 delims==" %%i IN (%file%) do (
	if "%%i"=="min" set min_ini=%%j
	if "%%i"=="script" set task_script=%%j
	if "%%i"=="username" set task_username=%%j
	if "%%i"=="password" set task_password=%%j
	if "%%i"=="task_name" set task_name=%%j
)


rem pause>null

rem 先删除后添加

schtasks /delete /f /tn %task_name%
schtasks /create /sc minute /mo 5 /tn %task_name% /tr %task_script%  /RU %task_username% /RP %task_password%

