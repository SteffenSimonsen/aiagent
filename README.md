# AI Coding Agent

A Python-based AI coding agent powered by Google's Gemini 2.0 Flash model that demonstrates autonomous file system interaction and code execution capabilities.

⚠️ **This is a research/demonstration project and is only intended for personal use.**

## Overview

This project showcases an AI agent that can:

- **File System Operations**: List directories, read file contents, and write files
- **Code Execution**: Run Python files with command-line arguments
- **AI-Powered Analysis**: Uses Google's Gemini 2.0 Flash model for intelligent code analysis and generation
- **Sandboxed Environment**: Operations are restricted to a specific working directory
- **Function Calling Architecture**: Demonstrates structured AI-to-system interactions

## Project Structure

The agent includes a complete calculator application as a working example of its capabilities.

## Technical Architecture

The AI agent uses a function-calling approach where the Gemini model can invoke:

1. **`get_files_info`** - List files and directories with metadata
2. **`get_file_content`** - Read the contents of specific files
3. **`write_file`** - Create or modify files
4. **`run_python_file`** - Execute Python scripts with optional arguments

The system is designed with security constraints, operating within a designated workspace directory.

## Educational Value

This project demonstrates:

- **Function Calling**: How AI models can interact with external systems through structured function calls
- **Code Analysis**: AI-driven understanding of codebases and project structures
- **Automated Testing**: AI agents running and interpreting test results
- **File Management**: Programmatic file system operations guided by natural language
- **Security Considerations**: Sandboxing and access controls for AI-driven file operations

## Implementation Details

**Dependencies:**
- Python 3.12+
- Google Gemini API

**Safety Features:**
- Path traversal protection
- Working directory restrictions
- File access validation
- Execution timeouts (30 seconds)
- Content size limits (10,000 characters per file)
