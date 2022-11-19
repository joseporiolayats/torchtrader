from setuptools import setup

test_packages = []

dev_packages = []

docs_packages = [
    "mkdocs>=1.1.2",
    "mkdocs-material>=7.2.3",
    "mkdocstrings>=0.18.1",
]

# setup(
#     extras_require={
#         "test": test_packages,
#         "dev": test_packages + dev_packages + docs_packages,
#         "docs": docs_packages,
#     }
# )


if __name__ == "__main__":
    # setup()
    setup(extras_require={"docs": docs_packages})
