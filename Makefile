PYTHON ?= python

.PHONY: verify

verify:
	$(PYTHON) scripts/verify.py
