# a_p_r_i_r_DEV - the living research system (DEV tree)

This folder is the DEV tree of the research system as the simple scheme describes it
(`exchange/Claude_The_Simple_Scheme_v0_2_20261126.md`, agreed by the project owner on 26 November 2026). It has the
same shape as the QA tree (`T:\a_p_r_i_r_QA`) and the PROD tree (`G:\a_p_r_i_r_PROD`), plus `deploy\` and
`tests\`. Everything outside this folder, at the top of the repository, is the old system and the present engine,
frozen as the reference for the comparison of the scheme's section 9.

**Step 1 (this commit): a byte-for-byte copy** of the present engine, its 40 methods in 12 families, the shared
helpers, the launchers, the owner's environment scripts and the engine's eight test modules. Nothing in it is
changed yet; the simplification is step 2. Some files are here only because the copied tests use them as oracles
of the old system, and step 2 removes them when the comparison of section 9 replaces those tests:
`src\methods\_common\contract_data\declarations\`, and in `src\methods\_common\` the modules
`contract_dispatch`, `contract_publication`, `contract_receipts`, `contract_registry`, `contract_runner`,
`game_draws_reader`, `master_versions` and `owner_records`.

**Not kept in Git** (see `.gitignore` here): this tree's `ENVIRONMENT.ini`, `.venv`, `source_data`, `results`,
`records`, `scratch` and `transitory_data`.

**Its Python environment** is built in this folder by the two scripts that lie in it, run in a plain CMD window
with no environment active: `create_venv.bat`, then `install_upgrade_dependencies_into_venv.bat`. Each works on the
folder it lies in.
