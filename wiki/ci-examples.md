# CI Examples

This project includes a GitLab CI pipeline (`.gitlab-ci.yml`). Below are notes and examples tailored to this repo.

## Current Jobs (in repo)
- `validate_syntax` (stage: validate): Checks for required files and assets.
- `test_framework` (stage: test): Parses `init python:` blocks in `.rpy` files to validate syntax.
- `build_docs` (stage: build): Validates docs exist.
- `create_release` (stage: build): Produces ZIP/TAR archives in `dist/` for tags.
- `pages` (stage: deploy): Publishes docs to GitLab Pages.
- `security_scan` (stage: validate): Grep-based warnings for risky patterns.

Note: Paths in `validate_syntax` should be updated to match this repo structure:
```yaml
script:
  - python -c "import os; assert os.path.exists('game/core/rooms/room_main.rpy')"
  - python -c "import os; assert os.path.exists('game/core/rooms/room_config.rpy')"
```

## Add Ren'Py Lint & Distribute Jobs
Prefer using a `RENPY_SDK` CI variable that points to your SDK path (default `/opt/renpy-8.4.2`).
```yaml
renpy_lint:
  stage: build
  image: debian:bookworm-slim
  tags: [ linux ]  # adjust for your runner
  script:
    - "$RENPY_SDK/renpy.sh" "$CI_PROJECT_DIR" lint

renpy_distribute:
  stage: build
  image: debian:bookworm-slim
  tags: [ linux ]
  script:
    - "$RENPY_SDK/renpy.sh" "$CI_PROJECT_DIR" distribute
  artifacts:
    paths:
      - dist/
    expire_in: 1 month
  needs: [ renpy_lint ]
  only:
    - tags
```

Also update doc paths to match the capitalized `Wiki/` directory used here (the sample CI references `wiki/`).

## Artifacts & Pages
- Build artifacts: `dist/<project>-*-win/` and `dist/<project>-*-linux/`.
- Pages: copy `README.md` and `Wiki/` into `public/` like the existing `pages` job.

## Caching (optional)
```yaml
cache:
  key: "$CI_COMMIT_REF_SLUG"
  paths:
    - game/cache/
```

Keep the pipeline fast by gating distribute jobs on lint/tests.
