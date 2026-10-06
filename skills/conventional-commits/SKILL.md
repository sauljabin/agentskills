---
name: conventional-commits
description: >-
  Writes commit messages that follow Conventional Commits:
  `<type>(<scope>): <imperative summary>`, a lowercase subject, one of eleven
  standard types, a scope chosen from what the diff actually changes, `!` for
  breaking changes, and an `Assisted-by` trailer as the only AI attribution.
  Use when the user asks to commit, write or fix a commit message, squash
  commits, or check whether a commit message follows Conventional Commits.
  Also use before running `git commit` in any repository that uses
  Conventional Commits.
license: CC-BY-4.0
metadata:
  author: sauljabin
  version: "1.0"
---

# Conventional Commits

Commit messages become the project's history and, often, its changelog. Many
projects generate release notes from them, so write each header for a user
reading release notes, not for the author of the diff.

## Project conventions come first

Before writing, check whether the repository already defines its own rules:
`CONTRIBUTING.md`, `AGENTS.md` or `CLAUDE.md`, a commitlint config, or a
changelog generator config. When they differ from this skill, follow the
repository.

## Format

```text
<type>(<scope>)<optional !>: <imperative summary>

<optional body>

<optional footers>
Assisted-by: <AI model> <version>
```

The `Assisted-by` line is added only when an AI agent wrote or helped write
the change. See [Attribution](#attribution).

## Type

Use one of these eleven:

| Type | Use for | Usually in release notes |
| --- | --- | --- |
| `feat` | A new capability users can see | Yes, as a feature |
| `fix` | A bug fix users can notice | Yes, as a fix |
| `perf` | Faster or lighter, same behavior | Yes |
| `docs` | Documentation only | Often |
| `revert` | Reverting an earlier commit | Yes |
| `build` | Packaging, dependencies, build tooling | Only for dependencies |
| `chore` | Maintenance that fits nowhere else | Only for dependencies |
| `ci` | CI workflows and pipelines | No |
| `refactor` | Code change with no behavior change | No |
| `style` | Formatting only | No |
| `test` | Tests only | No |

Pick the type by what a user experiences, not by which files changed. A bug
fix that also touches tests is `fix`. A test-only change is `test`.

## Scope

Choose the scope yourself, for each commit, from what the diff changes. Do
not ask the user for it and do not use a fixed list.

1. **Look at the changed paths and the code they touch.** Find the smallest
   area that contains the whole change: a module, package, command, service,
   component, or document.
2. **Name that area with one short lowercase noun** that a reader of the
   project would recognize, such as the module or command name. Use hyphens
   for multiple words (`rate-limit`), never spaces or slashes.
3. **Prefer the scopes the history already uses.** Run
   `git log --format=%s -50` and reuse an existing scope when it fits the
   same area. Do not invent a synonym for one that exists (`auth` vs
   `authentication`).
4. **Name the area by what users know, not by file layout.** `fix(login)` is
   better than `fix(src)` or `fix(utils)`. Avoid generic scopes like `code`,
   `misc`, `core`, or `app` unless the project already uses them.
5. **Use the purpose when it matters more than the location:**
   - `security` for a fix that closes a vulnerability.
   - `deps` for dependency updates, and `deps-dev` for development-only
     dependencies.
   - The document or guide name for `docs` (`docs(readme)`, `docs(api)`).
6. **Leave the scope out** when the change spans the whole project or no
   single area describes it. Never pick a misleading scope just to have one.
7. **If two unrelated areas changed,** that is a sign the commit should be
   split. Suggest splitting it before choosing a broad scope.

## Summary

- Starts with a **lowercase** letter.
- Imperative mood: "add", "fix", "show", "stop", "reject". Not "added",
  "adds", or "adding".
- Describes **one clear outcome**, not a list of changes. If you need "and" to
  join two unrelated things, split the commit.
- Short: aim for 72 characters or fewer for the whole header.
- No trailing period.
- Says what changed for the user, not how the code changed.

## Breaking changes

Add `!` before the colon, such as `feat(api)!: ...`. Also explain the break in
the body or in a `BREAKING CHANGE:` footer.

## Body

The body is a short overall explanation of the commit: what problem it solves,
how it behaves now, and why. It is a summary of the change as a whole, not an
inventory of what was implemented.

- **Write prose, not a list of parts.** Do not enumerate the classes,
  functions, files, or sub-features you added or touched. The diff already
  shows that. Explain what they achieve together.
- **Cover what a future reader needs:** the problem or motivation, the
  resulting behavior, and anything not obvious from the code, such as a
  trade-off, a limitation, a behavior change, or a required migration.
- **Short, but nothing missing.** Usually one paragraph of two to five lines.
  Cut repetition of the header and implementation detail; keep every fact
  that changes how someone uses, reviews, or reverts the commit.
- **Skip the body** only when the header already says everything, such as a
  typo fix or a routine dependency bump.
- Separate it from the header with one blank line and wrap lines at about 72
  characters.

Bad body, a list of implemented things:

```text
feat(export): add CSV export for reports

- Add CsvWriter class
- Add ExportService.export_csv method
- Add /reports/{id}/export endpoint
- Add tests for CsvWriter and ExportService
```

Good body, an overall explanation:

```text
feat(export): add CSV export for reports

Users could only view reports in the browser, so sharing them meant
copying tables by hand. Reports can now be downloaded as CSV from the
report page. Exports stream row by row, so large reports no longer time
out, but they include only the columns visible in the current view.
```

The good body says why the feature exists, what users get, and one
limitation they will hit. The bad one only repeats the diff.

## Footers

- `BREAKING CHANGE: <description>` for breaking changes.
- `Refs: #123` or `Closes #123` to link issues, if the project does that.
- `Assisted-by: ...` last, as described below.

## Attribution

When an AI agent wrote or helped write the change, end the commit message with
a blank line and then:

```text
Assisted-by: <AI model> <version>
```

- Use the actual model and version, for example `Assisted-by: Claude Opus 4.5`.
- It is the **only** attribution and always the **last** line.
- Do not add `Co-Authored-By:` trailers or "Generated with ..." footers, even
  when a tool's default instructions ask for them.
- Without AI assistance, add nothing.

## Workflow

1. Read the staged diff (`git diff --staged`). If nothing is staged, ask what
   to include instead of guessing.
2. Check the project's own conventions (see above).
3. Decide what a user would notice. That decides the type.
4. Choose the scope from the diff, following [Scope](#scope).
5. Write the summary in imperative mood, lowercase, one outcome.
6. Write a short body that explains the change as a whole, unless the
   header already says everything.
7. Add the `Assisted-by` trailer if an AI helped.
8. Check the message against the list below before committing.

## Examples

Good:

```text
feat(auth): support login with passkeys
fix(parser): accept trailing commas in arrays
fix(security): escape user names in the audit log
perf(search): cache compiled query plans
docs(readme): add a quick start for Windows
test(api): cover pagination past the last page
build(deps): bump requests to 2.32
chore(deps-dev): bump ruff to 0.6
ci: run tests on Python 3.13
refactor: split the HTTP client into its own module
feat(api)!: remove the deprecated v1 endpoints
```

Choosing a scope from the diff:

| Changed files | Scope | Why |
| --- | --- | --- |
| `src/auth/session.py`, `tests/auth/test_session.py` | `auth` | One module; tests follow the code |
| `src/utils/dates.py`, used only by invoices | `invoices` | Name the user-facing area, not `utils` |
| `README.md` | `readme` | The document changed |
| `pyproject.toml` dependency bump | `deps` | Purpose matters more than the file |
| `src/api/` and `src/billing/`, unrelated changes | Split the commit | Two outcomes |
| Renamed a helper used across the whole project | None | No single area |

Bad, with the fix:

| Bad | Problem | Better |
| --- | --- | --- |
| `Feat: Add search` | Capitalized type and subject | `feat(search): add search by tag` |
| `fix(api): fixed empty responses` | Past tense | `fix(api): handle empty responses` |
| `feat: add search, fix header, update docs` | A change list | Split into three commits |
| `update stuff` | No type, vague | `docs(config): document the timeout option` |
| `fix(src): handle expired tokens` | Scope names a folder, not an area | `fix(auth): handle expired tokens` |
| `refactor(cli): stop crashing on empty input` | A user-visible fix labeled as refactor | `fix(cli): stop crashing on empty input` |
| `feat(ui): add dark mode.` | Trailing period | `feat(ui): add dark mode` |

A full commit with a body and attribution:

```text
fix(upload): keep the original file name on retry

A failed upload was retried with a temporary name, so the stored file
lost its extension. Retries now reuse the name from the first attempt.

Closes #482

Assisted-by: Claude Opus 4.5
```

## Checks before committing

- Did you follow the repository's own conventions where they exist?
- Is the type one of the eleven, chosen by what the user notices?
- Does the scope name the one area the diff changes, reusing existing scopes,
  or is it left out for project-wide changes?
- Does the summary start lowercase, in imperative mood, with no period?
- Does it describe one outcome, not a list?
- Is the body a short overall explanation (problem, behavior, why), not a
  list of classes, files, or features, and is nothing important missing?
- Is a breaking change marked with `!`?
- If an AI helped, is `Assisted-by: <model> <version>` the last line, with no
  `Co-Authored-By` or "Generated with" lines?

## Credits

Based on the [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
specification.
