- v1.0.14 Mar 2024
	- use pure css to set black output cell background in generated html, instead of javascript.
	  This helps with rendering html files uploaded to 3rd party renderers such as sharepoint, 
	  who sanitize javascript in user uploaded html files.
	
- v1.0.13 Feb 2024
	- nbrshell_common: export LD_LIBRARY_PATH. This helps ggsci.
	- pbrun_as_oracle: Do not raise exception when oracle_sid is not passed. Set it to "dummy_sid"

- v1.0.12 Feb 2024
	- pbrun_as_oracle: if oracle_sid not passed as parameter, then take it from previously saved with set_nbrshell_env
	- nbrshell_common: prevent grep from parsing minus sign in ORACLE_SID, to allow -MGMTDB sid.
	
- v1.0.11 Feb 2024
	- fixing ORATAB parsing to avoid lines commented out
	
- v1.0.10 Feb 2024
	- fixing loosing black background on nbrshell reimport
	- allow pip install from github
	- Readme update
	
- v1.0.7 Feb 2024
	- adding pbrun_sqlplus cell magic
	- ability to set and reuse connection parameters
	- setting dark output background
	- moved git root one level down to nbrshell directory
	
- v1.0.6 Feb 2024
	- if standard error was not empty, then logger.error both standard out and standard error
	
- v1.0.5 Jan 2023
	- catch all exceptions in paramiko in ssh.connect and ssh.exec_command and print to logger
	
- v1.0.4 Sep 2022
	- catch paramiko.ssh_exception.NoValidConnectionsError and print exception to avoid printing error stack
	  This happens when there is no sshd on port 22 on target
	
- v1.0.3 Aug 2022
	- In addition to catching ssh connection exceptions and printing exception name, also 
	  return string f"AuthenticationException: {e}" to let calling function handle it.
	  Not reraising exception though, to be in line with what happens when error happens while running remote script
	
- v1.0.2 Feb 2022
	- Catch paramiko ssh connection exceptions to print just exception name instead of full stack.
	  This in particular covers wrong hostname and wrong ssh password.
	
- v1.0.1 Dec 2021
	- added "cd /tmp" before sending script to pbrun, to avoid 
		```
		shell-init: error retrieving current directory: getcwd: cannot access parent directories: Permission denied
		chdir: error retrieving current directory: getcwd: cannot access parent directories: Permission denied
		```
		from pbrun attempting to run script in connected user directory
		
- v1.0
	- initial version
