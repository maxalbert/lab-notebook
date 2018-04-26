Lab notebook
============

Author: Maximilian Albert <maximilian.albert@gmail.com>

This is a quick-and-dirty approach to keeping daily notes in a "lab notebook" fashion. This is purely intended for personal use and in no way meant to be a general-purpose note-keeping system. It has been working well for me but YMMV obviously.

It mainly uses Markdown format, sprinkled with [Asciidoc](http://asciidoc.org/) to enhance functionality.

My key considerations were:

- Use Markdown (ideally github-flavoured markdown) format for keeping notes because it's lightweight and flexible
- One file per day, accumulate into 
- Easy conversion to reasonably pretty pdf

## Prerequisites

- Text editor with Markdown support (e.g. Sublime Text with a Markdown plugin)

- [asciidoctor-pdf](https://github.com/asciidoctor/asciidoctor-pdf)
  _TODO: Add some installation info on Mac OS X_

  **Note:** Installing ruby via Homebrew caused problems for me on Mac OS X. I found [these instructions](http://usabilityetc.com/articles/ruby-on-mac-os-x-with-rvm/) by Jeffrey Morgan to install Ruby via `rvm` (the ruby version manager) very helpful (I think I just used the commands in section "Installing RVM and Ruby").

- `pdfnup` (to create a two-sided version of the pdf - I find this easier to read at a glance for longer documents)

- Ensure the auxiliary script below is visible in your path, in order to make the command `nn` available (which creates a new note).


## Workflow

### At the start of a project

_Note: In the future I may consider turning this into a [cookiecutter](https://github.com/audreyr/cookiecutter) template to automate these steps, if it turns out to be useful enough._

(i) Clone this repo to create a new lab notebook skeleton and get rid of the existing git history.
```
$ git clone https://github.com/maxalbert/lab-notebook.git
$ cd lab-notebook
$ rm -rf .git
```

(ii) Edit `convert.py` and change the project title.

(iii) Re-initialise a fresh git repo for the notebook and create an initial commit.
```
$ git init
$ git add .
$ git commit -m "Lab notebook for <project>: initial commit"
```

### For daily use:

- From within the lab notebook folder, type `nn` (for "new note") (this requires the script below to be accessible in your PATH)

  This will create a new file for the current date (with a heading reading `## YYYY-MM-DD`), add it to version control and open it in your editor.

- Type away & take notes of whatever is important...

  _(I often copy & paste a lot of things, especially during exploratory and trial & error type work, so that I can later revisit and learn from my different approaches and resulting insights)__

- At any point type `make notes-today` to convert today's markdown file into a pdf.

- You can also run `make watch` in a `tmux` session - this will run `make notes-today` every second to pick up changes immediately (make sure you use a pdf viewer that automatically refreshes, such as Skim on Mac OS X).

- Alternatively, run `make` (or `make all`) to generate a pdf with the entire history of notes.

  _TODO: In the future, it may be nice to easily limit the notes to, say, only the last week or so._

- At the end of the day (or whenever appropriate), `git commit` your notes for the day.

- Profit.


### Auxiliary scripts

Add the following script as `~/.local/bin/nn` (or any other location that's picked up in your PATH)

```
#!/bin/bash

# This is a little auxiliary command for my lab notebooks.
# It creates a skeleton file for the notes of the current day,
# adds it to version control and opens it in an editor.

# Define text editor to use for editing lab notebook files.
# This can be overridden by the LAB_NOTES_EDITOR environment
# variable. If it isn't set, use the value of EDITOR, or fall
# back to Sublime Text if neither is defined.
LAB_NOTES_EDITOR=${LAB_NOTES_EDITOR:=${EDITOR:=subl}}
TODAY=$(date +%Y-%m-%d)
FILENAME=markdown_notes/notes_${TODAY}.md

echo "## ${TODAY}" >> $FILENAME
git add $FILENAME
$LAB_NOTES_EDITOR $FILENAME
```
