# Dependency correction v0.5.3

The first corrected Scrapy setup reached import but failed because its resolved w3lib no longer exported _safe_chars. Pin w3lib 2.2.1 in both version environments; retain all other wheels and original probe. Record exact replacement hashes in scrapy-compatible-lock.json before execution. Preserve prior failures, do not classify them as behavioral observations. Repeat both versions three times under the same corrected isolation.
