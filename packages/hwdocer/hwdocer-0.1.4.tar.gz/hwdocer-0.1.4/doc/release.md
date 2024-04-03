# HWDOCER releases

See what is planned in the [roadmap][roadmap_file]

## 0.1.4

Release date: _2024-04-02_

**Features:**

- source files are now copied in output folder
- refactor the execution to be file based instead of process based
- all building is now executed in isolated multiprocessor-compatible processes
- added argument to control the number of processes created
- added argument to limit the execution time
- added argument to control the output files format (present but not used yet)

**Fix:**

- image from harnesses are now correctly copied into a similar folder structure inside output folder

**Known problems:**

- drawio calls throws some error in console and logs
- wireviz bad syntax throws stacktrace in console and logs
- leave a lot of undesired generated files in input and output folders

## 0.1.3

Release date: _2024-03-27_

**Features:**

- copy all images defined in harness with tag `image`.`src` to output path (for html correct render)

**Known problems:**

- drawio calls throws some error in console and logs
- wireviz bad syntax throws stacktrace in console and logs
- **[corrected in 0.1.4]** image copy doesn't recreate sub-folder structure into output destination
- leave a lot of undesired generated files in input and output folders

## 0.1.2

Release date: _2024-03-27_

**Features:**

- Improve debug verbosity
- Input file search is more iterative now

**Change:**

- Changed input file search to use glob instead of os.walk

**Known problems:**

- drawio calls throws some error in console and logs
- wireviz bad syntax throws stacktrace in console and logs
- leave a lot of undesired generated files in input and output folders

## 0.1.1

Release date: _2024-03-26_

**Fix:**

- Project publishing metadata added/corrected

**Known problems:**

- drawio calls throws some error in console and logs
- wireviz bad syntax throws stacktrace in console and logs
- leave a lot of undesired generated files in input and output folders

## 0.1.0

Release date: _2024-03-26_

**Features:**

- Initial functional release
- development venv setup
- logging in multiprocessing thread
- drawio automatic drawing via system call
- wireviz automatic drawing
- basic functional test for diagram and harness
- selectable verbosity in console and log (one argument for both)
- buildable & deployable with poetry

**Known problems:**

- drawio calls throws some error in console and logs
- wireviz bad syntax throws stacktrace in console and logs
- leave a lot of undesired generated files in input and output folders

---

[roadmap_file]: roadmap.md
