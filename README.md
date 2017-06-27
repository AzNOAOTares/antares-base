# antares-base

This is the repo for making documentation for Antares API.

## Directory structure

- `antares`: where python source code for API goes.
- `doc`: where source for documentation goes (.rst files)
- `Makefile`: used to generate online documentation at
  [here](http://aznoaotares.github.io/antares-base/index.html).

## Documentation source code structure.

doc/source

	|--- _static (resources, like png, js files, etc.)
	
	|--- alert (where .rst docs for alert go)
	
	|--- property (where .rst docs for property go)
	
	|--- context (where .rst docs for context go)
	
	|--- examples (where .rst docs for examples go)
	
	|--- helper (where .rst docs for helper functions go)
	
	|--- index.rst (.rst doc for the index page)
	
	|--- rules_constraints.rst (.rst doc for rules&constraints goes)
	

## How to generate online documentations

There are two branches for this repo, one is `master`, the other one
is `gh-pages`, which is used by Github to render webpages. You never
need to explicitly switch to `gh-pages` branch. Always work with the
`master` repo.

### Steps to follow

0. update python files in antares/*
1. make changes to the source code under `doc/source`.
2. commit and push your changes to the `master` branch.
3. render the webpages to reflect most-recent changes by executing:
```sh
make gh-pages
```

Then go to http://aznoaotares.github.io/antares-base/index.html to see
the newly updated webpages. If you cannot see the changes immediately,
refresh the page for a couple of times or clean up the cookies, then
you should be good to go.
