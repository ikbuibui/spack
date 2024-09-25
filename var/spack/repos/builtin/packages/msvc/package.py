# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

import spack.build_systems.compiler
from spack.package import *


class Msvc(Package, CompilerPackage):
    """
    Microsoft Visual C++ is a compiler for the C, C++, C++/CLI and C++/CX programming languages.
    """

    homepage = "https://visualstudio.microsoft.com/vs/features/cplusplus/"

    def install(self, spec, prefix):
        raise InstallError(
            "MSVC compilers are not installable with Spack, but can be "
            "detected on a system where they are externally installed"
        )

    compiler_languages = ["c", "cxx"]
    c_names = ["cl"]
    cxx_names = ["cl"]
    compiler_version_argument = ""
    compiler_version_regex = r"([1-9][0-9]*\.[0-9]*\.[0-9]*)"

    # Named wrapper links within build_env_path
    # Due to the challenges of supporting compiler wrappers
    # in Windows, we leave these blank, and dynamically compute
    # based on proper versions of MSVC from there
    # pending acceptance of #28117 for full support using
    # compiler wrappers
    link_paths = {"c": "", "cxx": "", "fortran": ""}

    @classmethod
    def determine_version(cls, exe):
        # MSVC compiler does not have a proper version argument
        # Errors out and prints version info with no args
        match = re.search(
            cls.compiler_version_regex,
            spack.build_systems.compiler.compiler_output(
                exe, version_argument=None, ignore_errors=1
            ),
        )
        if match:
            return match.group(1)

    @classmethod
    def determine_variants(cls, exes, version_str):
        # MSVC uses same executable for both languages
        spec, extras = super().determine_variants(exes, version_str)
        extras["compilers"]["c"] = extras["compilers"]["cxx"]
        return spec, extras

    @property
    def cc(self):
        if self.spec.external:
            return self.spec.extra_attributes["compilers"]["c"]
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg

    @property
    def cxx(self):
        if self.spec.external:
            return self.spec.extra_attributes["compilers"]["cxx"]
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert self.spec.concrete, msg

    @property
    def fortran(self):
        if self.spec.external:
            return self.spec.extra_attributes["compilers"]["fortran"]
        msg = "cannot retrieve Fortran compiler [spec is not concrete]"
        assert self.spec.concrete, msg
