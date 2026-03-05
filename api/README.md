# Dialogue Continuity API

## Overview

The Dialogue Continuity API is a Python module designed to monitor conversation length and automatically generate task cards when dialogues exceed 200 messages. This system ensures continuity in long-running projects by creating new task cards and resume prompts at predefined intervals.

## Features

- Automatic message counting with threshold detection at 200 messages
- Generation of new task cards with timestamped filenames
- Creation of resume prompts containing key context from previous dialogue
- Persistent storage across sessions
- Simple, easy-to-use API interface

## Installation

The API is already included in the project workspace. No additional installation is required.

## Usage

### Basic Usage

```python
from api import set_conversation, increment_message_count, get_message_count, get_current_status

# Set the current conversation ID
set_conversation("project_123")

# Increment message counter for each message in the conversation
for i in range(200):
    increment_message_count()

# Check current status
status = get_current_status()
print(f"Message count: {status['message_count']}")
```

### Advanced Usage

```python
from api import set_conversation, increment_message_count, get_message_count, reset_counter

# Set conversation and start monitoring
set_conversation("research_project")

# Process messages
for message in messages:
    increment_message_count()
    # Process message...

# Reset counter for next conversation
reset_counter()
```

## File Structure

```
api/
├── dialogue_continuity_api.py    # Main API implementation
├── __init__.py                   # Package initialization
└── README.md                     # This documentation file
```

## Configuration

The API is configurable through the following constants:

- `MAX_MESSAGES_THRESHOLD`: The message count threshold (default: 200)
- `TASK_CARD_DIR`: Directory where task cards are saved (default: "task_cards")
- `RESUME_PROMPT_DIR`: Directory where resume prompts are saved (default: "resume_prompts")

These can be modified in the `dialogue_continuity_api.py` file as needed.

## Verification

To verify the API works correctly:

1. Run the example usage in `dialogue_continuity_api.py`
2. Check that new task card and resume prompt files are created in their respective directories
3. Verify the content matches the expected format
4. Test with different conversation IDs
5. Confirm the system persists across session restarts

## Notes

- Task cards are versioned by date for easy reference
- The system is designed to be robust and handle edge cases
- All files are saved with UTF-8 encoding for international character support
- The API is thread-safe for use in multi-threaded applications

## Contributing

Contributions are welcome! Please follow the existing code style and document any changes in the README.md file.

## License

This project is licensed under the MIT License - see the LICENSE file for details.