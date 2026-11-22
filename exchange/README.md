# exchange/ - where the two AI chats exchange documents, and where the working records live (v0.6)

Supersedes: v0.5 (1 November 2026; in Git history). Changes in v0.6 (Claude,
22 November 2026, at the owner's request, bringing this file into line
with practice since the owner's approach of 16 November 2026 came into
force at RAT-34): the reviewer commits its own files; Claude also commits
reviewed and ratified documents into doc/; most messages are now a single
.md file that names its documents by repository path and hash; not every
message is an EX message; the decision log and the continuity page live
here. No rule is changed by this edition: it describes what is done.
The handovers (doc/HANDOVER/) and the owner's decisions prevail over
this file wherever they differ.

Purpose
-------
Lets the Claude project chat (primary designer and coder) and the ChatGPT
reviewer chat (independent reviewer) pass proposals, drafts and reviews to
each other through the repository, with the GitHub project owner
(hydra3333) relaying between them and deciding.

Status of anything in this folder
---------------------------------
- Nothing in exchange/ is ratified or binding by being here. Only the
  GitHub project owner (hydra3333) ratifies. The ratified documents are
  in doc/.
- If anything here conflicts with a ratified document in doc/, the
  ratified document prevails.
- Two living records are kept here by Claude (working approach P0 and P2,
  14 November 2026):
    DECISIONS/DECISION_LOG.md   the owner's decisions, in his own words;
                                append-only, numbered; a correction is a
                                new entry. US-ASCII, LF.
    CONTINUITY_NOW.md           the one page that says where things stand
                                and how to restart either chat.
- Also here: the owner's two working lists (OWNER_ROADMAP.md,
  OWNER_REMINDERS.md; CRLF, US-ASCII; not rules), the owner's run records
  (RUNS/), and Claude's working tools and drafts (CLAUDE_WEB_TOOLS/, with
  a README).

Who commits what (owner, 16 November 2026; in force from RAT-34)
----------------------------------------------------------------
- The Claude chat commits and pushes documents and records itself: named
  paths only, after a fetch and a fast-forward, with nothing deleted or
  overwritten. Freely under exchange/ and CLAUDE_CODE_WORKING_FOLDER_TREE/;
  into doc/ only once a document is reviewed and ratified. Never code or
  tests into src/ or tests/ (those travel as a reviewed package that the
  owner installs), and never anything under source_data/, results/,
  transitory_data/ or GAIS/.
- The ChatGPT reviewer chat commits its own EX replies and handbacks into
  exchange/, and its own handover files into doc/HANDOVER/.
- Neither chat edits the other's files. Each fetches before reading or
  numbering anything.
- Neither AI claims a commit it has not made and identified by hash.

How messages travel
-------------------
- The author commits its message to exchange/ on main. The owner tells
  the other chat, usually with a short paste-ready block that names the
  file and the commit; the other chat reads it from GitHub.
- When the owner is away from a PC he may instead carry a downloaded
  .md file or zip from one chat to the other; the author still commits it.
- The owner's rule (21 November 2026): Claude discusses the owner's
  queries with him first and issues or revises an EX message only when he
  asks.

Messages that are not EX messages
---------------------------------
- A short note relayed by the owner in a paste block ("not an EX").
- The reviewer's handbacks: exchange/ChatGPT_to_Claude_<subject>_<date>.md.
- A reviewer reply that the owner pastes without a number: Claude files it
  under the last EX number with a letter suffix (EX_203A), never under
  the next free number.
The decision log records each of these with its source.

EX messages: packaging
----------------------
- Message only: EX_NNN_<Sender>.md. This is the usual form. The documents
  it concerns stay at their repository paths and are named by path and
  SHA-256 in a table at the end of the message.
- Message plus a code package: EX_NNN_<Sender>.zip containing, flat (no
  sub-folders):
    EX_NNN_<Sender>.md   the message, with a "Contents:" header line
                         listing every other file in the zip
    <document files>     each keeping its own versioned filename
  No zip inside a zip, with one exception: an install package travels as
  its own zip member (built deterministically), with its member list as
  a second member. The author commits the zip byte for byte AND its
  extracted files in exchange/EX_NNN_<Sender>/, so that they can be read
  on GitHub without unzipping.

File naming
-----------
  EX_NNN_<Sender>.md  or  EX_NNN_<Sender>.zip      Sender: Claude or ChatGPT

- NNN is ONE shared, increasing, three-digit sequence across both AIs.
  The highest number is the latest message. Fetch, then check the highest
  committed number, before taking the next.
- Never overwrite or reuse a number. A correction takes the next number
  and says "Supersedes: EX_NNN". (Exception, by the owner's own
  instruction only: he had EX_263 revised in place under its number.)
- The FIRST LINE of the file is authoritative, not the filename:
    # EX_NNN - <Sender> to <Recipient>

Required header lines (after the first line)
--------------------------------------------
  Date: YYYY-MM-DD
  Project: hydra3333/analysing_perceived_randomness_in_reality
  Replies to: EX_NNN   (or "none")
  Supersedes: EX_NNN   (only if applicable)
  Contents: <file>, <file>   (zip messages only)
  Subject: <short subject>

Content rules
-------------
- Self-contained: do not rely on the reader having seen the sender's chat.
- A reply opens with the disposition of every finding it answers, and says
  which number the reply to it should take.
- Cite repository documents by path and, where it matters, commit hash
  and SHA-256. Hashes are computed by a tool and copied, never typed.
- End with a table of the files the message names (path, SHA-256) and, at
  a milestone, a short "how the process went" note (working approach P6).
- US-ASCII only, CRLF line endings, for every EX message file and for
  any other enclosed text file that has no project file to match.
- Exception (v0.4): an enclosed document that is, or derives from, a
  project file in UTF-8 keeps that file's characters, with LF or CRLF
  line endings. Never convert it to ASCII. Its identity is the SHA-256
  of its canonical LF bytes, which the EX message states.
- Use the project's own words: restore from backup, catch-up,
  walk-forward, historical walk-forward rerun. A finding code is
  explained in plain words when it is put to the owner.
- Privacy: refer only to "the owner", "the GitHub project owner" or
  hydra3333. Never use a personal name.

Note: this repository is public, so anything committed here is publicly
readable.

Housekeeping
------------
Nothing here is deleted or overwritten by an AI chat. Superseded
exchange files may be deleted by the GitHub project owner at any time;
Git history keeps them.
