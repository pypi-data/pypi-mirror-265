import textwrap
import unittest

from metagen.metagenerator import MyMetadata


class TestMyMetadata(unittest.TestCase):

    maxDiff = 1500

    def test_simple(self):
        expected = textwrap.dedent(
            """
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE pkgmetadata SYSTEM 'https://www.gentoo.org/dtd/metadata.dtd'>
            <pkgmetadata>
                <maintainer type="person">
                    <email>pythonhead@gentoo.org</email>
                    <name>Rob Cakebread</name>
                    <description>Maintainer description.</description>
                </maintainer>
            </pkgmetadata>
            """.strip("\n")
        ).replace('    ', '\t')

        metadata = MyMetadata()
        metadata.set_maintainer(["pythonhead@gentoo.org"],
                                ["Rob Cakebread"],
                                ["Maintainer description."],
                                ["person"])
        self.assertEqual(str(metadata), expected)

    def test_long(self):
        expected = textwrap.dedent(
            """
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE pkgmetadata SYSTEM 'https://www.gentoo.org/dtd/metadata.dtd'>
            <pkgmetadata>
                <maintainer type="person">
                    <email>goofy@gentoo.org</email>
                    <name>Goo Fi</name>
                    <description>Maintainer one.</description>
                </maintainer>
                <maintainer type="person">
                    <email>pythonhead@gentoo.org</email>
                    <name>Rob Cakebread</name>
                    <description>Maintainer two</description>
                </maintainer>
                <longdescription>This packages does X Y and Z.</longdescription>
            </pkgmetadata>
            """.strip("\n")
        ).replace('    ', '\t')

        metadata = MyMetadata()
        metadata.set_maintainer(["goofy@gentoo.org", "pythonhead@gentoo.org"],
                                ["Goo Fi", "Rob Cakebread"],
                                ["Maintainer one.", "Maintainer two"],
                                ["person", "person"])
        metadata.set_longdescription("This packages does X Y and Z.")
        self.assertEqual(str(metadata), expected)
