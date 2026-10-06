# Wording rules

Rules for words, phrases, sentences, formatting, and tone. Each rule has a bad
and a good example. Apply them to chat answers, documentation, comments, and
commit messages.

## Contents

- [Words](#words)
- [Phrases to delete](#phrases-to-delete)
- [Sentence patterns](#sentence-patterns)
- [Formatting](#formatting)
- [Tone](#tone)

## Words

Replace inflated words with the plain one, or with the specific fact they
stand in for.

| Instead of | Write |
| --- | --- |
| utilize, leverage | use |
| serves as, functions as, stands as | is |
| features, boasts, offers | has |
| facilitate, enable, empower | let, help, or name what becomes possible |
| in order to | to |
| ensure | make sure, check, or say what is checked |
| delve into, dive into, explore | look at, or cut |
| enhance, elevate, optimize | improve, and say how much or in what way |
| showcase, highlight, underscore | show |
| streamline | say which step goes away |
| robust, powerful, seamless | say what it handles or what is automatic |
| crucial, pivotal, vital, key | cut, or state the consequence |
| comprehensive | say what it covers |
| a wide range of, various, numerous | name them, or give the number |
| functionality, capabilities | feature, or name it |
| additionally, furthermore, moreover | also, or start a new sentence |
| prior to, subsequent to | before, after |
| in the event that | if |
| at this point in time | now |
| perform the installation, make a decision | install, decide |

Bad:

> The tool leverages a robust caching layer to facilitate seamless retrieval
> of a wide range of artifacts.

Good:

> The tool caches downloaded packages and container images, so the second
> install skips the download.

## Phrases to delete

These carry no information. Delete them and start with the content.

| Kind | Examples |
| --- | --- |
| Openers | "Great question!", "Certainly!", "Sure, here is...", "Let's dive in", "In this section, we will..." |
| Signposts | "It's important to note that", "It's worth mentioning", "Keep in mind that", "Here's the thing" |
| Restating | "As mentioned above", "In other words", "To put it simply", "Essentially" |
| Closers | "In summary", "In conclusion", "Overall", "I hope this helps", "Happy coding!" |
| Empty offers | "Let me know if you have any questions" (offer a next step only when there is a specific one) |

Bad:

> Great question! It's important to note that the cache is cleared on every
> restart. In summary, restarting clears the cache. I hope this helps!

Good:

> Restarting clears the cache.

## Sentence patterns

**Plain "is" and "has".**

- Bad: "The `config` directory serves as the central location for settings."
- Good: "Settings live in `config/`."

**No "not X, but Y" framing** unless you are correcting a real
misconception the reader has.

- Bad: "It's not just a linter, it's a complete code quality platform."
- Good: "It lints and formats Python code."

**No importance tails.** A trailing "-ing" clause that claims significance
adds nothing.

- Bad: "Version 2 adds streaming, highlighting the team's commitment to
  performance."
- Good: "Version 2 adds streaming, which cuts memory use for large files."

**One hedge at most.**

- Bad: "This might potentially cause some issues in certain cases."
- Good: "This fails when the file is larger than 2 GB."

**Name the actor.** Passive voice hides who does what.

- Bad: "Errors are handled and retries are performed."
- Good: "The client retries a failed request three times, then raises
  `TimeoutError`."

**Name the source.** Vague attribution is not evidence.

- Bad: "Experts recommend rotating keys regularly."
- Good: "The AWS security guide recommends rotating access keys every 90
  days."

**List what exists.** Do not pad to three items or trim to three.

- Bad: "It is fast, reliable, and scalable."
- Good: "It handles 10,000 requests per second on one core."

**No rhetorical questions or reveal colons.**

- Bad: "The result? A 40% faster build."
- Good: "The build is 40% faster."

**Verbs, not nouns.**

- Bad: "Perform the configuration of the proxy prior to the execution of the
  tests."
- Good: "Configure the proxy before running the tests."

**One idea per sentence.** If a sentence has more than one "and", "which", or
"while", split it.

- Bad: "The worker reads the queue, which is partitioned by tenant, and
  writes results to S3 while also updating the status table, which the UI
  polls."
- Good: "The worker reads the queue, which is partitioned by tenant. It
  writes results to S3 and updates the status table. The UI polls that
  table."

## Formatting

**No em dashes.** Use a period, comma, colon, or parentheses.

- Bad: "The command is idempotent — running it twice is safe."
- Good: "The command is idempotent: running it twice is safe."

**Bold sparingly.** At most one phrase per section, for something the reader
must not miss, such as a destructive action.

- Bad: "Run **`make build`** to **compile** the **project** before **testing**."
- Good: "Run `make build` before the tests. **It deletes `dist/` first.**"

**No bold labels on every bullet.**

Bad:

```markdown
- **Speed:** It is fast.
- **Safety:** It is safe.
- **Simplicity:** It is simple.
```

Good:

```markdown
- Builds in under a second for projects up to 10,000 files.
- Refuses to overwrite files outside the output directory.
```

**Headings in sentence case, no emoji.**

- Bad: "## 🚀 Getting Started With The CLI"
- Good: "## Get started"

**A heading only when the section has real content.** Do not give each
paragraph its own heading, and do not skip levels (`##` to `####`).

**Tables only for three or more rows** compared on the same columns. Two items
read better as a sentence.

**Code in backticks.** Commands, file names, flags, keys, and values go in
`code` so the reader can tell them from prose.

**No horizontal rules between sections.** Headings already separate them.

## Tone

**State facts, do not promote.**

- Bad: "This groundbreaking feature revolutionizes how you manage configs."
- Good: "You can now reload the config without restarting."

**No flattery or agreement filler.**

- Bad: "You're absolutely right! That's a great point."
- Good: "Yes, the timeout is too short. Raise it to 30 seconds."

**No exclamation marks** in documentation or technical answers.

**Say when you do not know.** One sentence, then what would find out.

- Bad: "This could be due to a variety of factors."
- Good: "I can't tell from this log. Run it with `--verbose` and send the
  lines around the error."
