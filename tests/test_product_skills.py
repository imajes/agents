"""Exercise skill maintenance on local Git repositories, including fresh clones."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/product_skills.py"


class ProductSkillsTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.provider = self.base / "provider"
        self.library = self.base / "library"
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
                        GIT_ALLOW_PROTOCOL="file", GIT_AUTHOR_NAME="Test", GIT_COMMITTER_NAME="Test",
                        GIT_AUTHOR_EMAIL="test@example.invalid", GIT_COMMITTER_EMAIL="test@example.invalid")
        for repo in (self.provider, self.library):
            self.git(self.base, "init", "-q", "-b", "main", repo)
        self.source = self.provider / "skills/example/SKILL.md"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("---\nname: example\ndescription: Test skill\n---\n")
        self.git(self.provider, "add", ".")
        self.git(self.provider, "commit", "-qm", "Add test skill")
        self.git(self.library, "submodule", "add", "-q", "-b", "main", self.provider, "upstream/test")
        (self.library / "scripts").mkdir()
        shutil.copyfile(SCRIPT, self.library / "scripts/product_skills.py")
        self.run_skill("enable", "test", "skills/example")
        self.git(self.library, "add", ".")
        self.git(self.library, "commit", "-qm", "Pin and link skill")
        self.link = self.library / "skills/product/test/example"

    def git(self, repo, *args):
        return subprocess.run(["git", "-C", repo, *args], env=self.env, check=True,
                              text=True, capture_output=True).stdout.strip()

    def run_skill(self, *args, repo=None, success=True):
        result = subprocess.run([sys.executable, (repo or self.library) / "scripts/product_skills.py", *args],
                                env=self.env, text=True, capture_output=True)
        self.assertEqual(result.returncode == 0, success, result.stderr)
        return result

    def test_fresh_clone_and_link_lifecycle(self):
        clone = self.base / "fresh"
        self.git(self.base, "clone", "-q", self.library, clone)
        self.run_skill("init", repo=clone)
        self.assertIn("skills/example", self.run_skill("list", repo=clone).stdout)
        self.assertFalse(self.link.readlink().is_absolute())
        self.run_skill("disable", "test", "example")
        self.assertFalse(self.link.exists())
        self.assertTrue(self.source.is_file())
        self.run_skill("enable", "test", "../outside", success=False)
        self.run_skill("enable", "test", "skills/example")
        self.run_skill("enable", "test", "skills/example")
        self.run_skill("check")
        self.link.unlink()
        self.link.mkdir()
        self.run_skill("disable", "test", "example", success=False)
        self.assertTrue(self.link.is_dir())

    def test_update_checks_pin_and_published_skill_before_switching(self):
        checkout = self.library / "upstream/test"
        initial = self.git(checkout, "rev-parse", "HEAD")
        (checkout / "pending").touch()
        self.run_skill("update", "test", success=False)
        (checkout / "pending").unlink()
        self.source.write_text(self.source.read_text() + "New content\n")
        self.git(self.provider, "commit", "-qam", "Extend example")
        self.run_skill("update", "test")
        new = self.git(self.provider, "rev-parse", "HEAD")
        self.assertNotEqual(initial, new)
        self.assertEqual(self.git(checkout, "rev-parse", "HEAD"), new)
        self.run_skill("update", "test", success=False)
        self.git(self.library, "add", "upstream/test")
        self.source.unlink()
        self.git(self.provider, "commit", "-qam", "Retire example")
        self.run_skill("update", "test", success=False)
        self.assertEqual(self.git(checkout, "rev-parse", "HEAD"), new)
        self.run_skill("check")


if __name__ == "__main__":
    unittest.main()
