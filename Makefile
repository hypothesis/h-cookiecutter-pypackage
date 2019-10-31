.PHONY: help
help:
	@echo "make help              Show this help message"
	@echo "make lint              Code quality analysis (pylint)"
	@echo "make format            Correctly format the code"
	@echo "make checkformatting   Crash if the code isn't correctly formatted"
	@echo "make dist              Create package in the dist/ directory"
	@echo "make release           Tag a release and trigger deployment to PyPI"
	@echo "make re-release        Re-release a tag by specifying VERSION=v.1.x.x etc."
	@echo "                       This will not overwrite a package in PyPI but can be"
	@echo "                       useful if the release did not pass CI the first time."
	@echo "make publish           Publish packages created in the dist/ directory"
	@echo "make test              Run the unit tests"
	@echo "make coverage          Print the unit test coverage report"
	@echo "make clean             Delete development artefacts (cached files, "
	@echo "                       dependencies, etc)"
	@echo "make template          Replay the cookiecutter project template over this"
	@echo "                       project. Warning! This can destroy changes."

.PHONY: lint
lint: python
	@tox -qe lint

.PHONY: format
format: python
	@tox -qe format

.PHONY: checkformatting
checkformatting: python
	@tox -qe checkformatting

.PHONY: dist
dist: python
	@BUILD=$(BUILD) tox -qe package

.PHONY: release
release: python
	@tox -qe release

.PHONY: re-release
re-release:
	@[ -z "$(VERSION)" ] && { echo "No VERSION specified"; exit 1; } || echo "This will delete and remake the tag '$(VERSION)'"
	@read -p "(Enter to continue, Ctrl-C to quit)" dummy
	@git tag --delete $(VERSION)
	@git tag -a $(VERSION)
	@git push --delete origin $(VERSION)
	@git push origin $(VERSION) --follow-tags

.PHONY: publish
publish: python
	@tox -qe publish

.PHONY: test
test: python
	@tox -q

.PHONY: coverage
coverage: python
	@tox -qe coverage

.PHONY: template
template: python
	@tox -qe replay-cookiecutter

.PHONY: clean
clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -rf build .eggs dist *.egg-info src/*.egg-info .coverage.* .coverage .pytest_cache

.PHONY: python
python:
	@./bin/install-python.sh
