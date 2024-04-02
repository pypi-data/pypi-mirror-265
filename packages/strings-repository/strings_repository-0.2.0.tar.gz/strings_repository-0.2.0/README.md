StringsRepository CLI
========
Simple command line tool to pull changes from [string repository](https://github.com/HereTrix/strings_repository).

Overview
--------
Application utilize `strings_repository.yaml` file for configuration. It is possible to use custom environment variable to store access token or put it directly into file. Environment variable usage is highly recommended.

Installation
-------
Install via `pip install strings_repository` 

or manually clone repository and launch `pip install .`

Usage
-------
To create configuration file run `strings_repository init` command and follow instructions.

Alternatively you can create `strings_repository.yaml` file manually.
Example:

```
env_variable: ENV_VARIABLE
host: your_host
languages:
- en
path: Source
tags:
- your_tags
type: json
```

After configuration completed you can pull data by `strings_repository pull` command.

License
-------

**StringsRepository CLI** is released under the MIT license. See `LICENSE` for details.
