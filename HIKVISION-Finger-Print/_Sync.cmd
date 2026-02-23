CLS
@ECHO OFF
ECHO  ____                     ____         
ECHO / ___^| _   _ _ __   ___  ^| __ ) _   _  
ECHO \___ \^| ^| ^| ^| '_ \ / __^| ^|  _ \^| ^| ^| ^| 
ECHO  ___) ^| ^|_^| ^| ^| ^| ^| (__  ^| ^|_) ^| ^|_^| ^| 
ECHO ^|____/ \__, ^|_^| ^|_^|\___^| ^|____/ \__, ^| 
ECHO      __^|___/          _         ^|___/  
ECHO     ^|  \/  ^| ___  ___^| ^|__  _   _      
ECHO     ^| ^|\/^| ^|/ _ \/ __^| '_ \^| ^| ^| ^|     
ECHO     ^| ^|  ^| ^|  __/\__ \ ^| ^| ^| ^|_^| ^|     
ECHO     ^|_^|  ^|_^|\___^|^|___/_^| ^|_^|\__,_^| 

For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
For /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a:%%b)
set d=%mydate%  %mytime: =%

git pull
git rm -r --cached . > nul
git add .
git commit -m "%d%"
git push

rem echo %errorlevel%
IF %ERRORLEVEL% == 0 GOTO SUCCESS
GOTO ERROR

:SUCCESS
cls
ECHO  ____
ECHO / ___^| _   _  ___ ___ ___  ___ ___
ECHO \___ \^| ^| ^| ^|/ __/ __/ _ \/ __/ __^|
ECHO  ___) ^| ^|_^| ^| (_^| (_^|  __/\__ \__ \
ECHO ^|____/ \__,_^|\___\___\___^|^|___/___/


timeout /t 3
GOTO END

:ERROR
CLS
ECHO  _____ ____  ____   ___  ____  
ECHO ^| ____^|  _ \^|  _ \ / _ \^|  _ \ 
ECHO ^|  _^| ^| ^|_) ^| ^|_) ^| ^| ^| ^| ^|_) ^|
ECHO ^| ^|___^|  _ ^<^|  _ ^<^| ^|_^| ^|  _ ^< 
ECHO ^|_____^|_^| \_\_^| \_\\___/^|_^| \_\
cd
pause
explorer .
pause

:END
REM End of script

rem Author Meshu
rem fb.me/m3shu
rem meshu12345@gmail.com

