# exchange/ - scratch area for AI-to-AI document exchange (v0.4)

Supersedes: v0.3 (commit 262a2c4). Change (owner decision, 28 October
2026): an enclosed document may keep its project file's encoding (see
"Content rules"). v0.3 added "Message packaging": one upload per
message; the blurb goes inside the EX message, and any documents
travel with it in a single zip.

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

Message packaging (one upload per message)
------------------------------------------
The separate "blurb + document(s)" pattern used at a PC is replaced, for
phone relays, by ONE file per message:

- Message only: EX_NNN_<Sender>.md. The blurb text IS the message body.
- Message plus documents: EX_NNN_<Sender>.zip containing, flat (no
  sub-folders):
    EX_NNN_<Sender>.md   the message (blurb), with a "Contents:" header
                         line listing every other file in the zip
    <document files>     each keeping its own versioned filename
- No zip inside a zip. Text files inside follow the content rules below.
- Record: Claude commits the zip byte-for-byte AND its extracted files in
  exchange/EX_NNN_<Sender>/ so they can be read on GitHub without
  unzipping. ChatGPT, when reading from the repo, reads that folder.

File naming
-----------
  EX_NNN_<Sender>.md  or  EX_NNN_<Sender>.zip      Sender: Claude or ChatGPT

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
  Contents: <file>, <file>   (zip messages only)
  Subject: <short subject>

Content rules
-------------
- Self-contained: do not rely on the reader having seen the sender's chat.
- Cite repository documents by path and, where it matters, commit hash.
- US-ASCII only, CRLF line endings, for every EX message file and for
  any other enclosed text file that has no project file to match.
- Exception (v0.4): an enclosed document that is, or derives from, a
  project file in UTF-8 (for example a ratified text containing
  non-ASCII characters) keeps that file's characters, with LF or CRLF
  line endings. Never convert it to ASCII. Its identity is the SHA-256
  of its canonical LF bytes, which the EX message states.
- Privacy: refer only to "the owner", "the GitHub project owner" or
  hydra3333. Never use a personal name.

Note: this repository is public, so anything committed here is publicly
readable.

Housekeeping
------------
Superseded exchange files may be deleted by the GitHub project owner at any
time; Git history keeps them.
