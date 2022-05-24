# Linux command-line utilities (3 points)

The goal of this assignment is to help you practice using simple [Linux commands](https://linuxjourney.com/) on the terminal. From your local Linux terminal or [one of WM's Linux machines](https://www.cs.wm.edu/~tadavis/remoteaccess.html),

## Q1. (1 point) 
Create a directory (name it whatever you wish, e.g., `data440`. Change the permissions on this directory so that you are the only user who can read, write, or execute (view the contents) the directory (see ["Protection and Permission"](https://linuxjourney.com/lesson/file-permissions)). Take a screenshot of (or copy/paste) the command and its output into your report.

## Q2. (2 points) 
In the directory that you just created, use a simple text editor (e.g., the nano editor) to create a file named test.txt (`nano test.txt`) with the following contents:

```text
CS 800
CS 432
CS 725
MATH 212
MATH 32
```

For each of the commands below, do the following:

* Execute the command
* Take a screenshot of (or copy/paste) the command and its output into your report
* Write a sentence that describes what the command did

Commands:

1. `wc -l test.txt`
2. `echo "CS 800" >> test.txt; cat test.txt`
3. `grep CS test.txt`
4. `grep -c CS test.txt`
5. `sort test.txt`
6. `sort -k2 test.txt`
7. `sort -k2 -n test.txt`
8. `sort test.txt | uniq -c`

For more information, see ["Redirection and Pipes"](https://linuxjourney.com/lesson/pipe-tee-redirect).  For information on the Unix commands, you can use the `man` command (ex: `man grep`) to display the manual page or google the command.
