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
- For the change to take effect, must logout. Alternatively also edit `~/.bashrc` by adding:

        exec zsh

- During first run, select `(2)` when prompted

`zsh` configuration files consist of:
- `.zshenv` - should contain only environment variables
    - note that there is also `/etc/zsh/zshenv` or `etc/zshenv` file
- `.zprofile` - commands executed on shell login
    - note that there is also `/etc/zsh/zprofile` or `/etc/zprofile` file
- `.zshrc` - is sourced in interactive shells, contains configurations and commands: aliases, key bindings, variables, functions
    - note that there is also `/etc/zsh/zshrc` or `/etc/zshrc` file

#### ohmyzsh

Install

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Set theme in `~/.zshrc`

```bash
ZSH_THEME=af-magic
```

#### .zshrc

`alias` keyword do define some command. The example below shows a command `myip` which will echo the obtained ip.
```bash
alias myip="curl http://ipecho.net/plain; echo"
```
- Terminal must be restarted in order for changes to take place

#### tips

`autocomplete` is set by
```console
autoload -Uz compinit
compinit
_comp_options+=(globdots)
```

### .zshenv

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
        <user> ALL=(ALL:ALL) ALL

## Navigation

### Key shortcuts

Jump to start of line (home)

```text
CTRL + A
```

Jump to end of line (end)

```text
CTRL + E
```

Delete previous word

```text
CTRL + W
```

Delete previous whole text

```text
CTRL + U
```

Delete text to end of line

```text
CTRL + K
```

Paste previously deleted text

```text
CTRL + Y
```

### Paths

Relative paths start without "/", so it starts in current directory

go to home directory
```bash
cd
```

root directory
```text
/
```

So it the dir name starts without any sign it means that the dir is searched in current directory
```bash
find Downloads -name '*.deb'
```

current directory
```text
.
```

If we want to specify the current directory using relative path we can use
```bash
find ./Downloads -name '*.deb'
```

one level up directory
```text
..
```

```console
pwd
/dir1/dir2
cat ../dir1/some_dir1.json
{"some": "body"}
```
- pwd - print working directory

one level down from directory

```console
pwd
/dir1
cat ./dir2/some_dir2.json
{"some": "body"}
```

### Parenthesis

Single parenthesis : `''` makes the literal not be interfered by the shell. 
```console
echo '$PATH'

output:
'$PATH'
```

Double parenthesis : `""` makes the literal to be interfered by the shell. 
```console
echo "$PATH"

output:
home/mati/.cargo/bin:/usr/local/sbin
```

### Names globbing

Any amount of signs
```text
*
```
Display all files names in directory
```bash
echo *
```
Display all files names staring with "at"
```bash
echo at*
```
Display all files names endinging with "csv"
```bash
echo *csv
```
Display all files with "some_pattern" inside name
```bash
echo *some_pattern*
```
All folders and files consisting a dot
```bash
echo *.*
```
Any sign with "?"

Display all files with "some?pattern" inside name
```bash
echo *some?pattern*
```

## Commands

See also: https://www.tutorialspoint.com/unix/index.htm

### Display

`which` displays the executable location
```console
which zsh

output:
/usr/bin/zsh
```

Read files content
```bash
cat file1 file2 ...
```

Read folder content (For detailed flags use --help)
```bash
ls
```

Read content of a given folder
```bash
ls <FOLDER>
```

Print to standard output
```bash
echo some text to output
```

Compare files
```bash
diff file1 file2
```

Check file type
Compare files
```bash
file file1
```

Display with portions (for large files)
```bash
cat some_huge_file | less
```
- `space` - next page, `b` - previous page, `q` - break

Find file(s) in directory
```bash
find /users/me -name '.zsh[a-z_]*' | sort
find /home/mati -name '*bash*'
```

Find file(s) in current directory which name consists
```bash
find . -name '*bash*'
```

Find entires in files in /etc/passwd that consist a phrase which starts with `r` and ends with `t`
```bash
grep 'r.*t' /etc/passwd
```

Find strings excluding the ones containing some pattern

```bash
grep -v 'some-pattern'
```

Find in Downloads directory all files with .deb extension
```bash
find Downloads -name '*.deb' 
find ./Downloads -name '*.deb'
```

- remember that with the "name" the "*" must be escaped with putting the pattern in quotes

Find files which paths contain pattern / paths that do not contain "sessions"
```bash
find .zsh[a-z_]*
find .zsh[a-z_]* | grep -v sessions
```

Display first 10 rows of a file
```bash
head file1
```

Display last 10 rows of a file
```bash
tail file1
```

Sort displayed rows
```bash
cat file1 | sort
cat file1 | sort -r
```
- `-r` reversed

Display help for commands (here ls)
```bash
man ls
```

Display help using a searched key_word
```bash
man -k key_word
```

### Grep

Prints rows from file(s) or input stream that contain phrase
```bash
grep phrase /path/to/file
```

Prints files names and rows that contain a phrase
```bash
grep -r phrase path/to/dir/*
grep -r "some longer phrase" path/to/dir
```
- `-i` ignores letters size 
- `-v` prints the rows that do not contain the phrase
- `-r` recursive to include files and subfolders

### Regular expressions

https://regex101.com/

### Redirecting

Redirect output of some command from console to a file 
```bash
command > file
```
- use `>>` to append to file without erasing the previous content

Redirect from file to command (hear "head")
```bash
head < file
```
- usually the `<` is not required as this behaviour is default for many commands

### Pipes

Redirect the output of one command to other command input
```bash
cmd1 | cmd2
```

### Copy file(s)

Copy file1 to file2 
```bash
cp file1 file2
```

Copy files to folder
```bash
cp file1 file2 ... folder1
```

Copy whole directory 
```bash
cp -R source_dir destination_dir
```

Copy only the content of directory to another directory
```bash
cp -R source_dir/* destination_dir
```

### Move file(s)

Rename file
```bash
mv file_old_name file_new_name
```

Move file(s) to folder
```bash
mv file1 file2 ... folder1
```

### Files crud

Create file
```bash
touch file1
```

Remove file
```bash
rm file1
```

### Directories crud

Create directory
```bash
mkdir dir1
```

Delete directory
```bash
rmdir dir1
```

Delete directory with files and folders recursively
```bash
rmdir -rf dir1
```
- `-r` recursively
- `-f` force

### Password

To change password
```bash
passwd
```

### Shell

Adding and reading shell variable
```bash
STUFF=blabla
echo $STUFF
```

Moving shell variable to env variables
```bash
export STUFF
```

### Env variables

add to `PATH` at front for terminal lifetime
```bash
PATH=/new/location:$PATH
```

add to `PATH` for terminal lifetime
```bash
PATH=$PATH:/new/location
```

### General

Read current processes - PIDs
```bash
ps
```
- `w` - with commands
- `x` - processes started by actual user
- `ax` - all processes
- `u` - detailed data

Read data of a specific PID
```bash
ps wu <PID_NR>
```

Kill PID
```bash
kill <PID_NR>
```

Stop and restore PID
```bash
kill -STOP <PID_NR>
kill -CONT <PID_NR>
```

Ctrl + C
```bash
kill -INT <PID_NR>
```

Ctrl + Z freezes the process, to run again we use "fg" or "bg"

Read the process using blocking the specific port

```bash
lsof -ti tcp:<PORT_NR>
```

or

```bash
sudo lsof -i :<PORT_NR>
```

Stopping the service blocking the port

```bash
sudo systemctl stop <USER>
```

### Permissions

To see permissions use:
```bash
ls -l
```
```console
-rwxrw-r--
```
- first `-` means this is a simple file, `l` means it is a link
- `rwx`: user permissions read write execute
- `rw-`: group permissions read write, no execute
- `r--`: other users permissions read, no write no execute

Set write permission for other users and group
```bash
chmod og+w file
```

Set permissions with numbers
```bash
chmod 777 file
```
- 4: read
- 2: write
- 1: execute

Set permissions with +notation
```bash
chmod +x some_executable
```

### Compression

#### gzip

A file that contain .gz extension

Unpack
```bash
gunzip file.gz
```

Pack
```bash
gzip file
```

#### tar

To compress archives .tar extension

Create archive
```bash
tar cvf some_archive.tar file1 file2
```
- `c` : creating archive
- `v` : verbosity
- `f` : enable providing file name

Unpack from archive
```bash
tar xvf some_archive.tar
```
- `x` : unpack
- `t` : investigate
- `p` : keep same permissions like in archive

#### tar.gz / tgz

First we have to unpack gz and then tar.

We can do this also using zcat

```bash
zcat my_archive.tar.gz | tar xvf -
```

### File system

https://www.pathname.com/fhs/pub/fhs-2.3.html

- /
    - bin/ [binary executables]
    - dev/ [devices files]
    - etc/ [config files, like netplan for eth]
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

### Superuser

Use
```bash
sudo command
```
Or just log as super user
```bash
su
command
```

### Networks

Display active IP addresses
```bash
ifconfig
```

Display routing
```bash
route
```
- `-n` presents destination ip instead of names

File /etc/hosts consists of names and addresses used during search.

### Shell scripts

Remember to chmod +x to be able to execute the sh file.

All shell scripts should start with
```bash
#!/bin/sh
```

Scripts may use positional arguments

Let's have a sh file which consists of
```bash
echo $1
echo $2
```
So execution like this
```console
./my.sh lol rotfl

output:
lol
rotfl
```

Output code is in `$?` variable. In custom script we return the code
using the exit.

```bash
exit 1
```
means that there was an error of code 1.

if-else-elif-fi with the unix program that does the test for conditionals: `[]`

```bash
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
```bash
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
```bash
if grep -q daemon /etc/passwd; then
        echo there is a daemon user password
else
        echo there is no dameon  
fi
```

AND condition `&&`

```bash
if [ "$1" = hello ] && [ "$2" = friend ]; then
    echo 'Done, both contidions met'
fi
```

OR condition `||`

```bash
if [ "$1" = hello ] || [ "$2" = hi ]; then
    echo 'Done, one of conditions met'
fi
```

Files testing

```bash
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
```bash
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
```bash
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
```console
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
```console
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
of `ls -l` and prints only the first column of each entry
```console
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
```text
pass1: "lol"
```
if we use command below, the output stream will be changed, comparing to the file content:
```console
sed 's/:/%/' my_passwords

output:

pass% "lol"
```

`sed` may also work on addresses, so let's say we have a file named `text` that consists of:
```text
first
second
third
fourth
fifth
sixth
```
if we use comand below, it will remove rows from 2nd to fifth, comparing to the file content:
```console
sed 2,5d text

output:
first
sixth
```

`xargs` - runs command for each parameter from input stream

Here `xargs` will run creation of three directories named d1, d2 and d3
```console
echo 'd1 d2 d3' | xargs mkdir

ll

output:
d1/
d2/
d3/
```
`xargs` with `-t` option makes the command visible
```console
echo 'c1 c2 c3' | xargs -t rm -rf

output:
rm -rf c1 c2 c3
```
`xargs` to remove all git branchses that match regex
```bash
git branch | grep "some-branch-name-part" | xargs git branch -D
```

`expr` is for executing math operations or operations on strings
```console
expr 1 + 2

output:
3
```

`exec` changes current process to a program provided, but after `ctrl+c`/`ctrl+d` the previous process (like terminal) is terminated

To run scripts from our script we use `.`

Let's say we have a `scrip1.sh` that does something and we use `script2.sh` to run the first one as a part of the functionality. So the `script2.sh` looks like this:
```bash
echo "I will now run first script"
. script1.sh
echo "First script was executed"
```

`read` to read one row of input, let's print out what the user provided to the terminal, so we have a file `read_input`:
```bash
read some_input
echo see this $some_input
```
if we execute it and later on provide an input, we will se this
```console
./read_input

input:
lol

output:
see this lol
```

## Useful applications

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

```bash
sudo apt-get install pkg-config libssl-dev
```

## Installation guidelines

### Installing from .deb files

#### dpkg

Run installation with:

```bash
sudo dpkg -i package.deb
```

If dependencies are missing, fix them with:

```bash
sudo apt-get install -f
```

#### apt

```bash
sudo apt install ./package.deb
```

### VSCode

[Docs](https://code.visualstudio.com/docs/setup/linux)

> Note: Use the terminal approach so that the `code` is added automatically to path

### Display link

Download: https://www.synaptics.com/products/displaylink-graphics/downloads/ubuntu

Follow: https://support.displaylink.com/knowledgebase/articles/1944022-how-to-install-displaylink-software-on-ubuntu-20-0

### Linux alongside Windows

- Installation

    [Installation guidelines](https://www.fosslinux.com/50836/install-linux-mint-alongside-windows.htm)

- Make Windows default on ubuntu boot GRUB

        sudo grep menuentry /boot/grub/grub.cf

    or:

        sudo fgrep menuentry /boot/grub/grub.cf

    Save the: 
    
        `Windows Boot Manager (on /dev/nvme0n1p1)`

- Edit the GROB config

        sudo nano -B /etc/default/grub

    And set the line:

        GRUB_DEFAULT="Windows Boot Manager (on /dev/nvme0n1p1)"

- Apply changes

        sudo update-grub
