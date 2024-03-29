"""
nbrshell package defines Jupyter notebook "magic" functions to remotely execute shell script typed in a Jupyter notebook cell.
Functions ending with _fn are regular non-magic function equivalents.


Package structure :

    |__ pbrun_as_oracle             |
    |__ pbrun_as_oracle_fn          |--> connects using paramiko ssh client with password (i.e. no prior keys setup is needed)
    |                               |    Then executes pbrun to switch to oracle user and sets oracle environment according to provided "oracle_sid"
                                    |    Then runs provided shell script as oracle account.

    |__ pbrun_as                    |--> connects using paramiko ssh client with password (i.e. no prior keys setup is needed)
    |__ pbrun_as_fn                 |    Then executes pbrun to switch to another user
    |                               |    Then runs provided shell script
    
    |__ exec_shell_script           |--> connects using paramiko ssh client
    |__ exec_shell_script_fn        |    If password is provided, then connects with password and no prior ssh keys setup is needed.
    |                               |    If password is not provided, then attempts to connect with ssh keys.
                                    |    Then runs provided shell script.

    |__ exec_shell_script_ssh       |--> connects using local ssh client with previously setup ssh keys.
    |__ exec_shell_script_ssh_fn    |    Useful in cases when paramiko can not connect
    
    |__ pbrun_sqlplus               |--> runs cell content via sqlplus on a remote host, after connecting to the remote host with ssh, 
                                    |    becoming oracle with pbrun and setting some common Oracle environment variables.

    |__ nbrshell_common             |--> common functions and variables
        |__ set_psw                     |--> saves password in memory for use in subsequent executions
        |__ set_nbrshell_env            |--> saves nbr environment parameters for use in subsequent executions

"""

# import notebook "magic" functions only when I_Python exists.
# check if ipython is available
try:
    get_ipython
except NameError:
    # Not in Jupyter! Do not import.
    pass
else:
    # In Jupyter - import.
    from .pbrun_as             import pbrun_as
    from .pbrun_as_oracle      import pbrun_as_oracle
    from .exec_shell_script    import exec_shell_script
    from .nbrshell_common      import set_psw, set_nbrshell_env
    from .pbrun_sqlplus        import pbrun_sqlplus
       
from .pbrun_as_fn          import pbrun_as_fn
from .pbrun_as_oracle_fn   import pbrun_as_oracle_fn
from .exec_shell_script_fn import exec_shell_script_fn




