# Example Tool

Welcome to the Example Tool project! This versatile tool provides a foundation for building powerful applications with features such as Database Integration, Internationalization, and more.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
- [Examples](#examples)
  - [SQL Example](#sql-example)
  - [Internationalization Example](#internationalization-example)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Database Integration:** Seamlessly connect to databases for efficient data storage and retrieval.
- **Internationalization (custom files):** Support multiple languages in your tool's user interface.
- **Custom Logger:** Support adding tables, colors, emojies and tons more.

## Getting Started

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/example-tool.git
   cd example-tool
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

Run the example script:

```bash
py examples/sql.py
```

### Examples

#### SQL Example

The SQL example demonstrates the tool's Database Integration feature. It connects to a SQLite database, performs basic CRUD operations, and showcases the Data Validation Library.

```bash
py examples/sql.py
```

#### Internationalization Example

This example illustrates the tool's Internationalization feature. It supports multiple languages, allowing you to switch between translations easily.

The language files are a YAML-based format. You can find them in the set path of the config.yml file.

### Configuration

The config.yml file contains the tool's configuration settings. These are customizable settings that you can modify in the config.yml file, and for development purposes, you can change the settings in the config.py file.

#### Paths

- **Windows**: %PROGRAMDATA%/CodeVault/Example/

- **Linux (Logs)**: /var/log/CodeVault/Example/logs/
- **Linux (Messages)**: /var/share/CodeVault/Example/locales/

- **MacOS (Logs)**: /var/log/CodeVault/Example/logs/
- **MacOS (Messages)**: /var/share/CodeVault/Example/locales/

### Contributing

We welcome contributions! If you have ideas, bug reports, or want to add new features, please open an issue or submit a pull request.

### License

Any tool created using this template is most likely licensed under the MIT License, however if the project is created especially from CodeVault, it will be licensed under the CodeVault License. Please check the LICENSE file for more information.
