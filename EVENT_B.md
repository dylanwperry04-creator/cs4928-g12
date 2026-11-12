# Event B: prediction (recorded before analysis)

Pre-Event-B state: Week 9 design review in README.md (commit 41a203a), tagged PRE_EVENT_B on 12 Nov 2026. The tag was created after the Event B brief was opened; the Week 9 decision itself was committed on 3 Nov and has not been changed.

Pressure: a public API or type referenced by the code or comments is renamed. We test this on the 2022 Preferences.java by applying IDE-style renames (code changed, comments untouched) to identifiers that surviving comments mention, and by checking the ActionBar to Toolbar migration already visible in the 2022 code.

Prediction: comments that name a code identifier will drift after a rename, because IDE renames do not update comment text. The comments Week 9 kept (section dividers and "Reset toolbar button customizations") do not name identifiers, so we expect them to be unaffected. We expect 1 to 4 of the 37 surviving comments to name an identifier, and these sit outside the Week 9 set. So we expect the Week 9 decision to be only partly supported: it removes duplicated "what" comments, but does not protect comments that name identifiers. That needs an automated check, not more structural changed
