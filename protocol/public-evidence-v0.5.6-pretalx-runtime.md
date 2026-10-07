# pretalx runtime preparation correction

The Python 3.11 source builds for both selected versions failed while compiling reportlab because the slim image has no C compiler. Retain both failures. Before any pretalx behavioral collection, retry preparation on the already pinned Python 3.9 image used for certifi, which may provide compatible historical binary dependencies. Use the same 300-second limits and isolation as amendment v0.5.4. This changes a preparation environment, not a measured outcome or version selection. No success is assumed.
