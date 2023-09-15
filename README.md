# sirup

Summarise a directory of git repos. Regenerate them from the summary.

## Requirements

- Python 3 at `/usr/bin/python3`
- Git 2.22 or above
- Ensure that `~/.local/bin/` is in your `$PATH` environment variable
- [`jq`](https://stedolan.github.io/jq/) (optional)

## Installation

### Install and update

```
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/mebble/sirup/main/scripts/install.sh | sh
```

### Remove

```
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/mebble/sirup/main/scripts/remove.sh | sh
```

## Usage

Print the usage instructions by running:

```
sirup help
```

Output:

```
Usage: sirup <command> <args>
Commands:
    help                        Print these usage instructions
    sum                         Summarise git repos and print the summary in JSON to stdout
        --repos ./repos/dir     The directory containing the git repos
        --log   [optional]      Will output logs to stdout
    gen                         Generate git repos from a summary file
        --from  ./sum/file      Path to the summary file
        --to    ./dest/dir      The destination directory where you want to clone the repos
For more information, visit: https://github.com/mebble/sirup/blob/main/README.md
```

Notes:

- Your git repositories must be kept in a flat directory structure. That is, if your personal projects lie within `./projects-personal/`, they must be direct children of this directory and should not be nested within any sub directories. Future versions of `sirup` might allow nested directories.

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
sirup sum --repos ./projects
```

With logs:

```bash
sirup sum --repos ./projects --log
```

Piped to `jq` (don't use any flags so that only JSON gets piped to `jq`):

```bash
sirup sum --repos ./projects | jq
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
sirup sum --repos ./projects > repos.json
```

Basic usage:

```bash
sirup gen --from repos.json --to output-dir
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

## Who Needs This?

In your computer you might have a directory containing many git repositories. These could be personal projects, college assignments or codebases from work.

Now imagine you just got a new computer and need to move all these repositories to it. If you have hundreds of repos, you'd probably need to copy gigabytes of data. This could take time. Your old computer is probably slow, making this worse. You could first delete your `node_modules`, build files, etc, but this would be really tedious. It would also be tedious to figure out which repo is clean or dirty, which repo is synced to its remote, and so on.

Enter `sirup`. This tool will show you a JSON summary of all your git repositories. You could analyse the JSON using any standard tool to figure out the status of each repo. You could tweak this JSON to your liking. You could move this JSON to another computer and generate the git repositories over there.

This will hopefully save you time and data.

## Development

### Testing

```sh
python3 -m unittest tests.test_shell
python3 -m unittest tests.test_git
```
