# TypstDiff
### Dominika Ferfecka, Sara Fojt, Małgorzata Kozłowska

## Introduction
Tool created with Pandoc to compare two typst files. It marks things
deleted from first file and marks differently things added to the second file.

## Run virtual environment
To run virtual environment in poetry go to TypstDiff folder and use command
`poetry shell`

To exit virtual environment use command
`exit`

## Installing dependencies
To install the same versions of dependencies as used in the project you can use 
`pip install -e .` or `poetry install`

## Run tests
To run tests use command
`poetry run pytest -v`

### Issues
As both tools - Pandoc and Typst are new and still developing there is no full support
for typst in Pandoc. Because of that it is not possible to notice all changes made
in files, but tool will be developed.