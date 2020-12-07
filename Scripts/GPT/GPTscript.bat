@echo off
::enable delayed expansion - used to resolve variable in loop
:: variable has to be used with '!' instead of '%'
setlocal ENABLEDELAYEDEXPANSION
set gptPath="C:\Program Files\snap\bin\gpt.exe"

::::::::::::::::::::::::::::::::::::::::::::
:: User Configuration
::::::::::::::::::::::::::::::::::::::::::::

:: set path to xml-graph, source and output directory 
set graphXmlPath="..."
set OutputPath=...
set targetFilePrefix=Preprocessed_


for /D %%F in (...*.SAFE) do (
  echo "Processing: %%F"
  echo "Check Targetfile Name: %OutputPath%/%targetFilePrefix%_%%~nF.nc"
  call %gptPath% %graphXmlPath% -Pinput1=%%F -Poutput1=%OutputPath%/%targetFilePrefix%_%%~nF.nc
 )
pause

