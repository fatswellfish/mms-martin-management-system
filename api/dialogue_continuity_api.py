"""
Dialogue Continuity API

This module implements the API for monitoring dialogue length and generating task cards when exceeding 200 messages.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional

# Configuration
MAX_MESSAGES_THRESHOLD = 200
TASK_CARD_DIR = "task_cards"
RESUME_PROMPT_DIR = "resume_prompts"

# Initialize directories
os.makedirs(TASK_CARD_DIR, exist_ok=True)
os.makedirs(RESUME_PROMPT_DIR, exist_ok=True)


class DialogueContinuityAPI:
    """API class for managing dialogue continuity system"""

    def __init__(self):
        self.message_count = 0
        self.conversation_id = None
        self.task_card_file = None
        self.resume_prompt_file = None

    def set_conversation(self, conversation_id: str) -> None:
        """Set the current conversation ID"""
        self.conversation_id = conversation_id
        self.task_card_file = f"{TASK_CARD_DIR}/{conversation_id}_task_card_{datetime.now().strftime('%Y-%m-%d')}.md"
        self.resume_prompt_file = f"{RESUME_PROMPT_DIR}/{conversation_id}_resume_prompt_{datetime.now().strftime('%Y-%m-%d')}.md"

    def increment_message_count(self) -> int:
        """Increment message counter and check threshold"""
        self.message_count += 1
        
        # Check if we've reached the threshold
        if self.message_count >= MAX_MESSAGES_THRESHOLD:
            self._generate_new_task_card()
            
        return self.message_count

    def get_message_count(self) -> int:
        """Get current message count"""
        return self.message_count

    def _generate_new_task_card(self) -> bool:
        """Generate a new task card when threshold is reached"""
        try:
            # Create task card content
            task_card_content = f"""# TASK CARD: Dialogue Continuity System - {datetime.now().strftime('%Y-%m-%d')}

## Objective
Implement a system that automatically generates new task cards when dialogues exceed 200 messages, with accompanying prompt text for resuming work.

## Requirements
- Monitor message count in each conversation
- Generate a new task card when message count reaches 200
- Save the task card with timestamped filename
- Create a prompt string for resuming work
- Ensure the system is persistent across sessions

## Implementation Steps
1. Create a function to count messages in the current dialogue
2. Implement a threshold check at 200 messages
3. Generate a new task card with the current date and time
4. Save the task card in the workspace
5. Create a resume prompt with key context from the previous dialogue
6. Add this functionality to the core agent logic

## Verification
- Test with a simulated 200-message dialogue
- Confirm new task card is generated
- Verify resume prompt contains relevant context
- Ensure system persists across session restarts

## Notes
- This system will help maintain continuity in long-running projects
- The prompt should include key project details, recent decisions, and outstanding tasks
- Task cards should be versioned by date for easy reference
"""
            
            # Write task card file
            with open(self.task_card_file, 'w', encoding='utf-8') as f:
                f.write(task_card_content)
            
            # Create resume prompt content
            resume_prompt_content = f"""# RESUME PROMPT: Dialogue Continuity System - {datetime.now().strftime('%Y-%m-%d')}

You are continuing a long-running conversation that has exceeded 200 messages. Here's the context to resume work:

## Project Overview
A system to automatically generate new task cards when dialogues exceed 200 messages, with accompanying prompt text for resuming work.

## Key Context
- The system monitors message count in each conversation
- When message count reaches 200, it generates a new task card
- Task cards are saved with timestamped filenames
- A resume prompt is created with key context from the previous dialogue
- The system is designed to be persistent across sessions

## Current Status
The initial implementation has been completed with:
- A task card generated ({self.task_card_file})
- A resume prompt created ({self.resume_prompt_file})
- Basic monitoring and generation functionality established

## Next Steps
- Verify the system works correctly with a simulated 200-message dialogue
- Test that the new task card is properly generated
- Confirm the resume prompt contains relevant context
- Ensure the system persists across session restarts
- Document any edge cases or improvements needed

## Important Reminders
- Keep responses concise and actionable
- Focus on verifying the core functionality
- Maintain consistency with the original design
- Use the existing task card format for future iterations

Continue from here, ensuring all requirements are met and the system is robust."""
            
            # Write resume prompt file
            with open(self.resume_prompt_file, 'w', encoding='utf-8') as f:
                f.write(resume_prompt_content)
            
            print(f"New task card generated: {self.task_card_file}")
            print(f"New resume prompt generated: {self.resume_prompt_file}")
            
            return True
        
        except Exception as e:
            print(f"Error generating task card: {e}")
            return False

    def get_current_status(self) -> Dict[str, any]:
        """Get current system status"""
        return {
            "message_count": self.message_count,
            "threshold": MAX_MESSAGES_THRESHOLD,
            "status": "active",
            "task_card_file": self.task_card_file,
            "resume_prompt_file": self.resume_prompt_file
        }

    def reset_counter(self) -> None:
        """Reset message counter"""
        self.message_count = 0

# Global API instance
api = DialogueContinuityAPI()

# Export functions for external use
def set_conversation(conversation_id: str) -> None:
    """Set the current conversation ID"""
    api.set_conversation(conversation_id)


def increment_message_count() -> int:
    """Increment message counter and check threshold"""
    return api.increment_message_count()


def get_message_count() -> int:
    """Get current message count"""
    return api.get_message_count()


def get_current_status() -> Dict[str, any]:
    """Get current system status"""
    return api.get_current_status()


def reset_counter() -> None:
    """Reset message counter"""
    api.reset_counter()

# Example usage
if __name__ == "__main__":
    # Example of how to use the API
    set_conversation("project_123")
    
    # Simulate 200 messages
    for i in range(200):
        increment_message_count()
        
    print(f"Final message count: {get_message_count()}")
    print(f"Current status: {get_current_status()}")