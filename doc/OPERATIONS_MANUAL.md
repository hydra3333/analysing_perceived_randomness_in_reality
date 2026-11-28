# Operations manual - where it is

The operations manual of the research system is kept in one place, beside the software it describes:

    a_p_r_i_r_DEV/OPERATIONS_MANUAL.md

That file is the master, in Git, ratified by the owner as RAT-70 (decision log entry 404). `Create_Tree.bat`,
`Install.bat` and `Copy_From_PROD.bat software` put a copy at the root of the QA and PROD trees, so each tree holds
the edition last installed there. Edit only the master; an edit reaches QA and PROD by `Make_Installable.bat INFRA`
and an install, and makes nothing again.

The candidates and the reviewer's review it came from are in `exchange/`
(`Claude_Operations_Manual_v0_1_20261128.md`, `..._v0_2_...`, `ChatGPT_Operations_Manual_v0_1_Review_20261128.md`).
