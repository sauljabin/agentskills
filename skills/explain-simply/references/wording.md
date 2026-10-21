# Wording rules

Rules for words, phrases, sentences, formatting, and tone, most with a bad
and a good example. They apply to chat answers, documentation, comments, and
commit messages.

## Contents

- [Words](#words)
- [Phrases to delete](#phrases-to-delete)
- [Sentences](#sentences)
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
| crucial, pivotal, vital, groundbreaking, revolutionary, key (as in "a key feature", not a config key) | cut, or state the consequence |
| comprehensive | say what it covers |
| a wide range of, various, numerous | name them, or give the number |
| functionality, capabilities | feature, or name it |
| additionally, furthermore, moreover | also, or start a new sentence |
| prior to, subsequent to | before, after |
| in the event that | if |
| at this point in time | now |
| simply, just, obviously, easily | cut: if the reader finds it hard, these words make them feel slow |

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
| Restating the question | "You're asking why the lag...", "So the question is..." |
| Signposts | "It's important to note that", "It's worth mentioning", "Keep in mind that", "Here's the thing" |
| Restating | "As mentioned above", "In other words", "To put it simply", "Essentially" |
| Closers | "In summary", "In conclusion", "Overall", "I hope this helps", "Happy coding!" |
| Empty offers | "Let me know if you have any questions", "Feel free to ask" |

Bad:

> Great question! It's important to note that the cache is cleared on every
> restart. In summary, restarting clears the cache. I hope this helps!

Good:

> Restarting clears the cache.

## Sentences

### Connect ideas instead of chaining or chopping them

Say how one idea leads to the next with "because", "so", "but", "until", or
"which means". The reader should not have to guess the link between two
sentences.

- Bad (chopped): "The cache is full. Requests slow down. The app times out."
- Good: "When the cache is full, requests slow down until the app times out."

Split a sentence when it chains three or more clauses, or when the reader has
to hold its start in mind to understand its end.

- Bad (chained): "The worker reads the queue, which is partitioned by tenant,
  and writes results to S3 while also updating the status table, which the
  UI polls."
- Good: "The worker reads the queue, which is partitioned by tenant. It
  writes results to S3 and updates the status table, which the UI polls."

### Verbs, not nouns

- Bad: "Perform the configuration of the proxy prior to the execution of the
  tests."
- Good: "Configure the proxy before running the tests."

### Name the actor

Passive voice hides who does what.

- Bad: "Errors are handled and retries are performed."
- Good: "The client retries a failed request three times, then raises
  `TimeoutError`."

### "You", in the present tense

Write instructions to the reader as "you" or as plain commands, and describe
behavior in the present tense.

- Bad: "The user will need to run `make`, which will then generate the
  files."
- Good: "Run `make`. It writes the files to `dist/`."

### One hedge at most

Hedge only when the uncertainty is real, and then once.

- Bad: "This might potentially cause some issues in certain cases."
- Good: "This fails when the file is larger than 2 GB."

### No "not X, but Y" framing

Use it only to correct a misconception the reader actually has.

- Bad: "It's not just a linter, it's a complete code quality platform."
- Good: "It lints and formats Python code."

### No importance tails

A trailing "-ing" clause that claims significance adds nothing. State the
effect instead.

- Bad: "Version 2 adds streaming, highlighting the team's commitment to
  performance."
- Good: "Version 2 adds streaming, which cuts memory use for large files."

### Name the source

Vague attribution is not evidence.

- Bad: "Experts recommend rotating keys regularly."
- Good: "The AWS security guide recommends rotating access keys every 90
  days."

### List what exists

Do not pad a list to three items or trim it to three.

- Bad: "It is fast, reliable, and scalable."
- Good: "It handles 10,000 requests per second on one core."

### No rhetorical questions or reveal colons

- Bad: "The result? A 40% faster build."
- Good: "The build is 40% faster."

## Formatting

### No em dashes

Use a period, comma, colon, or parentheses.

- Bad: "The command is idempotent — running it twice is safe."
- Good: "The command is idempotent: running it twice is safe."

### Bold at most one phrase per section

Save it for something the reader must not miss, such as a destructive
action. Bold labels at the start of every bullet or list item count as bold
on every item.

- Bad: "Run **`make build`** to **compile** the **project** before **testing**."
- Good: "Run `make build` before the tests. **It deletes `dist/` first.**"

Bad:

```markdown
- **Speed:** It is fast.
- **Safety:** It is safe.
```

Good:

```markdown
- Builds in under a second for projects up to 10,000 files.
- Refuses to overwrite files outside the output directory.
```

### Headings

Use sentence case and no emoji. Add a heading only when the section has real
content: do not give each paragraph its own heading, and do not skip levels
(`##` to `####`).

- Bad: "## 🚀 Getting Started With The CLI"
- Good: "## Get started"

### Tables, code, and separators

- Use a table only for three or more rows that compare items on the same
  columns. Two items read better as a sentence.
- Put commands, file names, flags, keys, and values in `code`, so the reader
  can tell them from prose.
- Do not put horizontal rules between sections. Headings already separate
  them.

## Tone

### No flattery, agreement filler, or exclamation marks

- Bad: "You're absolutely right! That's a great point."
- Good: "Yes, the timeout is too short. Raise it to 30 seconds."

### Say when you do not know

One sentence, then what would find out.

- Bad: "This could be due to a variety of factors."
- Good: "I can't tell from this log. Run it with `--verbose` and send the
  lines around the error."

### End with a specific next step, or stop

A closing line earns its place only when it tells the reader what to do or
check next.

- Bad: "Let me know if you have any other questions!"
- Good: "If the lag still grows after offset 2,200, check how long each poll
  takes against `max.poll.interval.ms`."
