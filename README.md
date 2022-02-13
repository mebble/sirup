# sirup

Summarise a directory of git repos. Regenerate them from the summary.

## Who Needs This?

In your computer you might have a directory containing many git repositories. These could be personal projects, college assignments or codebases from work. If you're like me, you might like to keep all repositories in a flat directory structure, like `./projects-personal/*`, `./projects-college/*` and `./projects-work/*`.

Now imagine you just got a new computer and need to move all these repositories to it. If you have hundreds of repos, you'd probably need to copy gigabytes of data. This could take time. Your old computer is probably slow, making this worse. You could first delete your `node_modules`, build files, etc, but this would be really tedious. It would also be tedious to figure out which repo is clean or dirty, which repo is synced to its remote, and so on.

Enter `sirup`. This tool will show you a JSON summary of all your git repositories. You could analyse the JSON using any standard tool to figure out the status of each repo. You could tweak this JSON to your liking. You could move this JSON to another computer and generate the git repositories over there.

This will hopefully save you time and data.

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
