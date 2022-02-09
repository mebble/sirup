# sirup

Summarise a directory of git repos. Regenerate them from the summary.

## Requirements

- Python 3 at `/usr/bin/python3`
- Git 2.22 or above

## Installation

1. Clone this repo
2. `cd` into the repo and run `chmod +x ./sirup`

## Usage

Basic:

```bash
./sirup sum --repos ./path/to/repos
```

With logs:

```bash
./sirup sum --repos ./path/to/repos --log
```

With `jq`:

```bash
./sirup sum --repos ./path/to/repos | jq
```

### Example usage

Directory structure:

```
`-- projects
    |-- birdwatch
    `-- burl
```

Command:

```bash
./sirup sum --repos ./projects | jq
```

Output:

```json
[
  {
    "name": "birdwatch",
    "is_clean": true,
    "current_branch": {
      "local_branch": "master",
      "remote_branch": "origin/master",
      "synced": true
    },
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
    "current_branch": {
      "local_branch": "main",
      "remote_branch": "origin/main",
      "synced": false
    },
    "remotes": {
      "origin": {
        "fetch": "git@github.com:mebble/burl.git",
        "push": "git@github.com:mebble/burl.git"
      }
    }
  }
]
```
