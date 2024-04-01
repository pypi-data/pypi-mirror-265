import os
from pathlib import Path
from typing import Dict, List, Optional

import click
from dpkgs3.s3 import S3
from dpkgs3.release import Release
from dpkgs3.manifest import Manifest
from dpkgs3.package import Package


def configure_s3_client(
    s3_bucket: str,
    s3_prefix: Optional[str],
    s3_visibility: str,
    s3_encryption: bool,
    aws_default_region: Optional[str],
    aws_access_key_id: Optional[str],
    aws_secret_access_key: Optional[str],
):
    if aws_default_region is not None:
        os.environ.setdefault("AWS_DEFAULT_REGION", aws_default_region)
    if aws_access_key_id is not None:
        os.environ.setdefault("AWS_ACCESS_KEY_ID", aws_access_key_id)
    if aws_secret_access_key is not None:
        os.environ.setdefault("AWS_SECRET_ACCESS_KEY", aws_secret_access_key)

    s3 = S3(
        bucket=s3_bucket,
        prefix=s3_prefix,
        access_policy=s3_visibility,
        encryption=s3_encryption,
    )
    return s3


def add_common_options():
    common_options = [
        click.option(
            "--codename",
            default="stable",
            show_default=True,
            help="The codename of the APT repository",
        ),
        click.option(
            "--component",
            default="main",
            show_default=True,
            help="The component of the APT repository",
        ),
        click.option("--s3-bucket", required=True, help="S3 bucket name"),
        click.option(
            "--s3-prefix",
            default="",
            show_default=True,
            help="Path prefix to use when storing on S3",
        ),
        click.option(
            "--s3-visibility",
            type=click.Choice(
                choices=[
                    "public-read",
                    "private",
                    "authenticated-read",
                    "bucket-owner-full-control",
                ]
            ),
            default="public-read",
            show_default=True,
            help="The access policy for the uploaded files",
        ),
        click.option(
            "--s3-encryption",
            is_flag=True,
            default=False,
            show_default=True,
            help="Use S3 server side encryption",
        ),
        click.option(
            "--s3-cache-control",
            default=None,
            help="Cache-Control headers to add to S3 objects",
        ),
        click.option("--aws-default-region", default=None, help="AWS default region"),
        click.option("--aws-access-key-id", default=None, help="AWS Access Key ID"),
        click.option(
            "--aws-secret-access-key", default=None, help="AWS Secret Access Key"
        ),
    ]

    def inner(func):
        for option in reversed(common_options):
            func = option(func)
        return func

    return inner


@click.group()
def cli(**kwargs):
    pass


@cli.command()
@add_common_options()
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    show_default=True,
    help="Shows all package information in original format",
)
@click.option(
    "-a",
    "--architecture",
    default="all",
    show_default=True,
    help="The architecture of the package in the APT repository. Use 'all' to list all architectures.",
)
def list(
    verbose: bool,
    architecture: str,
    codename: str,
    component: str,
    s3_bucket: str,
    s3_prefix: str,
    s3_visibility: str,
    s3_encryption: bool,
    s3_cache_control: Optional[str],
    aws_default_region: Optional[str],
    aws_access_key_id: Optional[str],
    aws_secret_access_key: Optional[str],
):
    s3 = configure_s3_client(
        s3_bucket,
        s3_prefix,
        s3_visibility,
        s3_encryption,
        aws_default_region,
        aws_access_key_id,
        aws_secret_access_key,
    )
    release = Release.retrieve(
        s3=s3,
        codename=codename,
    )
    if architecture.lower() == "all":
        archs = release.architectures
    else:
        archs = [arch for arch in release.architectures if arch == architecture.lower()]

    packages: List[Package] = []
    for arch in archs:
        manifest = Manifest.retrieve(
            s3=s3,
            codename=codename,
            component=component,
            architecture=arch,
        )
        packages.extend(manifest.packages)

    if verbose:
        for pkg in packages:
            print(pkg.generate(codename=codename), end="\n\n")
        return

    max_pkg_name_len = max([len(pkg.name) for pkg in packages])
    max_pkg_ver_len = max([len(pkg.version) for pkg in packages])
    for pkg in packages:
        print(
            pkg.name.ljust(max_pkg_name_len + 2)
            + pkg.version.ljust(max_pkg_ver_len + 2)
            + pkg.architecture
        )


@cli.command()
@add_common_options()
@click.option(
    "--preserve-versions",
    is_flag=True,
    default=True,
    show_default=True,
    help="Whether to preserve other versions of a package in the repository when uploading one",
)
@click.option(
    "--fail-if-exists",
    is_flag=True,
    default=False,
    show_default=True,
    help="Whether to preserve other versions of a package in the repository when uploading one",
)
@click.option(
    "--dry-run", is_flag=True, default=False, show_default=True, help="Flag for DRY run"
)
@click.argument(
    "files", nargs=-1, type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
def upload(
    files: List[Path],
    codename: str,
    component: str,
    preserve_versions: bool,
    fail_if_exists: bool,
    dry_run: bool,
    s3_bucket: str,
    s3_prefix: str,
    s3_visibility: str,
    s3_encryption: bool,
    s3_cache_control: Optional[str],
    aws_default_region: Optional[str],
    aws_access_key_id: Optional[str],
    aws_secret_access_key: Optional[str],
):
    if len(files) == 0:
        raise click.MissingParameter(param_type="argument", param_hint="FILES")

    for filename in files:
        _, ext = os.path.splitext(filename)
        if ext != ".deb":
            raise click.BadParameter(
                param_hint="FILES", message=f"{filename} is not a .deb file"
            )

    s3 = configure_s3_client(
        s3_bucket,
        s3_prefix,
        s3_visibility,
        s3_encryption,
        aws_default_region,
        aws_access_key_id,
        aws_secret_access_key,
    )

    print("Retrieving existing manifests")
    release = Release.retrieve(s3=s3, codename=codename)
    manifests: Dict[str, Manifest] = {}
    for arch in release.architectures:
        manifests[arch] = Manifest.retrieve(
            s3=s3,
            codename=codename,
            component=component,
            architecture=arch,
        )

    for filename in files:
        pkg = Package.parse_file(filename)
        manifest = manifests[pkg.architecture]
        print(f"Add package file {filename} to {manifest}")
        try:
            manifest.add_package(
                pkg,
                preserve_versions=preserve_versions,
                fail_if_exists=fail_if_exists,
                dry_run=dry_run,
            )
        except Exception as e:
            raise click.ClickException(str(e))

    for manifest in manifests.values():
        if len(manifest.packages_to_be_uploaded) > 0:
            print(f"Uploading packages in {manifest}")
            manifest.write_to_s3(
                s3=s3, cache_control=s3_cache_control, fail_if_exists=fail_if_exists
            )
            release.update_manifest(manifest)

    print("Updating Release file")
    release.write_to_s3(s3=s3, cache_control=s3_cache_control)

    print("Update complete.")


@cli.command()
@add_common_options()
@click.option(
    "-a",
    "--architecture",
    default="all",
    show_default=True,
    help="The architecture of the package in the APT repository. Use 'all' to list all architectures.",
)
@click.option(
    "--dry-run", is_flag=True, default=False, show_default=True, help="Flag for DRY run"
)
@click.argument("package-name")
@click.argument("versions", nargs=-1)
def delete(
    package_name: str,
    versions: List[str],
    architecture: str,
    dry_run: bool,
    codename: str,
    component: str,
    s3_bucket: str,
    s3_prefix: str,
    s3_visibility: str,
    s3_encryption: bool,
    s3_cache_control: Optional[str],
    aws_default_region: Optional[str],
    aws_access_key_id: Optional[str],
    aws_secret_access_key: Optional[str],
):
    s3 = configure_s3_client(
        s3_bucket,
        s3_prefix,
        s3_visibility,
        s3_encryption,
        aws_default_region,
        aws_access_key_id,
        aws_secret_access_key,
    )

    print("Retrieving existing manifests")
    release = Release.retrieve(s3=s3, codename=codename)
    if architecture.lower() == "all":
        archs = release.architectures
    else:
        archs = [arch for arch in release.architectures if arch == architecture.lower()]

    for arch in archs:
        print(f"{arch}:")
        manifest = Manifest.retrieve(
            s3=s3,
            codename=codename,
            component=component,
            architecture=arch,
        )
        deleted = manifest.delete_package(package_name, versions, dry_run=dry_run)

        if len(deleted) == 0:
            print("No packages were deleted")
            continue

        for pkg in deleted:
            print(f"Deleted {pkg}")

        print("Updating new manifests to S3")
        manifest.write_to_s3(s3=s3, cache_control=s3_cache_control)
        release.update_manifest(manifest)
        release.write_to_s3(s3=s3, cache_control=s3_cache_control)
        print("Update completed.")
