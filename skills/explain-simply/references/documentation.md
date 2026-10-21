# Documentation rules

How to organize information across documentation files so each fact has one
home, readers find it fast, the files never contradict each other, and
nothing is lost when the docs change.

## Contents

- [Classify before writing](#classify-before-writing)
- [One home per fact](#one-home-per-fact)
- [Find duplication and contradictions](#find-duplication-and-contradictions)
- [Linking](#linking)
- [Editing existing documentation](#editing-existing-documentation)
- [Structure of a usage guide](#structure-of-a-usage-guide)
- [Commands and examples](#commands-and-examples)
- [Restructuring without losing knowledge](#restructuring-without-losing-knowledge)

## Classify before writing

Decide what kind of information you have, then put it in the file that owns
that kind. The four kinds come from [Diátaxis](https://diataxis.fr/):

| Kind | Answers | Reader | Typical file |
| --- | --- | --- | --- |
| Tutorial | "Teach me from zero" | New user | `README.md` quick start, `docs/tutorial.md` |
| How-to | "How do I do X?" | User with a goal | `USAGE.md`, `docs/how-to/*.md` |
| Reference | "What does this flag, key, or code mean?" | User looking something up | `USAGE.md` tables, `docs/reference/*.md`, `--help` |
| Explanation | "Why does it work this way?" | User or contributor who wants to understand | `ARCHITECTURE.md`, `docs/concepts/*.md` |

And by audience:

| File | Owns |
| --- | --- |
| `README.md` | What the project is, a minimal example, install, and links to the other docs |
| `USAGE.md` | Every user-facing command, option, config file, and behavior |
| `DEVELOPMENT.md`, `CONTRIBUTING.md` | Setting up the repo, running tests, the contribution workflow |
| `ARCHITECTURE.md` | Design decisions and the reasons behind them |
| `AGENTS.md`, `CLAUDE.md` | Rules for coding agents |
| `CHANGELOG.md` or releases | What changed in each version |

Follow the files the repository already has. If `AGENTS.md` or
`CONTRIBUTING.md` says which file owns what, that wins over these tables.

Do not mix kinds in one section. A how-to step that stops to explain design
history loses the reader; move the history to the explanation and link to it.

## One home per fact

Every fact lives in exactly one place. Everywhere else links to it.

Bad: the same install instructions in three files, worded three ways.

```markdown
<!-- README.md -->
## Install
Run `pipx install mytool`. Requires Python 3.10 or newer.

<!-- USAGE.md -->
## Installation
Install with `pipx install mytool`. You need Python 3.10+.

<!-- DEVELOPMENT.md -->
## Install
First install the tool with `pipx install mytool` (Python 3.10 or later).
```

Good: `README.md` owns installation, and the others link to it.

````markdown
<!-- README.md -->
## Install
Requires Python 3.10 or newer.

```bash
pipx install mytool
```

<!-- USAGE.md -->
Install the tool as described in [Install](README.md#install).

<!-- DEVELOPMENT.md -->
For a development setup, clone the repo and run `uv sync`. To use the
released tool instead, see [Install](README.md#install).
````

When the Python version changes, one line changes. With three copies, one of
them is eventually left at the old version, and the docs contradict each
other.

## Find duplication and contradictions

Do this when you edit documentation, and in full when the user asks to clean
up, shorten, or check the docs. Check the whole set of files, not only the
one you are touching, because a copy you do not see is the one that goes
stale.

1. List the facts that tend to be repeated: install commands, required
   versions, flags and their defaults, config keys, environment variables,
   paths, ports, and limits.
2. Search for each one across the docs. Search for the value as well as the
   name, since a copy may use different words:

   ```bash
   grep -rn -e "--from-beginning" -e "3\.10" README.md USAGE.md docs/
   ```

3. Read the section around each hit and sort it:

   | Finding | Fix |
   | --- | --- |
   | Same fact, same value, in two places | Keep it in the file that owns it. Replace the copy with a link. |
   | Same fact, different values | A contradiction. Find the true value in the code, the config, the `--help` output, or the tests. Fix the owner and replace the copy with a link. |
   | Docs disagree with the code | The code shows what the tool does now, so update the docs. If the code looks like the bug, tell the user instead of documenting the bug. |
   | You cannot tell which value is true | Do not pick one. Tell the user what each file says and where. |
   | One thing under several names | Use one name everywhere, as described in [Say it once, and the same way](../SKILL.md#say-it-once-and-the-same-way). |

4. Inside each file, look for these signs of repetition:
   - A summary or overview section that restates the sections after it.
   - A "Notes" or "Important" section that repeats warnings already given in
     place.
   - Two sections that describe the same option or behavior.
   - An introduction that says what the conclusion says.
5. Tell the user what you found and changed: each duplicate or contradiction,
   the file you kept as its home, and, for a contradiction, the true value
   and where it came from.

## Linking

- Use relative links with anchors: `[Credential vault](USAGE.md#credential-vault)`.
- Link text names the target. Never "click here", "this link", or "see
  above".
- Give one sentence of context with the link, so the reader knows whether to
  follow it: "OAuth needs its own CA; see [OAuth](#oauth)."
- Link the first mention in a section, not every mention.
- Keep links one level deep where possible. A reader should not follow three
  links to reach the fact.
- After renaming a heading, update every link to its anchor.

## Editing existing documentation

1. Search before adding. If the fact already exists, update it in its home
   instead of writing a new copy.
2. Replace instead of appending. When behavior changes, rewrite the existing
   text. A new paragraph added below the old one leaves the docs saying two
   different things.
3. Remove what is obsolete. Deleted features, old flags, and outdated
   workarounds go away. History belongs in the changelog.
4. Document only what exists. No planned features, no "coming soon".
5. Keep the style of the file. Match its heading style, example format, and
   level of detail.
6. Update the contents list when you add, rename, or remove a heading.

## Structure of a usage guide

A `USAGE.md`, or any guide for users, follows this order:

1. A title and one short paragraph that says what the tool does.
2. The smallest useful example, so a reader can start right away.
3. A contents list of the `##` and `###` headings, linked by anchor, when the
   file is longer than a few screens.
4. Sections named after tasks ("Add a profile", "Consume from the
   beginning"), not after internal modules.
5. Reference sections for options, environment variables, config keys, and
   exit codes, as tables.

Inside each task section:

1. One sentence: what the task does and when you need it.
2. The command or config.
3. What the reader should see.
4. Edge cases, limits, and errors, each said once.

Good section:

````markdown
## Consume from the beginning

Read every record still in the topic, instead of only new ones:

```bash
mytool consume orders --from-beginning
```

Records print as they arrive. Press `Ctrl+C` to stop. `--from-beginning`
can't be combined with `--offset`.
````

## Commands and examples

- Every example runs as written. Copy it, paste it, it works.
- Use clearly fake values: `example.com`, `replace-with-api-key`, `orders`.
  Never real hosts, tokens, or personal data.
- Tag code blocks with their language: `bash`, `yaml`, `json`, `text`.
- Show output in its own `text` block, not mixed into the command block.
- One command per block when the reader will copy it.
- Explain a non-obvious flag in the sentence before the block, not in a
  comment that repeats it.

## Restructuring without losing knowledge

When you shorten, merge, or move documentation:

1. List the facts first. Before deleting a paragraph, write down every fact
   it contains, as defined in [Keep the knowledge](../SKILL.md#keep-the-knowledge).
2. Find each fact a home. It stays where it is, moves to the file that owns
   it, or is already covered elsewhere. In the last case, check that the
   existing text gives the same value; if not, it is a contradiction (see
   [Find duplication and contradictions](#find-duplication-and-contradictions)).
3. Rewrite, then compare. Check the new text against your list. Every item
   must be present or reachable by one link. Shorter is better only when
   nothing on the list went missing.
