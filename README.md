# antares-base

This is the repo for making documentation for Antares API.

## Directory structure

- `antares`: where source code for API goes.
- `doc`: where source for documentation goes
- `Makefile`: used to generate online documentation at
  [here](http://aznoaotares.github.io/antares-base/index.html).

## Documentation source code structure.

doc/source

    |--- _static (resources, like png, js files, etc.)
	
	|--- alert (where docs for alert goes)
	
	|--- attribute (where docs for attribute goes)
	
	|--- context (where docs for context goes)
	
	|--- examples (where docs for examples goes)
	
	|--- helper (where docs for helper functions goes)
	
	|--- index.rst (where docs for the index page goes)
	
	|--- rules_constraints.rst (where docs for rules&constraints goes)
	

## How to generate online documentations

There are two branches for this repo, one is `master`, the other one
is `gh-pages`, which is used by Github to render webpages. You never
need to explicitly switch to `gh-pages` branch. Always work with the
`master` repo.

### Steps to follow

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
