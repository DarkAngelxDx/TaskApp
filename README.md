TaskApp — Advanced CLI Todo Manager

TaskApp is a powerful command-line todo application written in Python.
It is designed as a portfolio-level project with clean architecture and real-world features.

Features

Add, list, complete, and delete tasks

Task priorities: low / medium / high

Deadlines with overdue highlighting

Multi-user profiles (separate databases per user)

SQLite persistent storage

Today view for urgent and overdue tasks

Task statistics

Export tasks to CSV

Rich terminal UI

Command auto-completion

Installable via pip

Windows executable support

Installation
Local installation (development)
git clone https://github.com/DarkAngelxDx/TaskApp.git
cd TaskApp
pip install -e .

Run without installation
python -m todo.cli

Usage

Add a task:

todo add "Finish portfolio" --priority high --deadline 2026-01-15


List all tasks:

todo list


Mark task as done:

todo done 1


Delete a task:

todo delete 1

Today View

Show all pending tasks due today or overdue:

todo today

Statistics

Display task statistics:

todo stats

Multi-user Profiles

List users:

todo user list


Create a new user:

todo user create work


Switch active user:

todo user switch work

Export Tasks

Export all tasks to CSV:

todo export


Output file:

tasks.csv

Configuration

Configuration file location:

Windows: C:\Users\<username>\.todo\config.toml

Linux/macOS: ~/.todo/config.toml

Example configuration:

user = "default"
date_format = "%Y-%m-%d"

Command Auto-completion

Linux / macOS:

activate-global-python-argcomplete


Windows:

pip install pyreadline3

Running Tests
pytest
