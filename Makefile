.PHONY: help lint push-both push-all wiki-sync wiki-dry

help:
	@echo "Targets:"
	@echo "  lint       - Run Ren'Py lint"
	@echo "  push-both  - Push current branch and tags to all origin push URLs"
	@echo "  push-all   - Push all branches and tags"
	@echo "  wiki-sync  - Sync Wiki/ to GitHub wiki"
	@echo "  wiki-dry   - Dry-run wiki sync"

lint:
	@~/renpy-8.4.1-sdk/renpy.sh . lint

push-both:
	@bash scripts/push-both.sh

push-all:
	@bash scripts/push-both.sh all

wiki-sync:
	@bash scripts/sync-github-wiki.sh

wiki-dry:
	@bash scripts/sync-github-wiki.sh dry-run
