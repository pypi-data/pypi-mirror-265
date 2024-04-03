# SPDX-License-Identifier: GPL-3.0-or-later
# vim: et:ts=4
#
# This is the setup script for Rubber. It acts both as a part of the
# configuration script a la autoconf and as a setup script a la Distutils.
#
# Copyright 2002-2006 Emmanuel Beffara
# Copyright 2015-2015 Sebastian Kapfer
# Copyright 2015-2015 Nicolas Boulenguez

import logging
import os.path
import re
import shutil
from setuptools import Command, setup
from setuptools.command.build import build as BuildCommand
from setuptools.command.install import install as InstallCommand

project_root_dir = os.path.dirname(__file__)

# A file f is generated from f.in by replacing @author@, @version@ by
# sensible values (as ./configure does in the autoconf world).
files_with_substitutions = (
    os.path.join("doc", "man-en", "rubber.1"),
    os.path.join("doc", "man-en", "rubber-info.1"),
    os.path.join("doc", "man-fr", "rubber.1"),
    os.path.join("doc", "man-fr", "rubber-info.1"),
    os.path.join("doc", "rubber.texi"),
    os.path.join("rubber", "version.py"),
)

manual_basename = os.path.join("doc", "rubber.")
doc_recipes = (
    ("html", ("makeinfo", "--html", "--no-split")),
    ("info", ("makeinfo", "--info")),
    ("pdf", ("texi2dvi", "--pdf", "--quiet", "--tidy")),
    ("txt", ("makeinfo", "--plaintext")),
)


class build(BuildCommand):
    man = False
    info = False
    html = False
    pdf = False
    txt = False
    user_options = BuildCommand.user_options + [
        ("man=", None, "build Manpages [{default}]".format(default=man)),
        ("info=", None, "build Info documentation [{default}]".format(default=info)),
        ("html=", None, "format HTML documentation [{default}]".format(default=html)),
        ("pdf=", None, "format PDF documentation [{default}]".format(default=pdf)),
        ("txt=", None, "format plain text documentation [{default}]".format(default=txt)),
    ]

    @staticmethod
    def _distutils_util_strtobool(val):
        """Convert a string representation of truth to true (1) or false (0).

        True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
        are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
        'val' is anything else.
        """
        val = val.lower()
        if val in ('y', 'yes', 't', 'true', 'on', '1'):
            return 1
        elif val in ('n', 'no', 'f', 'false', 'off', '0'):
            return 0
        else:
            raise ValueError("invalid truth value {!r}".format(val))

    def finalize_options(self):
        super().finalize_options()
        for fmt in ['man'] + [fmt for fmt, recipe in doc_recipes]:
            value = getattr(self, fmt)
            if type(value) is str:
                value = self._distutils_util_strtobool(value)
                setattr(self, fmt, value)

    def generate_files_with_substitutions(self, subs):
        pattern = "|".join(subs.keys())
        pattern = "@(" + pattern + ")@"
        pattern = re.compile(pattern)

        def repl(match_object):
            return subs[match_object.group(1)]

        def func(in_path, out_path):
            # Rubber sources are encoded in utf_8.
            with open(in_path, encoding='utf-8') as in_file:
                with open(out_path, "w", encoding='utf-8') as out_file:
                    for in_line in in_file:
                        out_line = pattern.sub(repl, in_line)
                        out_file.write(out_line)

        for out_path in files_with_substitutions:
            if re.match('.*man-??.*\\.1', out_path) and not self.man:
                continue
            in_path = out_path + ".in"
            self.make_file(in_path, out_path, func, (in_path, out_path))

    def generate_documentation(self):
        infile = manual_basename + "texi"
        for fmt, recipe in doc_recipes:
            if getattr(self, fmt):
                outfile = manual_basename + fmt
                cmd = recipe + ("--output=" + outfile, infile)
                self.make_file(infile, outfile, self.spawn, (cmd,))

    def run(self):
        subs = {}
        for v in ("author", "author_email", "maintainer", "maintainer_email", "url", "version"):
            subs[v] = getattr(self.distribution.metadata, "get_" + v)()
        self.generate_files_with_substitutions(subs)

        super().run()

        self.generate_documentation()


class install(InstallCommand):

    mandir = "$base/man"
    infodir = "$base/info"
    docdir = "$base/share/doc/rubber"
    user_options = InstallCommand.user_options + [
        ("mandir=", None,
         "installation directory for manual pages [{default}]".format(default=mandir)),
        ("infodir=", None,
         "installation directory for info manuals [{default}]".format(default=infodir)),
        ("docdir=", None,
         "installation directory for other documentation [{default}]".format(default=docdir)),
    ]

    def finalize_options(self):
        super().finalize_options()
        self._expand_attrs(("mandir", "infodir", "docdir"))

    def run(self):
        build = self.get_finalized_command("build")
        assert self.distribution.data_files is None
        self.distribution.data_files = []
        if build.man:
            self.distribution.data_files = [(self.mandir + "/man1", (
                "doc/man-en/rubber.1",
                "doc/man-en/rubber-info.1",
                "doc/man-en/rubber-pipe.1",
            )),
                                            (self.mandir + "/fr/man1", (
                                                "doc/man-fr/rubber.1",
                                                "doc/man-fr/rubber-info.1",
                                                "doc/man-fr/rubber-pipe.1",
                                            ))]
        if build.info:
            infodocs = (manual_basename + "info",)
            self.distribution.data_files.append((self.infodir, infodocs))
        otherdocs = [manual_basename + f for f in ("html", "pdf", "txt") if getattr(build, f)]
        if len(otherdocs) > 0:
            self.distribution.data_files.append((self.docdir, otherdocs))
        super().run()


class clean(Command):
    description = "clean up temporary files from 'build' command"
    user_options = [
        ('build-base=', 'b', "base build directory (default: 'build')"),
        ('all', 'a', "remove all build output, not just temporary by-products"),
    ]

    def initialize_options(self):
        self.build_base = None
        self.all = None

    def finalize_options(self):
        self.set_undefined_options(
            'build',
            ('build_base', 'build_base'),
        )

    def remove_tree(self, path):
        if os.path.exists(path):
            logging.info("removing '%s'", path)
            if not self.dry_run:
                shutil.rmtree(path)
        else:
            logging.debug("'%s' does not exist -- can't clean it", path)

    def remove_file(self, path):
        if os.path.exists(path):
            logging.info("removing '%s'", path)
            if not self.dry_run:
                os.remove(path)

    def run(self):
        try:
            self.remove_tree(self.build_base)
        except OSError:
            pass

        if self.all:
            for f in files_with_substitutions:
                self.remove_file(f)

        for fmt, _ in doc_recipes:
            self.remove_file(manual_basename + fmt)
        self.remove_tree("rubber.t2d")

        for dirpath, dirnames, filenames in os.walk(os.curdir):
            for venv in ('.venv', 'venv'):
                if venv in dirnames:
                    dirnames.remove(venv)

            for filename in filenames:
                ew = filename.endswith
                if ew("~") or ew(".pyc") or ew(".pyo"):
                    self.remove_file(os.path.join(dirpath, filename))

        self.remove_tree(os.path.join("tests", "tmp"))


class tar(Command):
    description = "wrapper for git archive"
    user_options = [
        ("revision=", None, "git tree-ish [HEAD]"),
        ("extension=", None, "archive extension [tar.gz]"),
    ]
    revision = "HEAD"
    extension = "tar.gz"

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        version = self.distribution.metadata.get_version()
        self.spawn(("git", "archive", self.revision, "-9", "--prefix=rubber-" + version + "/",
                    "--output=rubber-" + version + "." + self.extension))


def extract_version():
    with open("NEWS", "r") as f:
        while True:
            line = f.readline()
            if line.startswith("Version"):
                break
    match = re.match(r'^Version ([0-9.]+) ', line)
    version = match.group(1)

    return version


setup(
    name="latex-rubber",
    version=extract_version(),
    description="an automated system for building LaTeX documents",
    long_description="""\
This is a building system for LaTeX documents. It is based on a routine that
runs just as many compilations as necessary. The module system provides a
great flexibility that virtually allows support for any package with no user
intervention, as well as pre- and post-processing of the document. The
standard modules currently provide support for bibtex, dvips, dvipdfm, pdftex,
makeindex. A good number of standard packages are supported, including
graphics/graphicx (with automatic conversion between various formats and
Metapost compilation).\
""",
    author='Sebastian Kapfer',
    author_email='sebastian.kapfer@fau.de',
    maintainer='Florian Schmaus',
    maintainer_email='flo@geekplace.eu',
    url='https://gitlab.com/latex-rubber/rubber',
    license="GPL",
    python_requires='>=3.8',
    packages=(
        "rubber",
        "rubber.converters",
        "rubber.latex_modules",
    ),
    package_dir={
        "rubber": "rubber",
    },
    package_data={
        "rubber": ["rules.ini"],
    },
    scripts=(
        "bin/rubber",
        "bin/rubber-info",
        "bin/rubber-lsmod",
        "bin/rubber-pipe",
    ),
    cmdclass={
        "build": build,
        "install": install,
        "clean": clean,
        "tar": tar,
    },
)
