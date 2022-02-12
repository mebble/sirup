# sirup

Summarise a directory of git repos. Regenerate them from the summary.

## Requirements

- Python 3 at `/usr/bin/python3`
- Git 2.22 or above
- [`jq`](https://stedolan.github.io/jq/) (optional)

## Installation

1. Clone this repo
2. `cd` into the repo and run `chmod +x ./sirup`

## Usage

Print the usage instructions by running:

```
./sirup help
```

Output:

```
Usage: ./sirup <sub-command> <args> <flags>
<sub-command>:
    help                       	Print these usage instructions
    sum                        	Summarise git repos and print the summary in JSON to stdout
        <args>:
            --repos ./repos/dir	The directory containing the git repos
        <flags>:
            --log   [optional] 	Will output logs to stdout
    gen                        	Generate git repos from a summary file
        <args>:
            --from  ./sum/file 	Path to the summary file
            --to    ./dest/dir 	The destination directory where you want to clone the repos
```

## Examples

Assuming you have this directory structure:

```
`-- projects
    |-- birdwatch
    `-- burl
```

### sirup sum

Basic usage:

```bash
./sirup sum --repos ./projects
```

With logs:

```bash
./sirup sum --repos ./projects --log
```

Piped to `jq` (don't use any flags so that only JSON gets piped to `jq`):

```bash
./sirup sum --repos ./projects | jq
```

Output when piped to `jq`:

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

Assuming you had executed:

```
./sirup sum --repos ./projects > repos.json
```

Basic usage:

```bash
./sirup gen --from repos.json --to output-dir
```

Output:

```
Cloning repositories to output-dir
[1/2] Cloning repo: birdwatch
[Done]
[2/2] Cloning repo: burl
[Done]
```

You can add the following fields to a repo object in the JSON summary that `sirup gen` will pick up:

| Field | Description |
|-------|-------------|
| `"ignore": true` | The repo will not be cloned |
