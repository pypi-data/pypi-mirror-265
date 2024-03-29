'''
    This module defines Jupyter Notebook "cell magic" to execute a sqlplus script in a remote shell.
    The sqlplus will be executed on a remote Unix after looging in and becoming oracle account via pbrun.
    The cell content is expected to be a valid sqlplus script.
    
    A Remote ssh connection is established using password either passed as a parameter on the command line, or preliminary set in initialization.
    Once connected, a sqlplus is executed via pbrun as oracle run user, and cell content is fed to sqlplus via "here doc" construct.

    Normal Oracle environment variables like ORACLE_HOME etc are set up according to SID passed as a parameter.
    
    The pbrun infrastructure and permissions on remote server are assumed to have already been set up.
    
    The cell magic will stream output back to Jupyter Notebook.
    
    Usage examples: 
    
        In: %%pbrun_sqlplus user@host ssh_psw=password1 oracle_sid=ORCL1 oracle_conn="/ as sysdba"
    
            select sysdate from dual;
    
    
    As regular python function. 
    The function does not stream output, i.e. output does not appear until script finishes.
    
        from pbrun_sqlplus import pbrun_sqlplus_fn
        shell_cmd="""
            select sysdate from dual;
        """
        out=pbrun_sqlplus_fn("user@host password ORACLE_SID ORACLE_CONN", sqlplus_cmds)
'''

import re
from IPython.core.magic import (register_cell_magic, needs_local_scope)
from IPython.display import Javascript, display

# import common functions
from . import nbrshell_common as cmn


@register_cell_magic
def pbrun_sqlplus(line, script):
    """
        This is a multiline cell magic function.
        It executes cell content via sqlplus on a remote host, after connecting to the remote host with ssh, 
        becoming oracle with pbrun and setting some common Oracle environment variables (ORACLE_SID, ORACLE_HOME, PATH).
        
        It uses paramiko as ssh client with password authentication so that prior key setup is not needed.
        
        Parameter "line", if present, should be in the form of "user@host psw=<ssh_password> oracle_sid=<sid> oracle_conn=<connection string> [debug=True]`" 
        If "line" not present, then it is assumed that all parameters have been previously set with set_nbrshell_env
        Parameter "debug" is optional.

        Usage example 1:
        
            import nbrshell as nbr
            nbr.set_nbrshell_env(ssh_conn=<user@host>,
                    ssh_psw=<ssh_password>,
                    oracle_sid=<sid>,
                    oracle_conn=<oracle_conn>)
            
            %sqlplus
            select * from dual;

            %sqlplus
            select host_name, instance_name from v$instance;
        
        Usage example 2:
        
            %sqlplus conn=<user@host> psw=<password> oracle_sid=<sid> oracle_conn=<connection string>] [debug=True]
            select * from dual;
        
        If "debug" is given then it will print shell script text after performing all substitutions
        and before sending it for remote execution.
        
        Substitutions performed prior to sending script for remote execution: 
        
            - substituting any Notebook variable inside curly braces.
              Therefore if any curly brace is part of the shell script, it needs to be backslash escaped.
            
            - adding sqlplus here doc construct:
                    sqlplus -s -l {oracle_conn} <<-EOF
                            {script}
                    EOF
            - adding ORACLE environment variables 
            
            - escaping single quotes. This is necessary because the script is sent for remote execution using below construct:
                    "cd /tmp; echo '{script}' | pbrun su {pbrun_user} -c 'bash -s'"
              Single quotes inside "script" are substituted with "quote-bakslash-quote-quote" sequence.
              Example: "select 'aaa'" becomes "select '\''aaa'\''"
              
    """

    # parse parameters
    conn, user, host, psw, kwargs = cmn._parse_str_as_parameters(line)

    oracle_sid = kwargs.get('oracle_sid', "dummy_sid")
    if oracle_sid =="dummy_sid":
        if cmn._oracle_sid:
            oracle_sid=cmn._oracle_sid
        else:
            raise Exception('Error! oracle_sid is not given.')    
       
    # if oracle_sid was not passed then get it from global
    oracle_sid = kwargs.get('oracle_sid', "dummy_sid")
    if oracle_sid =="dummy_sid":
        if cmn._oracle_sid:
            oracle_sid=cmn._oracle_sid
        else:
            raise Exception('Error! oracle_sid is not given.')    
    
    # if oracle_conn was not passed then get it from global
    oracle_conn = kwargs.get('oracle_conn', "dummy_conn")
    if oracle_conn =="dummy_conn":
        if cmn._oracle_conn:
            oracle_conn=cmn._oracle_conn
        else:
            raise Exception('Error! oracle_conn is not given.')    
    
    # debug default is False
    debug = kwargs.get('debug', False)
    
    #print(conn, user, host, psw, oracle_sid, debug, kwargs)
    
    # substitute notebook variables
    script1 = cmn._substitute_notebook_variables(script)
    
    # add sqlplus here doc
    script2 = _add_sqlplus_here_doc(script1, oracle_conn)

    # add oracle env variables
    script3 = cmn._add_oracle_env_variables(script2, oracle_sid)
    
    # substitute single quotes
    script4 = cmn._substitute_single_quote(script3)
        
    # form pbrun script 
    cmd=f"cd /tmp; echo '{script4}' | pbrun su oracle -c 'bash -s'"
        # alternatively:
        #   cmd=f"echo $'{script3}' | pbrun -u oracle bash -s"
        #       -- this sets uid to oracle, but not group
        #       -- on Solaris group can be set newgrp in the script
        #       -- but on Exadata with Oracle Linux newgrp does not change group
        #       -- therefore this syntax can not be used there
        #       -- Instead "pbrun su - oracle 'bash -s'" is used, since it sets both uid to oracle and group to oinstall
        #
        # alternatively:
        #   cmd=(f"pbrun -u oracle bash -s <<-EOF\n"
        #        f"{script3}\n"
        #         "EOF")
        #

    # print the final script for debugging
    if debug:
        print(f"Executing script on {conn}:")
        print("======== script-start ============")
        print(cmd)
        print("========= script-end =============")
   
    # add html element with id="id_pbrun_sqlplus" for CSS to pick up
    #display( Javascript('element.setAttribute("id", "id_pbrun_sqlplus")') )

    # set black background 
    cmn._set_output_cell_black_background()

    # remote execute
    cmn._remote_execute_stream_output(host, user, psw, cmd)


def _add_sqlplus_here_doc(script, oracle_conn):
    """
        add sqlplus here doc construct
        escape dollar sign
    """
    #script1= (f"newgrp oinstall\n"
    script1= (f"sqlplus -s -l {oracle_conn} <<-EOF"
              f"{script}"
              f"EOF")
    script2=re.sub(r"\$",
                   r"\\$",
                    script1)
    return script2
