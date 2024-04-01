import setuptools
import os.path
import glob

metadata = {
    "__name_program__": "deaotpy",
    "__name_module__": "aot",
    "__version__": "1.3.0",
    "__url__": "https://github.com/yoxu515/aot-benchmark",
    "__description__": "Decoupling Features in Hierarchical Propagation for Video Object Segmentation.",
    "__python_requires__": ">=3.10",
    "__license__": "BSD 3-Clause License",
    "__classifiers__": [
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    "__keywords__": "machine-learning, deep-learning, pytorch, "
                    "vision, object segmentation, video"
}
setup_dir = os.path.dirname(__file__)


def parse_requirements(fname="requirements.txt", with_version=True):
    """Parse the package dependencies listed in a requirements file but strips
    specific versioning information.

    Args:
        fname (str): path to requirements file
        with_version (bool, default=False): if True include version specs

    Returns:
        List[str]: list of requirements items

    CommandLine:
        python -c "import setup; print(setup.parse_requirements())"
    """
    import re
    import sys
    from os.path import exists

    require_fpath = fname

    def parse_line(line):
        """Parse information from a line in a requirements text file."""
        if line.startswith("-r "):
            # Allow specifying requirements in other files
            target = line.split(" ")[1]
            for info in parse_require_file(target):
                yield info
        else:
            info = {"line": line}
            if line.startswith("-e "):
                info["package"] = line.split("#egg=")[1]
            elif "@git+" in line:
                info["package"] = line
            else:
                # Remove versioning from the package
                pat = "(" + "|".join([">=", "==", ">"]) + ")"
                parts = re.split(pat, line, maxsplit=1)
                parts = [p.strip() for p in parts]

                info["package"] = parts[0]
                if len(parts) > 1:
                    op, rest = parts[1:]
                    if ";" in rest:
                        # Handle platform specific dependencies
                        # http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-platform-specific-dependencies
                        version, platform_deps = map(str.strip, rest.split(";"))
                        info["platform_deps"] = platform_deps
                    else:
                        version = rest  # NOQA
                    info["version"] = (op, version)
            yield info

    def parse_require_file(fpath):
        with open(fpath, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    for info in parse_line(line):
                        yield info

    def gen_packages_items():
        if exists(require_fpath):
            for info in parse_require_file(require_fpath):
                parts = [info["package"]]
                if with_version and "version" in info:
                    parts.extend(info["version"])
                if not sys.version.startswith("3.4"):
                    # apparently package_deps are broken in 3.4
                    platform_deps = info.get("platform_deps")
                    if platform_deps is not None:
                        parts.append(";" + platform_deps)
                item = "".join(parts)
                yield item

    def filter_index(packages):

        new_packages = []
        dependency_links = []
        for i, requirement in enumerate(packages):
            if requirement.startswith("--extra-index-url"):
                dependency_links.append(requirement.split()[-1])
            elif requirement.startswith("./dependencies") or requirement.startswith(
                "dependencies"
            ):
                dependency_links.append(requirement)
            else:
                new_packages.append(requirement)

        return new_packages, dependency_links

    packages = list(gen_packages_items())
    packages, dependency_links = filter_index(packages)
    return packages, dependency_links


if __name__ == "__main__":
    with open("README.md", "r") as f:
        long_description = f.read()

    with open("LICENSE", "r", encoding="utf-8") as f:
        license = f.read()

    install_requires, dependency_links = parse_requirements("requirements.txt")

    setuptools.setup(
        name=metadata["__name_program__"],
        version=metadata["__version__"],
        description=metadata["__description__"],
        long_description=long_description,
        long_description_content_type="text/markdown",
        url=metadata["__url__"],
        license=license,
        install_requires=install_requires,
        dependency_links=dependency_links,
        python_requires=metadata["__python_requires__"],
        packages=setuptools.find_packages(),
        include_package_data=True,
        classifiers = metadata["__classifiers__"],
        keywords=metadata["__keywords__"]
    )