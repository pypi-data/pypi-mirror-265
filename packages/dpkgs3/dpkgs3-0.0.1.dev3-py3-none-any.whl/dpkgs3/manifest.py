import gzip
import hashlib
import os
import tempfile
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional, Union

from dpkgs3.package import Package
from dpkgs3.s3 import S3


@dataclass
class Manifest:
    codename: str
    component: str
    architecture: str
    packages: List[Package] = field(default_factory=list, repr=False)
    packages_to_be_uploaded: List[Package] = field(default_factory=list, repr=False)
    packages_to_be_deleted: List[Package] = field(default_factory=list, repr=False)
    files: Dict[str, str] = field(default_factory=dict, repr=False)

    @classmethod
    def retrieve(
        cls,
        s3: S3,
        codename: str,
        component: str,
        architecture: str,
        **kwargs,
    ):
        m = cls(
            codename,
            component,
            architecture,
            **kwargs,
        )
        packages_data = s3.read(
            f"dists/{codename}/{component}/binary-{architecture}/Packages"
        )
        if packages_data is not None:
            m.packages = cls.parse_packages(packages_data.decode("utf-8"))

        return m

    @staticmethod
    def parse_packages(packages_data: str) -> List[Package]:
        packages = []
        for s in packages_data.split("\n\n"):
            if s.rstrip():
                packages.append(Package.parse_string(s))
        return packages

    def add_package(
        self,
        pkg: Package,
        preserve_versions: bool = True,
        fail_if_exists: bool = True,
        dry_run: bool = False,
    ):
        if fail_if_exists:
            for p in self.packages:
                if (
                    p.name == pkg.name
                    and p.full_version == pkg.full_version
                    and os.path.basename(p.url_filename(self.codename))
                    == os.path.basename(pkg.url_filename(self.codename))
                ):
                    raise Exception(
                        f"package {pkg.name}_{pkg.full_version} already exists with filename ({p.url_filename(self.codename)})"
                    )

        if not dry_run:
            self.packages = [
                p
                for p in self.packages
                if not (
                    p.name == pkg.name
                    and (
                        p.full_version == pkg.full_version
                        if preserve_versions
                        else True
                    )
                )
            ]
            self.packages.append(pkg)
            self.packages_to_be_uploaded.append(pkg)

        return pkg

    def delete_package(
        self,
        pkg_name: str,
        versions: Optional[List[str]] = None,
        dry_run: bool = False,
    ):
        deleted_packages: List[Package] = []
        versions = versions if versions is not None else []
        for p in self.packages:
            possible_versions = [
                p.version,
                p.full_version,
                f"{p.version}-{p.iteration}",
            ]
            if p.name == pkg_name and any(
                [possible_version in versions for possible_version in possible_versions]
            ):
                deleted_packages.append(p)

        if not dry_run:
            self.packages = [
                package for package in self.packages if package not in deleted_packages
            ]
            self.packages_to_be_deleted.extend(deleted_packages)
        return deleted_packages

    def generate(self):
        return "\n".join([package.generate(self.codename) for package in self.packages])

    def write_to_s3(
        self,
        s3: S3,
        cache_control: Union[str, None] = None,
        fail_if_exists: bool = False,
    ):
        manifest = self.generate()

        # actually upload packages supposed to be uploaded
        for pkg in self.packages_to_be_uploaded:
            assert pkg.filename is not None
            s3.store(
                pkg.filename,
                pkg.url_filename(self.codename),
                "application/x-debian-package",
                cache_control=cache_control,
                fail_if_exists=fail_if_exists,
            )
        self.packages_to_be_uploaded = []

        # actually delete packages supposed to be deleted
        for pkg in self.packages_to_be_deleted:
            s3.remove(pkg.url_filename(self.codename))
        self.packages_to_be_deleted = []

        # generate the Packages file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as pkgs_temp:
            pkgs_temp.write(manifest)
            pkgs_temp.close()
            f = f"dists/{self.codename}/{self.component}/binary-{self.architecture}/Packages"
            s3.store(
                pkgs_temp.name,
                f,
                "text/plain; charset=utf-8",
                cache_control=cache_control,
                fail_if_exists=fail_if_exists,
            )
            self.files[f"{self.component}/binary-{self.architecture}/Packages"] = (
                self.hashfile(pkgs_temp.name)
            )
            os.unlink(pkgs_temp.name)

        # generate the Packages.gz file
        with tempfile.NamedTemporaryFile(delete=False) as gztemp:
            gztemp.close()
            with gzip.open(gztemp.name, "wb") as gz:
                gz.write(manifest.encode("utf-8"))
            f = f"dists/{self.codename}/{self.component}/binary-{self.architecture}/Packages.gz"
            s3.store(
                gztemp.name,
                f,
                "application/x-gzip",
                cache_control=cache_control,
                fail_if_exists=fail_if_exists,
            )
            self.files[f"{self.component}/binary-{self.architecture}/Packages.gz"] = (
                self.hashfile(gztemp.name)
            )
            os.unlink(gztemp.name)

    @staticmethod
    def hashfile(path: str):
        data: Dict[str, Any] = {}
        data["size"] = os.path.getsize(path)

        with open(path, "rb") as f:
            content = f.read()
            data["sha1"] = hashlib.sha1(content).hexdigest()
            data["sha256"] = hashlib.sha256(content).hexdigest()
            data["md5"] = hashlib.md5(content).hexdigest()

        return data
