# sirup

Summarise a directory of git repos. Regenerate them from the summary.

## Requirements

- Python 3 at `/usr/bin/python3`
- Git 2.22 or above

## Installation

1. Clone this repo
2. `cd` into the repo and run `chmod +x ./sirup`

## Usage

```
Usage: ./sirup <sub-command> <args> <flags>
<sub-command>:
    sum
        <args>:
            --repos ./repos/dir\tThe directory containing all the git repositories
        <flags>:
            --log [optional]   \tWill output logs to stdout
    gen
        <args>:
            --from ./json/file \tThe JSON file containing the output of "./sirup sum"
            --to ./dest/dir    \tThe destination directory where you want to clone the repositories
```

## Examples

### sirup sum

This command summarises the git repositories in your computer and prints the summary in JSON to stdout.

Assuming you have this directory structure:

```
`-- projects
    |-- birdwatch
    `-- burl
```

Basic usage:

```bash
./sirup sum --repos ./projects
```

With logs:

```bash
./sirup sum --repos ./projects --log
```

With `jq`:

```bash
./sirup sum --repos ./projects | jq
```

Output when used with `jq`:

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
    },
    "size": {
      "value": "11.76",
      "unit": "KiB"
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
    },
    "size": {
      "value": "10.90",
      "unit": "KiB"
    }
  }
]
```

### sirup gen

This command generates git repositories from the summary output of `sirup sum`.

Assuming you had executed:

```
./sirup sum --repos ./projects | jq > repos.json
```

Basic usage:

```bash
./sirup gen --from repos.json --to output-dir
```
