import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "neulabs-cdk-constructs",
    "version": "0.7.0",
    "description": "neulabs-cdk-constructs",
    "license": "Apache-2.0",
    "url": "https://github.com/neulabscom/neulabs-cdk-constructs.git",
    "long_description_content_type": "text/markdown",
    "author": "Neulabs<tech@neulabs.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/neulabscom/neulabs-cdk-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "neulabs_cdk_constructs",
        "neulabs_cdk_constructs._jsii",
        "neulabs_cdk_constructs.aws_lambda",
        "neulabs_cdk_constructs.newrelic",
        "neulabs_cdk_constructs.oidc",
        "neulabs_cdk_constructs.stack",
        "neulabs_cdk_constructs.utils"
    ],
    "package_data": {
        "neulabs_cdk_constructs._jsii": [
            "neulabs-cdk-constructs@0.7.0.jsii.tgz"
        ],
        "neulabs_cdk_constructs": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib==2.134.0",
        "constructs>=10.3.0, <11.0.0",
        "jsii>=1.92.0, <2.0.0",
        "publication>=0.0.3",
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
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
