from setuptools import setup, find_packages

setup(
    name='Information_Retrieval',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Add dependencies here.
    ],
    entry_points={
        "console_scripts" : [
            "IR-Stop-Word-Removal = Information_Retrieval:Stop_Word_Removal_Code",
        ],
    },
)