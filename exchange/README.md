# exchange/ - scratch area for AI-to-AI document exchange (v0.2)

Supersedes: v0.1 (commit 6891196). Changes: adopts the EX_NNN naming
agreed in EX_001/EX_002; records the phone file-upload relay; records
that Claude commits every EX file here as the audit trail.

Purpose
-------
Lets the Claude project chat and the ChatGPT reviewer chat pass
proposals, drafts and reviews to each other when the GitHub project owner
(hydra3333) is away from a PC and cannot easily copy and paste.

Status of anything in this folder
---------------------------------
- NOTHING in exchange/ is authoritative, ratified or binding.
- Only the GitHub project owner (hydra3333) ratifies documents and moves
  them into the main tree (doc/, review/, src/, etc.).
- If anything here conflicts with a document in the main tree, the main
  tree prevails.
- AI chats may commit ONLY inside exchange/. Nothing outside it is touched.

How messages travel
-------------------
- ChatGPT -> Claude: ChatGPT produces a downloadable .md file; the owner
  downloads it and uploads it to the Claude chat. (ChatGPT has no write
  route to this repo; its GitHub connector is read-only.)
- Claude -> ChatGPT: Claude returns a downloadable .md file; the owner
  uploads it to the ChatGPT chat. Alternatively the owner may simply tell
  ChatGPT the EX number, and ChatGPT reads it from exchange/ on main.
- Record: Claude commits every EX file from both sides into exchange/,
  byte-for-byte unchanged, under its EX name, and gives the commit hash.
- Neither AI claims a commit it has not made and identified by hash.

File naming
-----------
  EX_NNN_<Sender>.md      Sender: Claude or ChatGPT

- NNN is ONE shared, increasing, three-digit sequence across both AIs.
  The highest number is the latest message.
- Never overwrite or reuse a number. A correction takes the next number
  and says "Supersedes: EX_NNN".
- Uploads may rename files (e.g. add a prefix). The FIRST LINE of the file
  is authoritative, not the filename. First line format:
    # EX_NNN - <Sender> to <Recipient>

Required header lines (after the first line)
--------------------------------------------
  Date: YYYY-MM-DD
  Project: hydra3333/analysing_perceived_randomness_in_reality
  Replies to: EX_NNN   (or "none")
  Supersedes: EX_NNN   (only if applicable)
  Subject: <short subject>

Content rules
-------------
- Self-contained: do not rely on the reader having seen the sender's chat.
- Cite repository documents by path and, where it matters, commit hash.
- US-ASCII only, CRLF line endings.
- Privacy: refer only to "the owner", "the GitHub project owner" or
  hydra3333. Never use a personal name.

Note: this repository is public, so anything committed here is publicly
readable.

Housekeeping
------------
Superseded exchange files may be deleted by the GitHub project owner at any
time; Git history keeps them.
