# sirup

Summarise a directory of git repos. Regenerate them from the summary.

# Requirements

- Python 3 at `/usr/bin/python3`
- Git 2.22 or above

# Installation

1. Clone this repo
2. `cd` into the repo and run `chmod +x ./sirup`

# Usage

Basic usage:

```bash
./sirup --repos ./path/to/repos
```

Usage with `jq`:

```bash
./sirup --repos ./path/to/repos | jq
```

Sample output when used with `jq`:

```json
[
  {
    "name": "birdwatch",
    "is_clean": true,
    "current_branch": "master",
    "remotes": {
      "origin": {
        "fetch": "git@github.com:mebble/birdwatch.git",
        "push": "git@github.com:mebble/birdwatch.git"
      }
    }
  },
  {
    "name": "burl",
    "is_clean": true,
    "current_branch": "main",
    "remotes": {
      "origin": {
        "fetch": "git@github.com:mebble/burl.git",
        "push": "git@github.com:mebble/burl.git"
      }
    }
  }
]
```
