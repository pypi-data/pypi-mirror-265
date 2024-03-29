
#
# common functions for pbrun_* modules
#

import re

from subprocess import Popen, PIPE, STDOUT

import paramiko
from socket import gaierror
from time import sleep

import logging
logger = logging.getLogger(__name__)

_ssh_conn=""
_psw=""
_pbrun_user=""
_oracle_sid=""
_oracle_conn="/ as sysdba"

def _set_output_cell_black_background():
    """
        make output cells white text on dark background
    """
    from IPython.display import display, HTML
    display(
        HTML("""
            <div id='id_nbrshell'></div>
            <style>
                .jp-OutputArea:has(div#id_nbrshell)>div>div.jp-OutputArea-output:not(#id_nbrshell) {
                    --jp-content-font-color1: silver;
                    background-color: #101010;
                }               
            </style>
            """))

def set_nbrshell_env(ssh_conn, ssh_psw, pbrun_user=None, oracle_sid=None, oracle_conn=None):
    """
        Public function to store connection info in module variables.
        
        ssh_conn should have form 'user@host'
        oracle_conn should be complete connection sufficient for connection to a db.
            Example 1: oracle_conn='/ as sysdba'
            Example 2: oracle_conn='user/psw@tnsalias'
    """
    global _ssh_conn, _psw, _pbrun_user, _oracle_sid, _oracle_conn
    
    _ssh_conn=ssh_conn
    _psw=ssh_psw
    
    if pbrun_user:
        _pbrun_user=pbrun_user
   
    if oracle_sid:
        _oracle_sid=oracle_sid
        
    if oracle_conn:
        _oracle_conn=oracle_conn


def set_psw(psw):
    """
        Public function to store psw in a module variable.
        The stored value optionally can be used instead of supplying psw on each cell magic call
    """
    global _psw
    _psw=psw


def _parse_str_as_parameters(line):
    """
        Function to interpret cell magic "line" string as Python parameters (positional and keyword) 
        separated by spaces instead of commas
    """
    
    def _line_to_parameters(ssh_conn="dummy", ssh_psw="dummy", **kwargs):
        """
        helper function
        """

        if ssh_conn =="dummy":
            # if no ssh connection given then take it from global
            global _ssh_conn
            if _ssh_conn:
                ssh_conn=_ssh_conn
            else:
                raise Exception('Error! ssh_conn is not given.')
        
        if '@' in ssh_conn:
            user = ssh_conn.split('@')[0]
            host = ssh_conn.split('@')[1]
        else:
            raise Exception('Error! First line magic parameter should be in the form of user@host')

        if ssh_psw =="dummy":
            # if password not given then take it from global
            global _psw
            if _psw:
                ssh_psw=_psw
            else:
                raise Exception('Error! ssh password is not given.')
            
        #print(ssh_conn, user, host, ssh_psw, kwargs)
        return ssh_conn, user, host, ssh_psw, kwargs
   
    
    
    if len(line)>0:
    
        #
        # convert line from space-delimeted into comma-delimeted to mimic Python function parameter list
        #
        
        
        # replace spaces with commas, except when space is enclosed in single or double quotes
        #
        
        # pattern finds either single quoted substring, double quoted substring, or space 
        pat=re.compile(r'([\'][^\']*[\'])|(["][^"]*["])|\s+')
        
        # lambda in sub returns single/double quoted substring if it was found, otherwise returns comma
        args_str = re.sub(pat, lambda x: x.group(1) if x.group(1) else x.group(2) if x.group(2) else ", ", line)
        
        #print(args_str)
    
        # at this point args_str is comma-delimeted
        # first argument is connection; surround it with quotes to make it a string parameter
        # But it may be a keyword, in which case do not surround.
        if ',' in args_str and '=' not in args_str[ : args_str.find(',') ] :
            args_str = '"' + args_str[ : args_str.find(',') ] + '"' + args_str[ args_str.find(',') :]
        elif '=' not in args_str:
            args_str = '"' + args_str + '"'
        
        # parse args_str as parameters 
        #
        parse_call_str="_line_to_parameters(" + args_str + ")"
        #print(parse_call_str)
        return eval(parse_call_str)
        
    else:
        # parameter line was empty
        return _line_to_parameters()
    
def _add_oracle_env_variables(script, oracle_sid):
    """
        add Oracle environment setup to script
    """
    #script1= (f"newgrp oinstall\n"
    script1= (f"export ORACLE_SID={oracle_sid}\n"
              f'if [[ "`uname -s`" == "Linux" ]]\n'
              f"  then ORATAB=/etc/oratab\n"
              f'elif [[ "`uname -s`" == "AIX" ]]\n'
              f"  then ORATAB=/etc/oratab\n"
              f'elif [[ "`uname -s`" == "SunOS" ]]\n'
              f"  then ORATAB=/var/opt/oracle/oratab\n"
              f"fi\n"
              f"export ORACLE_HOME=`cat $ORATAB | egrep -v '^#' | grep -- $ORACLE_SID | cut -d: -f2 | head -1`\n"
              f"export ORACLE_BASE=`echo $ORACLE_HOME | sed 's@/product.*$@@'`\n"
              f"PATH=$ORACLE_HOME/bin:$PATH\n"
              f"export LD_LIBRARY_PATH=$ORACLE_HOME/lib:$LD_LIBRARY_PATH\n"
             f"{script}")

    return script1

             #f"export ORACLE_HOME=`cat $ORATAB | grep $ORACLE_SID | cut -d: -f2`\n"


def _substitute_notebook_variables(script):
    """
      Substitute any Notebook variables inside not escaped curly braces.
      If curly braces were escaped with backslash then remove backslash.
      get_ipython().user_ns[] gives variable value
      
    """
    #
    # Substitute any Notebook variables inside not escaped curly braces.
    #
    ip=get_ipython()
    script1=re.sub(r"(?<=[^\\]){[^\\]*?}",
                   lambda x: ip.user_ns[x.group(0)[1:-1]],
                   script,
                   flags=re.MULTILINE)
    #
    # if curly braces were escaped with backslash then remove backslash
    #
    script2=re.sub(r"\\([{}])",
                   "\\1",
                   script1)
    return script2
   
def _substitute_single_quote(script):
    """
      Escape any single quote within script with sequence '\'' (quote-backslash-quote-quote)
      because "script" will be echo'ed in single quotes:
            echo '{script}' | pbrun su oracle -c 'bash -s'
    """
    script1=re.sub(r"'",
                   r"'\''",
                    script)
    return script1

def _remote_execute_stream_output(host, user, psw, cmd):
    #
    # establish connection
    #
    
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, 22, user, psw)
    #except (paramiko.SSHException, gaierror, TimeoutError, paramiko.ssh_exception.NoValidConnectionsError) as e:
    except Exception as e:
        logger.error(f"AuthenticationException: {e}")
        ssh.close()
        return f"AuthenticationException: {e}"

    #
    # execute remote_script and stream output
    #
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
    except Exception as e:
        logger.error(f"Error in ssh.exec_command ! {e}")
    
    while True:
        while stdout.channel.recv_ready():
             line = stdout.readline()
             print(line.replace("\n",""), flush=True)
       
        if stdout.channel.exit_status_ready():
            lines=''.join(stdout.readlines())
            print(lines, flush=True)
            break
            
        # sleep to save on CPU
        sleep(0.2)
    #
    # append stderr after stdout
    #
    errlines=stderr.readlines()
    # remove two unexplainable errors 
    err=''.join([l for l in errlines if 'shell-init: error retrieving current directory' not in l
                                             and 'Command caught signal 15 (Terminated)' not in l])
    print(err, flush=True)
    
    ssh.close()
    
def _remote_execute_fn (host, user, psw, cmd, stderr_after_stdout=False):
    #
    # establish connection
    #
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, 22, user, psw)
    #except (paramiko.SSHException, gaierror, TimeoutError, paramiko.ssh_exception.NoValidConnectionsError) as e:
    except Exception as e:
        logger.error(f"AuthenticationException: {e}")
        ssh.close()
        return f"AuthenticationException: {e}"
    #
    # execute remote_script
    #
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
    except Exception as e:
        logger.error(f"Error in ssh.exec_command ! {e}")       

    outlines=stdout.readlines()
    out=''.join(outlines)
    logger.debug(out)
    
    errlines=stderr.readlines()
    # remove three unexplainable errors 
    err=''.join([l for l in errlines if 'shell-init: error retrieving current directory' not in l
                                             and 'Command caught signal 15 (Terminated)' not in l
                                             and 'Cannot access sharedlibsolarisprojects /usr/lib/libproject.so.1' not in l
                                             ])
    #err=''.join([l for l in errlines ])
    ssh.close()
    
    #if err and not stderr_after_stdout:
    if err:
        logger.error(out+err)
    
    if stderr_after_stdout:
        # append stderr after stdout
        return out+err
    else:
        return out

    # below if we want to stream output via returned generator
    # (but see how streaming is done in _remote_execute_stream_output, as it uses sleep to save on CPU)
    #while True:
    #    if stdout.channel.recv_ready():
    #        line = stdout.readline()
    #        yield line.replace("\n","")
    #
    #    if stdout.channel.exit_status_ready():
    #        if stdout.channel.recv_ready():
    #            lines=''.join(stdout.readlines())
    #            yield lines
    #        ssh.close()
    #        break
