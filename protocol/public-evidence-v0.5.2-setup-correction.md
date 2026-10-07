# Setup correction v0.5.2

The six original Scrapy runs failed before probe execution: tmpfs did not permit running pip. Retain them as environment failures. Permit execution on the disposable /tmp mount to install and run the pinned virtual environment. All other isolation, image, wheels, probe code, controls and expected results remain unchanged. Retry only Scrapy in fresh containers, three repetitions per version. This changes setup, not the behavioral hypothesis. Certifi already completed and will not be rerun.
