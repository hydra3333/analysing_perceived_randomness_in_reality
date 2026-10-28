# exchange/ - scratch area for AI-to-AI document exchange (v0.1)

Purpose
-------
A drop folder that lets the Claude chat and the ChatGPT reviewer chat pass
proposals, drafts and reviews to each other when the GitHub project owner
(hydra3333) is away from a PC and cannot easily download, upload or paste.

Status of anything in this folder
---------------------------------
- NOTHING in exchange/ is authoritative, ratified or binding.
- Only the GitHub project owner (hydra3333) ratifies documents and moves
  them into the main tree (doc/, review/, src/, etc.).
- If anything here conflicts with a document in the main tree, the main
  tree prevails.
- AI chats may commit ONLY inside exchange/. Nothing outside it is touched.

Who can write
-------------
- Claude: can commit here (via the Claude GitHub App, scoped to this repo).
- ChatGPT: can read this repository through its GitHub connector, but its
  standard chat connector is read-only. ChatGPT reviews therefore reach
  Claude through the GitHub project owner unless and until a write route
  is set up.

File naming
-----------
  <FROM>_<TO>_<Topic>_v<major>_<minor>_<YYYYMMDD>.md

  FROM / TO : CLAUDE or CHATGPT
  Example   : CLAUDE_CHATGPT_Exchange_Folder_Test_v0_1_20261028.md

- The version is always in the filename; never overwrite a sent version,
  emit a new one instead.
- A reply names the file it responds to in its first lines.

Encoding
--------
US-ASCII only, CRLF line endings.

Privacy
-------
Do not name the GitHub project owner in any file here; refer to "the GitHub
project owner" or hydra3333.

Note: this repository is public, so anything committed here is publicly
readable.

Housekeeping
------------
Superseded exchange files may be deleted by the GitHub project owner at any
time; Git history keeps them.
