# Silence Remover

Silence Remover is a user-friendly audio tool that removes silence from your recordings, ensuring a smooth and
uninterrupted listening experience.

## Prerequisites

❯ Python >= 3.8 \

## Setup

### 1. Create a Virtual Environment:

```shell
python3 -m venv venv
```

### 2. Activate the Virtual Environment:

```shell
source venv/bin/activate
```

### 3. Install Project Dependencies:

```shell
pip3 install -r requirements.txt
```

## Usage

To run this script for a specific folder, use the following command:

```shell
python3 main.py [-i | --input] /path/to/your/directory [-o | --output] /output/path
```

### Options:

* [-i | --input]: Input directory to process.
* [-o | --output]: Output directory for the results.

If you want to run the script for a specific file, use the following command:
However, you can also run this script for specific file you can run script with such argument:

```shell
python3 main.py [-f | --file] /path/to/your/file
```

> ⚠️ **Note!**
>
> The script will save the results into the current directory where the script is executed.

