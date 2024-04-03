import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "reapit-cdk.entra-id-application",
    "version": "0.1.0",
    "description": "This construct creates and manages a Microsoft Entra ID Application",
    "license": "MIT",
    "url": "https://github.com/reapit/ts-cdk-constructs/blob/main/packages/constructs/entra-id-application",
    "long_description_content_type": "text/markdown",
    "author": "Josh Balfour<jbalfour@reapit.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/reapit/ts-cdk-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "reapit_cdk.entra_id_application",
        "reapit_cdk.entra_id_application._jsii"
    ],
    "package_data": {
        "reapit_cdk.entra_id_application._jsii": [
            "entra-id-application@0.1.0.jsii.tgz"
        ],
        "reapit_cdk.entra_id_application": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.96.2, <3.0.0",
        "constructs>=10.2.70, <11.0.0",
        "jsii>=1.94.0, <2.0.0",
        "publication>=0.0.3",
        "reapit-cdk.replicated-key>=0.1.0, <0.2.0",
        "reapit-cdk.replicated-secret>=0.1.0, <0.2.0",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": [
        "src/reapit_cdk/entra_id_application/_jsii/bin/0",
        "src/reapit_cdk/entra_id_application/_jsii/bin/1",
        "src/reapit_cdk/entra_id_application/_jsii/bin/2",
        "src/reapit_cdk/entra_id_application/_jsii/bin/3",
        "src/reapit_cdk/entra_id_application/_jsii/bin/4",
        "src/reapit_cdk/entra_id_application/_jsii/bin/5",
        "src/reapit_cdk/entra_id_application/_jsii/bin/6",
        "src/reapit_cdk/entra_id_application/_jsii/bin/7",
        "src/reapit_cdk/entra_id_application/_jsii/bin/8",
        "src/reapit_cdk/entra_id_application/_jsii/bin/9",
        "src/reapit_cdk/entra_id_application/_jsii/bin/10",
        "src/reapit_cdk/entra_id_application/_jsii/bin/11",
        "src/reapit_cdk/entra_id_application/_jsii/bin/12",
        "src/reapit_cdk/entra_id_application/_jsii/bin/13",
        "src/reapit_cdk/entra_id_application/_jsii/bin/14"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
