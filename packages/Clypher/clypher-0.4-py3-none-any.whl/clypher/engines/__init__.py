"""
Engines combine an encryptor and a file handler into a single interface.
Their job is to provide a simple way of encrypting and decrypting data.

When adding a new engine, add it to INSTALLED_ENGINES using the following format:
"enginename": "path.to.engine.Class"

All engines should inherit from BaseEngine

Once added, it can automatically be imported by the main app when needed.
"""

INSTALLED_ENGINES = {
    "fernet": "clypher.engines.fernet_engine.FernetEngine",
    
    #Add any new engines here
}