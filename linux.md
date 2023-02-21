# Linux cheat sheet

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

current directory
```
.
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
Display all files names staring with"at"
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
---
### Display
---

Read files content
```
cat file1 file2 ...
```

Read folder content (For detailed flags use --help)
```
ls
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
- space - next page, b - previous page, q - break

Find file(s) in directory
```
find ./ -name .localized
find ./Movies -name .localized
find /users/me -name '.zsh[a-z_]*' | sort
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
- -r reversed

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
- -i ignores letters size, -v prints the rows that do not contain the phrase, -r recursive to include files and subfolders

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
- use >> to appen to file without erasing the previous content

Redirect from file to command (hear "head")
```
head < file
```
- usually the < is not required as this behaviour is default for many commands

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
- -r recursively, -f force

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

add to PATH at front for terminal lifetime
```
PATH=/new/location:$PATH
```

add to PATH for terminal lifetime
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
- optional parameters: w - with commands, x - processes started by actual user, ax - all processes, u - detailed data

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
Read permissions
```
ls -l
```
```
-rwxrw-r--
```
- first "-" means this is a simple file, "l" means it is a link
- rwx: user permissions read write execute
- rw-: group permissions read write, no execute
- r--: other users permissions read, no write no execute

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
