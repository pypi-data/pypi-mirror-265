# Copyright 2024 Nicolas Paul.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

__version__ = "0.0.0"
# TODO(nc0): __version__ = bloow.__version__


def requirements():
  """Parse requirements from requirements.txt."""
  with open("requirements.txt", encoding="utf-8") as f:
    return f.read().splitlines()


setup(
  name="bloow",
  version=__version__,
  description="A modular and flexible static site generation tool that will blow your mind.",
  author="Nicolas Paul",
  author_email="n@nc0.fr",
  packages=find_packages(exclude=["tests", "examples"]),
  package_data={},
  python_requires=">=3.9",
  install_requires=[],  # requirements(),
  extras_require={},
  url="https://bloow.wtf",
  license="Apache-2.0",
  classifiers=[
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
  ],
  zip_safe=True,
  keywords=["static", "site", "generator", "bloow", "web"],
)
