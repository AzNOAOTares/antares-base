# antares-base

This is the repo for making documentation for Antares API via Sphinx and GitHub pages

## Directory Structure

- `antares`: where python source code for API goes.
- `doc/source/`: where .rst files for documentation goes.
- `Makefile`: used to generate html files for online documentation at
  [here](http://aznoaotares.github.io/antares-base/index.html).

### Documentation .rst Source Code Structure

doc/source/

	|--- _static/ (resources, like png, js files, etc.)
	|--- alert/ (.rst docs for antares.model.alert.*)
	|--- property/ (.rst docs for antares.model.property.*)
	|--- context/ (.rst docs for antares.model.context.*)
	|--- examples/ (.rst docs for examples)
	|--- helper/ (.rst docs for antares.model.helper.*)
	|--- index.rst (for the main index page)
	|--- rules_constraints.rst (for rules&constraints, referenced in index.rst)
*directories correspond to python modules, .rst files correspond to python classes* 


## How to Generate Online Documentation

There are two branches for this repo, one is `master`, the other one
is `gh-pages`, which is used by Github to render webpages. You *never*
need to explicitly switch to `gh-pages` branch. **Always work with the
`master` branch.**

 -- Please note that you don't really need to make any changes to gh-pages.
### Updating Python Files and Rendering New Documentation

0. Ensure that Sphinx is installed in your python virtual-environment (`pip install Sphinx`)
	- This is used by the makefile
1. Update python files in `antares/` (copy changed files from antares repo)
2. Make sure .py files in `antares/` are compilable by executing: ```python3 setup.py install```
	- The makefile will try to import all .py files in `antares/`, any import errors will cause errors in rendering webpages
3. Make updates to the corresponding .rst files under `doc/source/`; *this is not done automatically*
	- That is, add labels for new attributes, methods, etc. so that the new html pages reflect the new python docstrings
4. Commit and push your changes to the `master` branch.
5. Render the webpages to reflect most-recent changes by executing: ```make gh-pages```
	- This will push the newly rendered html files to the gh-pages branch
6. Go to http://aznoaotares.github.io/antares-base/index.html to see
the newly updated webpages. 
	- If you cannot see the changes immediately,
refresh the page for a couple of times or clean up the cookies, then
you should be good to go.

### Resources

- https://pythonhosted.org/an_example_pypi_project/sphinx.html
- http://www.sphinx-doc.org/en/stable/
- Existing docstrings in python files and their respective .rst files
