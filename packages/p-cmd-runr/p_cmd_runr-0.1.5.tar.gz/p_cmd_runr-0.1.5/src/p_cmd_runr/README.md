# Introduction

The p_cmd_runner package was born from the need to run local commands (taken from local files) on any number of remote nodes accessible via SSH(/AMOS/MOSHELL).
It is written in Python 3, and is based on the Paramiko package.

As of **version 0.1.0**, SSH security key files are supported as an alternative to password authentication.
See this [tutorial](https://phoenixnap.com/kb/setup-passwordless-ssh) on how to setup your SSH security key files.
In general, you would generate public and private key-pair(s) on your local machine, then transfer the public key(s) to your remote node(s).

### To install the package:
**python -m pip install p_cmd_runr**


### The p_cmd_runr package provides access to:
- an API composed of a ConfigGrabber class, a CmdRunner class, a main function called boxjumper, and other utility functions.
- the gp_cmd_runr a general purpose command runner script.

Whether you will be implementing your own script with the help of the API, or running the gp_cmd_runr script, you will have to provide 2 types of files:
- at least one configuration file stating which nodes to access, their login information, along with references to the files containing the commands to run on those nodes.
- at least one command file containing the commands you would normally run on the above node(s).


# The Main API Classes And Functions

The **ConfigGrabber** class creates an iterator type object. You provide it with the filename of your local configuration file.
```
__init__(self, filename="config.txt", separator="=", comment="#", mvs=",", delay="0", cmd_timeout="0.5", prompts="$#?<>")
        Description:
            Initializer of a ConfigGrabber object.
            Reads a configuration file and makes available a dictionary of key-value pairs taken from that configuration file.
        Parameters:
            - Filename specifies the name of the configuration file to process.
            - separator defines the character or string used as separator between key-value pairs.
            - comment defines the character or string used for line comments.
            - mvs (or multi-value seperator): defines the character or string that seperates multiple values.
            - delay pause time (in seconds) before running the next command.
            - cmd_timeout maximum time (in seconds) to wait for a command to finish executing.
            - prompts string of characters representing command line prompts.
        Returns:
            ConfigGrabber object (which contains the jumpboxes used by the boxjumper function).
```


The **CmdRunner** class creates an object that logs into a node *jumpbox-style* and runs commands taken from cmd_file. It outputs the results in log_file.
```
__init__(self, jumpbox, node, cmd_file, log_file, blocking, key_file=None)
        Description:
            Initializer of CmdRunner object.
        Parameters:
            - jumpbox defines parameters needed to login to node.
            - node hostname or IP address of the node.
            - cmd_file file containing the commands to execute on node.
            - log_file name of file in which activity is logged. If log_file is not given, a log file will be created.
            - blocking determines whether to block and wait for a command to finish executing.
            - key_file optional SSH security key file.
        Returns:
            CmdRunner object.
```


The **boxjumper** function internally creates CmdRunner objects from jumpboxes, and recursively logs into those boxes/nodes. If commands happen to be defined for a node, they are executed.
```
boxjumper(jumpboxes, count, fp=None, channelstack=None, print_output=False, blocking=True)
    Description:
        boxjumper recursively logs into the boxes/nodes defined in jumpboxes.
        And optionally executes the commands for the current node if it's defined.
    Parameters:
        - jumpboxes list of jumpbox objects (contained within a ConfigGrabber object).
	- count number of jumpboxes.
        - fp boxjumper's log file pointer.
        - channelstack optional channel created by the previous node (if there was a previous node).
        - print_output determines whether or not to print command output on the screen.
        - blocking determines whether to block and wait for a command to finish executing.
    Returns:
        fp boxjumper's log file pointer.
```


## A Very Simple Example On How To Use The API
``` 
from p_cmd_runr.p_cmd_runr import ConfigGrabber
from p_cmd_runr.p_cmd_runr import boxjumper

# your local configuration file
filename="config.txt"
# parse the configuration file and create a ConfigGrabber object, which contains one or more jumpboxes and their associated parameters
cfo = ConfigGrabber(filename)
# boxjumper will create a CmdRunner object from each jumpbox contained in cfo, and use the CmdRunner objects to remote into its corresponding node and optionally run commands on it.
fp = boxjumper(cfo, len(cfo))
if fp:
	fp.close()
```


For more information on other functions and class methods, load the package and use the Python help() function to inspect them, or check the [source code](https://github.com/kaiyoux/p_cmd_runr).


# How To Use The gp_cmd_runr Script 

The gp_cmd_runr script is a general purpose and flexible means of automatically running commands remotely on one or more service node(s) using SSH(/AMOS/MOSHELL).
It allows you to jump from node to node, with the option of running commands on each node.
**PLEASE MAKE SURE THAT YOU MANUALLY TEST THE COMMANDS ON THE INTENDED NODE(S) BEFORE RUNNING THEM 
AUTOMATICALLY WITH THIS SCRIPT.**


The script is controlled by one or more configuration files. See Definitions and the Example Configuration Files section below to have an idea on how to write your own configuration file(s).


### Prerequisite (skip this if the p_cmd_runr package install was successful):
1. Install the latest version of python 3 from https://www.python.org/ if you don't already have it.
For Windows users, during the python installation, make sure that the option to add the location of the python executable to your Windows PATH environment variable is selected.

2. Install the paramiko package by doing the following: (This should not be necessary, because installing the p_cmd_runr package should install all dependancies such as Paramiko)
	1. Open a console or command prompt. For Windows users, Right click on Windows PowerShell (or CMD prompt) and select Run as Administrator. (If Run as Administrator does not work, try using the regular mode.)
	2. Type the following 2 commands: 

**python -m pip install –upgrade pip**

and

**python -m pip install –upgrade paramiko**

or

**python -m pip install -r requirements.txt**


### To run the scrpit:
**python -m gp_cmd_runr [-h] [-d] [-t] [-p] [-r|-n|-f] [-c CONFIG1 [CONFIG2 ...] ]**
```
general purpose command runner

optional arguments:
  -h, --help            show this help message and exit
  -d, --dry_run         display loaded configuration, but do not execute
  -t, --timeout         sets command execution to non-blocking. default is blocking
  -p, --print_output    flag to print command output to the screen. default is not to print
  -r, --raw		no manipulation of output file(s)
  -n, --normal		remove duplicate '\n' between lines in output file(s). this "normal" appearance is the default behavior
  -f, --flatten		only have output file(s) containing a single '\n' between lines
  -c CONFIG1 [CONFIG2 ...], --config CONFIG1 [CONFIG2 ...]
                        list of one or many configuration files. default is config.txt
```


# Definitions
```
# This defines the structure of a configuration file.
# # character is a comment
# [] encloses an optional entry or block of entries
# <> value to specify. Note that the terms file, filename and filepath within <> are synonymous

[
# optional jumpboxes. these are potentially intermediary nodes, and can only be accessed through ssh
# example: ssh [-i key_file] [username@]node [-p port]
# jumbox1
jump_cmd = ssh
node = <node>
[username = <username>]  # will be prompted if not provided
[
[
[key_file = <ssh security key file>]  # will not be prompted if not provided. this would usually be a private key file on your local machine
[passphrase = <passphrase of key_file>]  # if your private key file was created with a passphrase for additional security, you will have to specify it here. Note that this entry is optional if you are not using a passphrase
]
# or
[password = <password>]  # will be prompted if not provided. meaningless if key_file is provided
]
[port = <port number>]   # specify a custom ssh port number. default is 22
[cmd_file = <filepath>]
[log_file = <log filename>]
[delay = <pause time before running next command>]  # defaults to 0 sec
[cmd_timeout = <maximum time to wait for command execution>]  # maximum amount of time to wait (in seconds) for output from a command. it defaults to 0.5 sec. increase this value if you are missing some output. meaningless in blocking mode
[prompts = <string of characters representing prompts on the node>]  # for blocking execution, the script blocks until it detects one of the prompts specified here. default is $#?<> . meaningless in non-blocking mode
end


#jumpbox2
...

#jumpboxN
...
]

# and/or

[
# optional final node(s). these are similar nodes sharing the same login username, the same password (if key files are not used), and understanding the same commands. can either be accessed through ssh or amos/moshell
# the name of each log file will be a combination of its corresponding IP/node name with date and timestamp. 
# Note that if there happens to be a local tmp/ folder, the script will silently move the logs files to that tmp/ folder as a measure to avoid cludder in the working directory
nodes = <comma seperated list of nodes (either node names or IP addresses)>

[
# optional ssh security key files for the above final nodes 
# the first key file is for the secure login to the first node, the second key file to the second node, etc.
# if there are more nodes than key files, the last key file will be used to login to the remaining nodes
# if there are less nodes than key files, the excess key files are ignored
# Note that individual passphrases are not allowed in this section for each final node
key_files = <comma seperated list of ssh security key files>
]

# command files for the above final nodes
# the first command file is run on the first node, the second command file on the second node, etc.
# if there are more nodes than command files, the last command file will be run on the remaining nodes
# if there are less nodes than command files, the excess command files are ignored
cmd_files = <comma seperated list of filepaths>

# defines common parameters for the final nodes
jump_cmd  = amos or moshell or ssh  # examples: amos node or moshell node or ssh [-i key_file] [username@]node [-p port]
[username = <username>]  # mandatory if using ssh. my amos/moshell does not use username
[password = <password>]  # mandatory if using ssh and no key_files have been specified. this password will be used to login on all final nodes. meaningless if key_files are provided. my amos/moshell does not use password authentication
[passphrase = <passphrase for one, some or all key_files>]  # you may define and use a common passphrase for one, all or some of the final nodes/key files. specifying a passcode here for some of the key files will not interfere with the other key files that do not require a passphrase
[port = <port number>]   # specify a custom ssh port number. default is 22
[delay = <pause time before running next command>]  # defaults to 0 sec
[cmd_timeout = <maximum time to wait for command execution>]  # maximum amount of time to wait (in seconds) for output from a command. it defaults to 0.5 sec. increase this value if you are missing some output. meaningless in blocking mode
[prompts = <string of characters representing prompts on the nodes>]  # for blocking execution, the script blocks until it detects one of the prompts specified here. default is $#?<> . meaningless in non-blocking mode 
end
]
```

# Example Confiuration Files
```
# The below configuration will ssh to node 99.99.99.99, and from there ssh to node 88.88.88.88.
# It will run the commands in linux_commands_2.txt on node 88.88.88.88, and save the output in EMM.txt under tmp/ folder.
# Once done, it will backtrack and run the commands in linux_cmds.txt on node 99.99.99.99, and save the output in cubevm.txt.

jump_cmd = ssh
node = 99.99.99.99
username = 
password = 
#cmd_timeout = 0.5
#delay = 0
log_file = cubevm.txt
cmd_file = linux_cmds.txt
end

jump_cmd = ssh
node = 88.88.88.88
username = iTsm3
password = my5ecr3t#Cu8#passw  # yes, you may use '#' characters as part of your password
log_file = tmp/EMM.txt  # note: log file will be placed in tmp folder, if tmp/ exists
cmd_file = linux_commands_2.txt
cmd_timeout = 1
end
```

```
# The below configuration will ssh to 4 nodes: cube5, cube6, 3.3.3.3, cube1. Note that they must all accept the same login username and password credentials.
# It will run the commands in linux2_commands on all 4 nodes and save the output locally in text files named after each node with a date and timestamp.

nodes = cube5, cube6, 3.3.3.3, cube1

cmd_files = linux2_commands

jump_cmd = ssh
username = iTsm3
password = my5ecr3tCu8passw
#delay = 0
#cmd_timeout = 1
end
```

```
# The below configuration will ssh to node 1.2.3.4, and from there amos to node box1, then box3.
# It will run the commands in amos2_commands.txt on box1, run the commands in generic_cmds.txt on box3, and save the output files locally in a text files named after each node with a date and timestamp.
# It will ignore the excess command files: DOES_NOT_EXIST.txt, RANDOM.txt.


jump_cmd = ssh
node = 1.2.3.4
port = 22
username = iTsm3
password = my5ecr3tCu8passw
prompts = $
end

#nodes = box2 
nodes = box1, box3

cmd_files = amos2_commands.txt, generic_cmds.txt, DOES_NOT_EXIST.txt, RANDOM.txt

jump_cmd = amos
#delay = 1
prompts = <>
end
```

```
# The below configuration will ssh to cubeX node using the private key in C:/Users/jd/ssh-keys/id_rsa (which does not require a passphrase),
# and execute the commands in C:/Users/jd/work/commands_to_run_on_cubeX.

jump_cmd = ssh
node = cubeX
port = 2233
username = jane-doe
key_file = C:/Users/jd/ssh-keys/id_rsa  # was not generated with a passphrase
#key_file = C:/Users/jd/ssh-keys/pp_id_dsa  # was generated with the below passphrase
#passphrase = passphrase-for-pp_id_dsa
prompts = $
cmd_file = C:/Users/jd/work/commands_to_run_on_cubeX
end
```

```
# The below configuration will successively ssh to the 2 nodes (aServer and 721.9.0.5) using the private key in pp_id_ed25519, along with passphrase "common_pp*",
# and execute the commands in cmd1 on aServer, and commands in cmd2 on 721.9.0.5.

nodes = aServer, 721.9.0.5
key_files = pp_id_ed25519
cmd_files = cmd1, cmd2, cmd3, cmd4

jump_cmd = ssh
username = admin
passphrase = common_pp*
port = 2222
prompts = $
end
```

```
# The below configuration will ssh to sales node using the private key in id_rsa and execute the commands in cmd1.txt.
# Then ssh to dmz node using the private key in pp_id_rsa, along with its corresponding passphrase "the_passphrase_of_pp_id_rsa", and execute the commands in /home/billy/special/dmz/cmd2.
# And finally, ssh to production node using the private key in id_ed25519, and execute the commands in cmd1.txt.

nodes = sales, dmz, production

key_files = id_rsa, pp_id_rsa, id_ed25519

cmd_files = cmd1.txt, /home/billy/special/dmz/cmd2, cmd1.txt, cmd.txt

jump_cmd = ssh
username = admin
passphrase = the_passphrase_of_pp_id_rsa
port = 2222
prompts = $
end
```

```
# The below configuration will ssh to node 99.99.99.99, and from there ssh to node 88.88.88.88.
# From node 88.88.88.88, it will ssh to nodes cube5, cube6, 3.3.3.3, cube1.
# It will run the commands in linux2_commands.txt on cube5, cube6, 3.3.3.3 and cube1, and save 
# the output locally in text files named after each node with a date and timestamp.
# It will backtrack and run the commands in linux_TEST_commands on node 88.88.88.88, and save the output in EMM.txt under tmp/ folder.
# Once done, it will backtrack and run the commands in linux_cmds.txt on node 99.99.99.99, and save the output in cubevm.txt.

jump_cmd = ssh
node = 99.99.99.99
username = 
key_file = /home/john/.ssh/id_to_login_to_99-99-99-99
cmd_timeout = 10.0
#delay = 0
log_file = cubevm.txt
cmd_file = linux_cmds.txt
end

jump_cmd = ssh
node = 88.88.88.88
username = ITteam
key_file = /home/john/.ssh/id_to_login_to_88-88-88-88
log_file = tmp/EMM.txt  # note: log file EMM.txt as well as the logs from the below nodes will be placed in the tmp/ folder, if it exists 
cmd_file = linux_TEST_commands
cmd_timeout = 1
end

nodes = cube5, cube6, 3.3.3.3, cube1

key_files = /home/john/.ssh/id_to_login_to_cube5, /home/john/.ssh/id_to_login_to_cube6, /home/john/.ssh/id_to_login_to_3-3-3-3_and_cube1

cmd_files = linux2_commands.txt

jump_cmd = ssh
username = admin
#delay = 0
#cmd_timeout = 1
end
```

# Command File Special Notation:

The command file(s) would contain the typical commands that you would run, line by line, while logged in on the remote host(s).
As of **version 0.0.6**, a special notation 

**:<number of seconds>[sS]:** 

can be used in your command files.
The purpose of this special notation is to wait for the output of the previous command that was issued, for which a prompt was returned but the expected output has yet to be received, as it is still being processed and will be returned in a few seconds or minutes.
**Note that this special notation must appear on a seperate line, in order to keep it distinct from your regular commands. Any other command(s) that appear on the same line as this special notation will be ignored.**
```
Examples of valid notations:
:2: (same as :2s: or :2S:) to wait for 2 seconds.
:063: (same as :63: or :63s:) to wait for 63 seconds.

Examples of non-valid notations:
:: (same as :s: or :S:) will be ignored
:5.9: will be ignored
:1m5s: will be ignored, use :65: instead
```

# Limitations/Known Issues:

- Pagination type commands like `more` or `less` will lock after the first output. It is best to avoid such commands.
You may try to run gp_cmd_runr with the -t or --timeout option. This will force the script to send the next command after the delay you specify, which may result in unexpected behavior on the remote node.

- Given that my AMOS/MOSHELL environments do not require login credentials, the script does not provide the option of specifying such login credentials for AMOS/MOSHELL access.




Let me know if you have any questions: <kaiyoux@gmail.com>
