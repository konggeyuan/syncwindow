@echo off & color 0A
setlocal enabledelayedexpansion 

rem 判断文件时间

set dayLength=-1
set file=D:\rsyncfile\test
set back=D:\rsyncfile\backup
set log=D:\rsyncfile\log

rem 几天后的日期
echo Wscript.echo dateadd("d",%dayLength%,date)>vbs.vbs
for /f %%a in ('cscript //nologo vbs.vbs') do del vbs.vbs&&set delDate=%%a

rem %delDate%
rem %delDate:~,4%

for /f "skip=4 tokens=1,3,4 delims= " %%a in ('dir %file% /a-d') do (

    set t=%%a
	set y=!t:~,4!
	set m=!t:~5,2!
	set d=!t:~8,2!
    
    if  !y! LSS  %delDate:~,4% (
	   rem %delDate:~,4%
	   move %file%\%%c %back%
       echo %delDate:~,4%-%delDate:~5,2%-%delDate:~8,2%------->>%log%\%delDate:~,4%-%delDate:~5,2%-%delDate:~8,2%.txt
       echo %file%\%%c %back%>>%log%\%delDate:~,4%-%delDate:~5,2%-%delDate:~8,2%.txt
	)

    if  !m! LSS  %delDate:~5,2% (
	   echo %delDate:~5,2%
	   move %file%\%%c %back%
       echo %delDate:~,4%-%delDate:~5,2%-%delDate:~8,2%------->>%log%\%delDate:~,4%-%delDate:~5,2%-%delDate:~8,2%.txt
       echo %file%\%%c %back%>>%log%\%delDate:~,4%-%delDate:~5,2%-%delDate:~8,2%.txt
	)

    if  !d! LSS  %delDate:~8,2% (
	   echo %delDate:~8,2%
       move %file%\%%c %back%
       echo %delDate:~,4%-%delDate:~5,2%-%delDate:~8,2%------->>%log%\%delDate:~,4%-%delDate:~5,2%-%delDate:~8,2%.txt
       echo %file%\%%c %back%>>%log%\%delDate:~,4%-%delDate:~5,2%-%delDate:~8,2%.txt
	)

)