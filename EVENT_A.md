# Event A: held-out material and prediction (recorded before running)

Held-out snapshot: AnkiDroid Preferences.java at commit 9db834afd0 (28 Feb 2022), the last Java version before conversion to Kotlin.
M2 snapshot: commit 79163e4b57 (4 May 2021), identified by matching the dataset's source hash.

Cases: the 50 M2 comments, located in the later file by exact comment text. Comments not found are recorded as removed, not replaced.
Method: unchanged from M2. Same prompt, GPT-6 High in ChatGPT Temporary Chats, batches of 10 with 20/30 lines of context, same scorer and decision rule.

Prediction: most comments (40+) survive. Accuracy and MCC on surviving comments stay within ±0.10 of M2 (0.66 / 0.58). 2-5 comments become stale or misaligned where the code around them changed, and the model will not flag most of these.

What would challenge our M2 conclusion: accuracy or MCC dropping by more than 0.10, or the model giving a different label to more than 30% of unchanged comments.