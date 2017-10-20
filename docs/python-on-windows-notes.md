# How to do Python 2.7 development on Windows using powershell, virtual env, pip and VSCode

## Install gitbash from MSI installer

## Install chocolatey package manager 

## Using Chocolatey, install wget 

## Install Python 2.7 using windows 64 bit MSI installer


Add C:\Python27 to PATH environment variable

open gitbash

```
cd 
cd dev
mkdir Python
cd Python
wget https://bootstrap.pypa.io/get-pip.py
python get-pip-py
```

## Configure Environment Variables

Add C:\Python27\Scripts to PATH environment variable

Open Powershell

```
cd 
cd dev/Python
pip install virtualenv
pip install virtualenvwrapper-powershell
Get-ChildItem Env:PSModulePath
cp -R C:\Python27\Lib\site-packages\Users\<username>\Documents\WindowsPowerShell\Modules\VirtualEnvWrapper\* .
```

## Fix broken poweshel scripts

Edit VirtualenvWrapperTabExpansion.psm1 


on line 12 from this:

```
$_oldTabExpansion = Get-Content Function:TabExpansion
```

to this:

```
$_oldTabExpansion = Get-Content Function:TabExpansion2
```

on line 15 from this:

```
$_oldTabExpansion = Get-Content Function:TabExpansion
```

to this:

```
$_oldTabExpansion = Get-Content Function:TabExpansion2
```

## Create a new virtual environment

Open powershell

```
cd 
cd dev/Python
mkdir 'C:\Users\<username>/.virtualenvs'
Import-Module .\VirtualEnvWrapper.psd1
Get-Command *virtualenv*
New-VirtualEnvironment <virtual env name>
```

## Configure VSCode to use the virtualenv (so that debugging works)

Open VSCode preferences (CTRL comma) and add the following lines

```
  "editor.wordWrap": "on",
  "editor.rulers": [
    80    
  ],
  "python.pythonPath": "C:/Users/<username>/.virtualenvs/<virtual env name>/Scripts/Python.exe",  
  "editor.formatOnSave": true
```


## Install pre-compiled modules into the <virtual env name> virtual environment

Open powershell

```
cd dev/Python
Import-Module .\VirtualEnvWrapper.psd1
Set-VirtualEnvironment <virtual env name>
pip install <package-name>
```

```
example

pip install spotipy
```


## Whenever you start a new session

Open powershell

```
cd dev/Python
Import-Module .\VirtualEnvWrapper.psd1
Set-VirtualEnvironment <virtual env name>
```

Your command prompt should look like this (virtual env in parens before PS prompt)

```
(<virtual env name>)PS C:\Users\<username>\dev\Python>
```

## Show environment variables in power shell

Get-ChildItem Env:

## Set environment variables in power shell
[Environment]::SetEnvironmentVariable("SPOTIPY_CLIENT_ID", "example", "User")
[Environment]::SetEnvironmentVariable("SPOTIPY_CLIENT_SECRET", "example", "User")
[Environment]::SetEnvironmentVariable("SPOTIPY_REDIRECT_URI", "example", "User")

restart powershell



