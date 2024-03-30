import os
import shutil
from tempfile import TemporaryDirectory
import time
from gpyg import GPG, StatusInteractive, ProcessSession

if os.path.exists("./tmp"):
    shutil.rmtree("./tmp")

os.makedirs("./tmp", exist_ok=True)
with TemporaryDirectory(dir="tmp", delete=False) as tmpdir:
    gpg = GPG(homedir=tmpdir, kill_existing_agent=True)
    key = gpg.keys.generate_key("Test Key", passphrase="beans")
    print(key.revoke(passphrase="beans"))
    print(gpg.keys.list_keys())

    """gpg = GPG(homedir=tmpdir, kill_existing_agent=True)
    key = gpg.keys.generate_key("Bongus", passphrase="test")
    key_other = gpg.keys.generate_key("Bingus", passphrase="test")

    print("BONGUS:", key.fingerprint)
    print("BINGUS:", key_other.fingerprint)
    with key.edit(passphrase="test", run_as=key_other.fingerprint) as editor:
        print(editor.sign())

    key.reload()"""
