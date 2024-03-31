"""Handles the changelog."""
from .changelogEntry import ChangelogEntry
from .version import Version


class Changelog:
    """Contains the Owega Changelog."""

    def __init__(self):
        """Initialize the changelog."""
        self.logs = []
        self.log = ""
        self.version = Version(0, 0, 0)
        self.initLogs()
        self.genLog()

    def initLogs(self):
        """Fill the changelog."""
        self.logs.append(
            ChangelogEntry(1, 0, 0)
            .addLine("Geemlib initial version")
        )

    def genLog(self):
        """Generate the changelog string."""
        self.logs.sort()
        self.version = self.logs[-1].version
        self.version_str = str(self.logs[-1].version)
        self.log = f"OWEGA v{self.version_str} CHANGELOG:"
        for entry in self.logs:
            ver = entry.version
            if (not ver.status) and ver.patch == 0:
                self.log += '\n'
                if ver.minor == 0:
                    self.log += '\n'
            self.log += '\n'
            if 'rc' in ver.status:
                self.log += '\033[91m'
            self.log += str(entry)
            if 'rc' in ver.status:
                self.log += '\033[m'


GeemlibChangelog = Changelog()
