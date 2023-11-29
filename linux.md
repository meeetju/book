# Linux cheat sheet

## Shells

Check shell
```console
echo $SHELL
```

### zsh

Check if `zsh` is installed
```console
zsh --version
```

Install `zsh`
```console
sudo apt-get install zsh
```

Change shell to `zsh`
```console
chsh -s $(which zsh)
```
- For the change to take effect, must logout
- During first run, select `(2)` when prompted

`zsh` configuration files consist of:
- `.zshenv` - should contian only environment variables
    - note that there is also `/etc/zsh/zshenv` or `etc/zshenv` file
- `.zprofile` - commands executed on shell login
    - note that there is also `/etc/zsh/zprofile` or `/etc/zprofile` file
- `.zshrc` - is sourced in interactive shells, contains configurations and commands: aliases, key bindings, variables, functions
    - note that there is also `/etc/zsh/zshrc` or `/etc/zshrc` file

---
####
.zshrc
####
---

`alias` keyword do define some command. The example below shows a command `myip` which will echo the obtained ip.
```
alias myip="curl http://ipecho.net/plain; echo"
```
- Terminal must be restared in order for changes to take place

####
tips
####

`autocomplete` is set by
```console
autoload -Uz compinit
compinit
_comp_options+=(globdots)
```



---
###
.zshenv
###
---
Updating the path
```console
export PATH="$HOME/.local/bin:$PATH"
```
Or
```console
path=("$HOME/.local/bin" $path)
```

We can also link another config file from other files
```console
. "$HOME/.zshenv_my_custom_file"
. "$HOME/.cargo/env"
```

## Users

### Give Sudo privileges to a User

- Execute

        sudo visudo

- Modify the file at the bottom

        <user> ALL=(ALL) ALL

    Or depending on how the `root` is defined

        <user> ALL=(ALL:ALL) ALL

## Navigation

---
### Key shortcuts
---
Jump to start of line (home)

```
CTRL + A
```

Jump to end of line (end)

```
CTRL + E
```

Delete previous word

```
CTRL + W
```

Delete previous whole text

```
CTRL + U
```

Delete text to end of line

```
CTRL + K
```

Paste previously deleted text

```
CTRL + Y
```

---
### Paths
---
Relative paths start without "/", so it starts in current directory

go to home directory
```
cd
```

root directory
```
/
```

So it the dir name starts without any sign it means that the dir is searched in current directory
```
find Downloads -name '*.deb'
```

current directory
```
.
```

If we want to specify the current directory using relative path we can use
```
find ./Downloads -name '*.deb'
```

one level up directory
```
..
```

```
pwd
/dir1/dir2
cat ../dir1/some_dir1.json
{"some": "body"}
```
- pwd - print working directory

one level down from directory

```
pwd
/dir1
cat ./dir2/some_dir2.json
{"some": "body"}
```

---
### Parenthesis
---

Single parethesis : `''` makes the literal not be interfered by the shell. 
```
echo '$PATH'

output:
'$PATH'
```

Double parethesis : `""` makes the literal to be interfered by the shell. 
```
echo "$PATH"

output:
home/mati/.cargo/bin:/usr/local/sbin
```

---
### Names globbing
---
Any amount of signs
```
*
```
Display all files names in directory
```
echo *
```
Display all files names staring with "at"
```
echo at*
```
Display all files names endinging with "csv"
```
echo *csv
```
Display all files with "some_pattern" inside name
```
echo *some_pattern*
```
All folders and files consisting a dot
```
echo *.*
```
Any sign with "?"

Display all files with "some?pattern" inside name
```
echo *some?pattern*
```
## Commands

See also: https://www.tutorialspoint.com/unix/index.htm

---
### Display
---
`which` displays the executable location
```
which zsh

output:
/usr/bin/zsh
```

Read files content
```
cat file1 file2 ...
```

Read folder content (For detailed flags use --help)
```
ls
```

Read content of a given folder
```
ls <FOLDER>
```


Print to standard output
```
echo some text to output
```

Compare files
```
diff file1 file2
```

Check file type
Compare files
```
file file1
```

Display with portions (for large files)
```
cat some_huge_file | less
```
- `space` - next page, `b` - previous page, `q` - break

Find file(s) in directory
```
find /users/me -name '.zsh[a-z_]*' | sort
find /home/mati -name '*bash*'
```

Find file(s) in current directory which name consists
```
find . -name '*bash*'
```

Find entires in files in /etc/passwd that consist a phrase which starts with `r` and ends with `t`
```
grep 'r.*t' /etc/passwd
```

Find in Downloads directory all files with .deb extension
```
find Downloads -name '*.deb' 
find ./Downloads -name '*.deb'
```

- remember that with the "name" the "*" must be escaped with putting the pattern in quotes

Find files which paths contain pattern / paths that do not contain "sessions"
```
find .zsh[a-z_]*
find .zsh[a-z_]* | grep -v sessions
```

Display first 10 rows of a file
```
head file1
```

Display last 10 rows of a file
```
tail file1
```

Sort displayed rows
```
cat file1 | sort
cat file1 | sort -r
```
- `-r` reversed

Display help for commands (here ls)
```
man ls
```

Display help using a searched key_word
```
man -k key_word
```

---
### Grep
---

Prints rows from file(s) or input stream that contain phrase
```
grep phrase /path/to/file
```

Prints files names and rows that contain a phrase
```
grep -r phrase path/to/dir/*
grep -r "some longer phrase" path/to/dir
```
- `-i` ignores letters size 
- `-v` prints the rows that do not contain the phrase
- `-r` recursive to include files and subfolders

---
### Regular expressions
---

https://regex101.com/


---
### Redirecting
---

Redirect output of some commang from consolde to a file 
```
command > file
```
- use `>>` to append to file without erasing the previous content

Redirect from file to command (hear "head")
```
head < file
```
- usually the `<` is not required as this behaviour is default for many commands

---
### Pipes
---

Redirect the output of one command to other command input
```
cmd1 | cmd2
```

---
### Copy file(s)
---
Copy file1 to file2 
```
cp file1 file2
```

Copy files to folder
```
cp file1 file2 ... folder1
```

Copy whole directory 
``` 
cp -R source_dir destination_dir
```

Copy only the content of directory to another directory
```
cp -R source_dir/* destination_dir
```

---
### Move file(s)
---
Rename file
```
mv file_old_name file_new_name
```

Move file(s) to folder
```
mv file1 file2 ... folder1
```
---
### Files crud
---
Create file
```
touch file1
```

Remove file
```
rm file1
```
---
### Directories crud
---
Create directory
```
mkdir dir1
```

Delete directory
```
rmdir dir1
```

Delete directory with files and folders recursively
```
rmdir -rf dir1
```
- `-r` recursively
- `-f` force

---
### Password
---

To change password
```
passwd
```

---
### Shell
---

Adding and reading shell variable
```
STUFF=blabla
echo $STUFF
```

Moving shell variable to env variables
```
export STUFF
``` 

---
### Env variables
---

add to `PATH` at front for terminal lifetime
```
PATH=/new/location:$PATH
```

add to `PATH` for terminal lifetime
```
PATH=$PATH:/new/location
```

---
### General
---

Read current processes - PIDs
```
ps
```
- `w` - with commands
- `x` - processes started by actual user
- `ax` - all processes
- `u` - detailed data

Read data of a specific PID
```
ps wu PID
```

Kill PID
```
kill PID
```

Stop and restore PID
```
kill -STOP PID
kill -CONT PID
```

Ctrl + C
```
kill -INT PID
```

Ctrl + Z freezes the process, to run again we use "fg" or "bg"

---
### Permissions
---
To see permissions use:
```
ls -l
```
```
-rwxrw-r--
```
- first `-` means this is a simple file, `l` means it is a link
- `rwx`: user permissions read write execute
- `rw-`: group permissions read write, no execute
- `r--`: other users permissions read, no write no execute

Set write permission for other users and group
```
chmod og+w file
```

Set permissions with numbers
```
chmod 777 file
```
- 4: read
- 2: wrtie
- 1: execute

Set prmissions with +notation
```
chmod +x some_executable
```

---
###
Compression
###
---

## 
gzip
##

A file that contain .gz extension

Unpack
```
gunzip file.gz
```

Pack
```
gzip file
```

##
tar
##

To compress archives .tar extension

Create archive
```
tar cvf some_archive.tar file1 file2
```
- `c` : creating archive
- `v` : verbosity
- `f` : enable providing file name

Unpack from archive
```
tar xvf some_archive.tar
```
- `x` : unpack
- `t` : investigate
- `p` : keep same permissions like in archive

##
tar.gz / tgz
##

First we have to unpack gz and then tar.

We can do this also using zcat

```
zcat my_archive.tar.gz | tar xvf -
```

---
###
File system
###
---
https://www.pathname.com/fhs/pub/fhs-2.3.html

- /
    - bin/ [binary executables]
    - dev/ [devices files]
    - etc/ [cofig files, like netplan for eth]
    - usr/ [structure consists of part of the same type of files]
        - bin/
        - man/
        - lib/
        - local/
        - sbin/
        - share/
    - home/ [personal user files]
    - lib/  [libraries used by executables]
    - sbin/ [system binary executables]
    - tmp/
    - var/  [here programs write data, logs while working]
        - log/
        - tmp/
    - media/ [external disks]
    - opt/   [third party software]

---
###
Superuser
###
---

Use
```
sudo command
```
Or just log as super user
```
su
command
```

---
###
Networks
###
---

Display active IP addresses
```
ifconfig
```

Display routing
```
route
```
- `-n` presents destination ip instead of names

File /etc/hosts consists of names and addresses used during search.

---
###
Shell scripts
###
---
Remember to chmod +x to be abele to execute the sh file.

All shell scripts should start with
```console
#!/bin/sh
```

Scipts may use positional arguments

Let's have a sh file which consists of
```
echo $1
echo $2
```
So execution like this
```
./my.sh lol rotfl

output:
lol
rotfl
```

Output code is in `$?` variable. In custom script we return the code
using the exit.

```
exit 1
```
means that there was an error of code 1.

if-else-elif-fi with the unix program that does the test for conditionals: `[]`

```
#!/bin/sh
if [ "$1" = "lol" ]; then
    echo 'first param was lol'
elif [ "$2" = "rotfl" ]; then
    echo 'second parameter was rotfl'
else
    echo 'there was no first lol and second rotfl' 
    echo it was $1 and &2
fi
```

Test `[]` may be replaced with the `test`
```
if test "$1" = "lol" ; then
    echo 'first param was lol'
elif test "$2" = "rotfl" ; then
    echo 'second parameter was rotfl'
else
    echo 'there was no first lol and second rotfl' 
    echo it was $1 and $2
fi
```




Test `[]` may be replaced with the `grep` test
```
if grep -q daemon /etc/passwd; then
        echo there is a daemon user password
else
        echo there is no dameon  
fi
```

AND condition `&&`

```
if [ "$1" = hello ] && [ "$2" = friend ]; then
    echo 'Done, both contidions met'
fi
```

OR condition `||`

```
if [ "$1" = hello ] || [ "$2" = hi ]; then
    echo 'Done, one of conditions met'
fi
```

Files testing

```
[ -parameter file]
```
- -f : is a regular file (expect 0)
- -d : is a directory (expect 0)
- -e : file exists (expect 1)
- -s : is file empty (expect 1)
- -r : is file readable (expect 0)
- -w : is file writeable (expect 0)
- -x : is file executable (expect 0)

Math comparisons
```
a=10
b=20

if test "$a" -lt "$b"
then
	echo "a is less then b"
fi
```
- `-eq`
- `-ne`
- `-lt`
- `-gt`
- `-le`
- `-ge`

Compare text with `case` 
```
case $1 in
seeya)
	echo seeya was said
	;;
yello|hello|hi)
	echo kind of hello was said
	;;
*)
	echo something else was said
	;;
esac
```

`for` loop
```
for str in one two three; do
	echo $str
done

output:
one
two
three
```

`while` loop  
Commands are put in `` qotes, here command result is stored in a, and later used in script as $a 
```
#!/bin/sh

a=0

while [ $a -lt 4 ]
do
   echo $a
   a=`expr $a + 1`
done

output:
0
1
2
3
```

`awk` is a language to work on data in shell, this takes the output
of `ls -l` and prints only the first collumn of each entry
```
ls -l | awk '{print $1}'

output:
total
-rw-r--r--
-rwxrwxr-x
-rwxr-xr-x
-rwxrwxr-x
```

`sed` is a stream editor

`sed` may take regular expression and text, so let's say we have a file named `my_passwords` that consists of:
```
pass1: "lol"
```
if we use command below, the output stream will be changed, comparing to the file content:
```
sed 's/:/%/' my_passowrds

output:

pass% "lol"
```

`sed` may also work on addresses, so let's say we have a file named `text` that consists of:
```
first
second
third
fourth
fifth
sixth
```
if we use comand below, it will remove rows from 2nd to fifth, comparing to the file content:
```
sed 2,5d text

output:
first
sixth
```

`xargs` - runs command for each parameter from input stream

Here `xargs` will run creation of three directories named d1, d2 and d3
```
echo 'd1 d2 d3' | xargs mkdir

ll

output:
d1/
d2/
d3/
```
`xargs` with `-t` option makes the command visible
```
echo 'c1 c2 c3' | xargs -t rm -rf

output:
rm -rf c1 c2 c3
```
`xargs` to remove all git branchses that match regex
```
git branch | grep "some-branch-name-part" | xargs git branch -D
```

`expr` is for executing math operations or operations on strings
```
expr 1 + 2

output:
3
```

`exec` changes current process to a program provided, but after `ctrl+c`/`ctrl+d` the previous process (like terminal) is terminated

To run scripts from our script we use `.`

Let's say we have a `scrip1.sh` that does something and we use `script2.sh` to run the first one as a part of the functionality. So the `script2.sh` looks like this:
```
echo "I will now run first script"
. script1.sh
echo "First script was executed"
```

`read` to read one row of input, let's print out what the user provided to the terminal, so we have a file `read_input`:
```
read some_input
echo see this $some_input
```
if we execute it and later on provide an input, we will se this
```
./read_input

input:
lol

output:
see this lol
```

## Usefull applications

### apt-get


`apt-get` is a command line tool for interacting with the Advanced Package Tool (APT) library (a package management system for Linux distributions). It allows you to search for, install, manage, update, and remove software

To resynchronize the package index files and update the package repository to the latest version
```console
apt-get update
```
- This ensures that the packages you install are up-to-date

Upgrade a specific package by running
```console
apt-get upgrade [package_name]
```

Installing packages
```console
apt-get install [package_name]
```

To remove package with all config files
```console
apt-get purge [package_name]
```

## Useful packages

In order to avoid future problems install

    sudo apt-get install pkg-config libssl-dev


## Instalation guidelines

### VSCode

[Docs](https://code.visualstudio.com/docs/setup/linux)

> Note: Use the terminal approach so that the `code` is added automatically to path

## Linux alongside Windows

- Installation

    [Istallation guidelines](https://www.fosslinux.com/50836/install-linux-mint-alongside-windows.htm)

- Make Windows default on ubuntu boot GRUB

        sudo grep menuentry /boot/grub/grub.cf

    Save the: 
    
        `Windows Boot Manager (on /dev/nvme0n1p1)`

- Edit the GROB config

        sudo nano -B /etc/default/grub

    And set the line:

        GRUB_DEFAULT="Windows Boot Manager (on /dev/nvme0n1p1)"

- Apply changes

        sudo update-grub
