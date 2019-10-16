from distutils.core import setup

setup(
    # Application name:
    name="CertManagerBackup",

    # Version number (initial):
    version="0.1.0",

    # Packages
    packages=["cert-manager-backup"],

    # Dependent packages (distributions)
    install_requires=[
        "pyyaml",
    ]
)
