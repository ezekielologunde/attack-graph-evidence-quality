# Langroid Document fixture correction

Cached runs reached the real import but Document construction failed because metadata is required. No expressions were evaluated. Preserve these setup failures. The v2 probe adds an ordinary DocMetaData instance to each Document; expressions, expected outcomes, package and dependency versions, and limits remain unchanged. Freeze v2 probe/runner hashes in langroid-v2-lock.json before execution. This is a fixture correction, not a change to the sanitizer or expected version distinction.
