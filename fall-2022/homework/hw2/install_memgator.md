# How to Install MemGator

Download and install a local version of MemGator

* Go to the [Releases page](https://github.com/oduwsdl/MemGator/releases) in the repository
* Scroll down to the "Assets" section.  Click the triangle icon to expand the list.  Choose the executable that matches your OS.
  * -darwin is for MacOS
  * -386 is for 32-bit architectures (older machines)
  * -amd64 is for 64-bit architectures (newer machines)

Memgator is a command-line tool, so you will need to run it from Terminal (for MacOS) or PowerShell (for Windows).  You may need to set the permissions to executable before it will run.

* MacOS: If you get a security pop-up the first time you run it, open Finder to where you've installed it.  Right-click on memgator and choose Open.  Then you'll be able to select 'Open' from the pop-up.  Once you've done that, you'll be able to run it from the command line.

Test out your installation of memgator with the following example.  

* `$` is the command line prompt (don't type that in)
* Replace `./memgator-darwin-amd64` with the appropriate executable for your system

```bash
$ ./memgator-darwin-amd64 -F 2 -f JSON https://alexandernwala.com/ > anwala_tm.json
```

The result in `anwala_tm.json` should be similar to what you see below.  
```bash
$ head anwala_tm.json
{
  "original_uri": "https://alexandernwala.com",
  "self": "http://localhost:1208/timemap/json/https://alexandernwala.com",
  "mementos": {
    "list": [
      {
        "datetime": "2021-07-25T05:52:37Z",
        "uri": "https://web.archive.org/web/20210725055237/https://alexandernwala.com/"
      },
      {
        ...
```

**Questions:** What do the `-F 2` and `-f JSON` options do?
