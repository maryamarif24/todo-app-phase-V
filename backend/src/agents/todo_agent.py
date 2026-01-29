"""
AI Agent for todo management using OpenAI Agents SDK with OpenRouter.

This agent uses OpenAI Agents SDK to create an intelligent agent that can manage todos
and engage in conversation using OpenRouter API.
"""
import os
import json
import httpx
import uuid
from typing import Dict, Any, Optional
from openai import OpenAI

from ..services.conversation_service import ConversationService
from ..services.todo_service import (
    get_todos_by_user,
    get_todo_by_id,
    create_todo,
    update_todo,
    delete_todo,
    toggle_todo_complete,
    get_todo_by_title
)
from ..models.database import get_db
from sqlmodel import Session


class TodoAgent:
    """
    AI Agent using OpenAI Agents SDK for managing todos through natural language conversations.
    """

    def __init__(self):
        """Initialize the TodoAgent with OpenRouter API configuration."""
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.offline_mode = not bool(self.openrouter_api_key)
        self.current_user_id = None  # Will be set when processing messages

        # Define the API configuration attributes
        self.api_key = self.openrouter_api_key
        self.model = "openai/gpt-4o-mini"
        self.base_url = "https://openrouter.ai/api/v1"

        if self.offline_mode:
            print("Warning: OPENROUTER_API_KEY not found. Running in offline mode with limited functionality.")
        else:
            # Initialize OpenAI client with OpenRouter
            self.client = OpenAI(
                api_key=self.openrouter_api_key,
                base_url="https://openrouter.ai/api/v1",
            )
            print("TodoAgent initialized with OpenRouter API")

    def _call_openrouter_api(self, messages: list, tools: list = None) -> dict:
        """
        Call the OpenRouter API with Gemini 2.5 Flash model.

        Args:
            messages: List of messages for the conversation
            tools: Optional list of tools to provide to the model

        Returns:
            Response from the OpenRouter API
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }

        if tools:
            payload["tools"] = tools

        try:
            # Increase timeout and add retry logic
            timeout = httpx.Timeout(60.0, connect=10.0)  # 60s total, 10s connect
            with httpx.Client(timeout=timeout) as client:
                response = client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException as e:
            print(f"Timeout error calling OpenRouter API: {str(e)}")
            # Return a helpful response when request times out
            return {
                "choices": [{
                    "message": {
                        "content": "The request timed out. Please check your internet connection and try again. I can still help you manage your todos if you'd like!"
                    }
                }]
            }
        except httpx.RequestError as e:
            print(f"Network error calling OpenRouter API: {str(e)}")
            # Return a mock response structure when network fails
            return {
                "choices": [{
                    "message": {
                        "content": "I'm currently unable to connect to my AI services due to a network issue. I can help you manage your todos directly though. What would you like to do?"
                    }
                }]
            }
        except httpx.HTTPStatusError as e:
            print(f"HTTP error from OpenRouter API: {e.response.status_code} - {e.response.text}")
            # Return a mock response structure when API returns error
            return {
                "choices": [{
                    "message": {
                        "content": f"API Error {e.response.status_code}: I'm having trouble connecting to my AI services. What would you like to do with your todos?"
                    }
                }]
            }
        except Exception as e:
            print(f"Unexpected error calling OpenRouter API: {str(e)}")
            # Return a mock response structure for other errors
            return {
                "choices": [{
                    "message": {
                        "content": "I'm experiencing an issue connecting to my AI services. What would you like to do with your todos?"
                    }
                }]
            }

    def process_message(self, user_id, message: str, conversation_id: Optional[str] = None) -> str:
        """
        Process a natural language message and return an appropriate response.

        Args:
            user_id: The user's UUID
            message: The natural language message from the user
            conversation_id: Optional conversation ID for context

        Returns:
            AI-generated response string
        """
        # Set current user ID for tool functions
        self.current_user_id = user_id
        user_id_str = str(user_id)
        message_lower = message.lower().strip()

        # Handle todo-specific commands first
        if self._is_todo_command(message_lower):
            return self._handle_todo_command(user_id_str, message)

        # For general conversation, use AI if available
        if not self.offline_mode:
            return self._process_with_ai(user_id_str, message)

        # Fallback to offline conversation handling
        return self._handle_general_conversation(message)

    def _extract_todo_title(self, message: str) -> Optional[str]:
        """Extract todo title from a create message."""
        # First, try to extract from quoted strings (handles "add todo -- add todo\n  \"hi\" with description \"hello\"\n  08:05 am")
        import re

        # Look for quoted strings - handles cases like "add todo -- add todo\n  \"hi\" with description \"hello\"\n  08:05 am"
        quote_pattern = r'"([^"]*)"|\'([^\']*)\''
        matches = re.findall(quote_pattern, message)

        if matches:
            # If there are multiple quoted strings, use the first one (usually the title)
            for match in matches:
                # match is a tuple where one element is the matched string in double quotes,
                # and the other is the matched string in single quotes (or empty string)
                title = match[0] if match[0] else match[1]
                if title:
                    return title.strip()

        # Simple extraction - look for common patterns
        message_lower = message.lower()

        # Patterns like "create todo to [title]" or "add [title] to my todos"
        if 'todo to' in message_lower:
            parts = message.split('todo to', 1)
            if len(parts) > 1:
                return parts[1].strip()
        elif 'todo:' in message:
            parts = message.split('todo:', 1)
            if len(parts) > 1:
                return parts[1].strip()
        elif 'add' in message_lower and 'to' in message_lower:
            # Extract between "add" and "to"
            add_idx = message_lower.find('add')
            to_idx = message_lower.find('to', add_idx)
            if add_idx != -1 and to_idx != -1:
                return message[add_idx + 3:to_idx].strip()

        # Fallback: return the whole message after removing common words
        words_to_remove = ['create', 'add', 'new', 'make', 'todo', 'to', 'a', 'an', 'the']
        title = message
        for word in words_to_remove:
            title = title.replace(word, ' ')
        return title.strip() or None

    def _is_todo_command(self, message_lower: str) -> bool:
        """Check if the message is a todo command."""
        todo_keywords = ['create', 'add', 'new', 'make', 'todo', 'task', 'delete', 'remove', 'complete', 'finish', 'done', 'mark', 'show', 'list', 'view', 'get']
        for keyword in todo_keywords:
            if keyword in message_lower:
                return True
        return False

    def _handle_todo_command(self, user_id_str: str, message: str) -> str:
        """Handle todo-specific commands."""
        message_lower = message.lower()

        # Check for delete command first (more specific)
        if any(word in message_lower for word in ['delete', 'remove']) and any(word in message_lower for word in ['todo', 'task']):
            return self._delete_todo_from_message(user_id_str, message)

        # Create a new todo (prioritize creation over completion when both keywords are present)
        elif any(word in message_lower for word in ['create', 'add', 'new', 'make']) and any(word in message_lower for word in ['todo', 'task']):
            return self._create_todo_from_message(user_id_str, message)

        # Check for completion commands (only if not a creation command)
        elif any(word in message_lower for word in ['complete', 'finish', 'done', 'mark']) and any(word in message_lower for word in ['todo', 'task']):
            return self._toggle_todo_completion(user_id_str, message)

        # Check for show/list commands
        elif any(word in message_lower for word in ['show', 'list', 'view', 'get']) and any(word in message_lower for word in ['todo', 'task', 'todos', 'tasks']):
            return self._get_user_todos(user_id_str)

        else:
            return "I can help you manage your todos! Try saying things like 'Create a todo to buy groceries' or 'Show me my todos'."

    def _create_todo_from_message(self, user_id_str: str, message: str) -> str:
        """Create a new todo from a natural language message."""
        try:
            user_id = uuid.UUID(user_id_str)

            # Extract the title from the message
            title = self._extract_todo_title(message)
            if not title:
                return "I couldn't extract a title from your message. Please try again with a clear todo description."

            # Create a new database session
            db_gen = get_db()
            db = next(db_gen)

            try:
                # Create the todo
                new_todo = create_todo(db, user_id, title.strip())
                db.add(new_todo)
                db.commit()
                db.refresh(new_todo)

                return f"[SUCCESS] Successfully created todo: '{new_todo.title}'. Your todo has been added to your list!"
            except Exception as e:
                db.rollback()
                return f"I encountered an error creating your todo: {str(e)}"
            finally:
                db.close()
        except ValueError:
            return "Invalid user ID format. Please try again."
        except Exception as e:
            return f"An error occurred while creating your todo: {str(e)}"

    def _get_user_todos(self, user_id_str: str) -> str:
        """Get all todos for the user."""
        try:
            user_id = uuid.UUID(user_id_str)

            # Create a new database session
            db_gen = get_db()
            db = next(db_gen)

            try:
                # Get all todos for the user
                todos = get_todos_by_user(db, user_id)

                if not todos:
                    return "You don't have any todos yet. Try creating one with 'Create a todo to [your task]'!"

                # Format the todos for display
                todo_list = []
                for i, todo in enumerate(todos, 1):
                    status = "[DONE]" if todo.is_complete else "[PENDING]"
                    todo_list.append(f"{i}. {status} {todo.title}")

                return f"Here are your todos:\n" + "\n".join(todo_list)
            finally:
                db.close()
        except ValueError:
            return "Invalid user ID format. Please try again."
        except Exception as e:
            return f"An error occurred while retrieving your todos: {str(e)}"

    def _toggle_todo_completion(self, user_id_str: str, message: str) -> str:
        """Toggle the completion status of a todo."""
        try:
            user_id = uuid.UUID(user_id_str)

            # Create a new database session
            db_gen = get_db()
            db = next(db_gen)

            try:
                # Try to find the todo by ID first
                todo_id = self._extract_todo_id(message)
                todo = None

                if todo_id:
                    try:
                        todo_uuid = uuid.UUID(todo_id)
                        todo = get_todo_by_id(db, todo_uuid)
                    except ValueError:
                        # Invalid UUID format
                        pass

                # If no ID found, try to find by title
                if not todo:
                    # Extract title from message
                    title = self._extract_todo_title(message)
                    if title:
                        todo = get_todo_by_title(db, user_id, title)

                if not todo:
                    return "I couldn't find that todo. Please check the title or ID and try again."

                # Toggle completion status
                updated_todo = toggle_todo_complete(db, todo.id)
                db.commit()
                db.refresh(updated_todo)

                status = "completed" if updated_todo.is_complete else "marked as incomplete"
                return f"[SUCCESS] Todo '{updated_todo.title}' has been {status}."
            finally:
                db.close()
        except ValueError:
            return "Invalid user ID or todo ID format. Please try again."
        except Exception as e:
            return f"An error occurred while updating your todo: {str(e)}"

    def _delete_todo_from_message(self, user_id_str: str, message: str) -> str:
        """Delete a todo based on the message."""
        try:
            user_id = uuid.UUID(user_id_str)

            # Create a new database session
            db_gen = get_db()
            db = next(db_gen)

            try:
                # Try to find the todo by ID first
                todo_id = self._extract_todo_id(message)
                todo = None

                if todo_id:
                    try:
                        todo_uuid = uuid.UUID(todo_id)
                        todo = get_todo_by_id(db, todo_uuid)
                    except ValueError:
                        # Invalid UUID format
                        pass

                # If no ID found, try to find by title
                if not todo:
                    # Extract title from message
                    title = self._extract_todo_title(message)
                    if title:
                        todo = get_todo_by_title(db, user_id, title)

                if not todo:
                    return "I couldn't find that todo. Please check the title or ID and try again."

                # Delete the todo
                success = delete_todo(db, todo.id)
                if success:
                    db.commit()
                    return f"[SUCCESS] Todo '{todo.title}' has been deleted successfully."
                else:
                    return "I couldn't delete that todo. It may have already been removed."
            finally:
                db.close()
        except ValueError:
            return "Invalid user ID or todo ID format. Please try again."
        except Exception as e:
            return f"An error occurred while deleting your todo: {str(e)}"

    def _extract_todo_id(self, message: str) -> Optional[str]:
        """Extract todo ID from message."""
        import re
        # Look for UUID pattern or simple ID
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern, message, re.IGNORECASE)
        if match:
            return match.group(0)
        return None

    def _is_general_conversation(self, message_lower: str) -> bool:
        """Check if the message is general conversation (not todo-specific)."""
        # General conversation keywords
        general_keywords = [
            'hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon',
            'good evening', 'how are you', 'what\'s up', 'howdy', 'sup',
            'thanks', 'thank you', 'bye', 'goodbye', 'see you', 'later',
            'how can you help', 'what can you do', 'help', 'who are you',
            'what are you', 'tell me about yourself', 'introduce yourself',
            'nice to meet you', 'pleased to meet you', 'how\'s it going',
            'what\'s new', 'how have you been', 'long time no see',
            'what do you think', 'in your opinion', 'do you like', 'favorite',
            'hobby', 'interest', 'passion', 'dream', 'goal', 'wish',
            'weather', 'time', 'date', 'day', 'today', 'tomorrow',
            'yesterday', 'weekend', 'vacation', 'holiday', 'birthday',
            'celebration', 'party', 'fun', 'joke', 'laugh', 'smile',
            'happy', 'sad', 'angry', 'excited', 'bored', 'tired',
            'hungry', 'thirsty', 'sleepy', 'awake', 'dream', 'nightmare',
            'music', 'song', 'movie', 'film', 'book', 'game', 'sport',
            'food', 'drink', 'color', 'animal', 'place', 'country',
            'city', 'travel', 'adventure', 'story', 'memory', 'experience'
        ]

        # Check if message contains general conversation keywords
        for keyword in general_keywords:
            if keyword in message_lower:
                return True

        # Check for questions (starts with who, what, where, when, why, how)
        question_words = ['who ', 'what ', 'where ', 'when ', 'why ', 'how ', 'which ', 'whose ']
        for word in question_words:
            if message_lower.startswith(word) or f' {word}' in message_lower:
                return True

        # If message is very short (likely greeting or simple response)
        if len(message_lower.split()) <= 3:
            return True

        return False

    def _handle_general_conversation(self, message: str) -> str:
        """Handle general conversation in offline mode."""
        message_lower = message.lower().strip()

        # Greetings
        if any(word in message_lower for word in ['hi', 'hello', 'hey', 'greetings', 'howdy', 'sup']):
            return "Hello! I'm your todo assistant. I can help you manage your tasks and have a chat too! How can I help you today?"

        # How are you
        elif 'how are you' in message_lower or 'how\'s it going' in message_lower:
            return "I'm doing great, thanks for asking! I'm here and ready to help you with your todos or just chat. What's on your mind?"

        # Thanks
        elif any(word in message_lower for word in ['thanks', 'thank you', 'thx', 'ty']):
            return "You're welcome! I'm always here to help with your todos or chat. Is there anything else I can assist you with?"

        # Goodbye
        elif any(word in message_lower for word in ['bye', 'goodbye', 'see you', 'later', 'cya']):
            return "Goodbye! Don't forget to check your todos. Come back anytime!"

        # Help/About
        elif any(word in message_lower for word in ['help', 'what can you do', 'how can you help']):
            return """I'm your friendly todo assistant! I can help you:

📝 **Todo Management:**
• Create new todos: "Create a todo to buy groceries"
• View your todos: "Show me my todos"
• Mark complete: "Mark todo abc-123 as complete"
• Delete todos: "Delete todo abc-123"

💬 **Chat with me:**
• Ask questions, tell jokes, or just say hi!
• I can talk about various topics

What would you like to do?"""

        # Who are you
        elif any(phrase in message_lower for phrase in ['who are you', 'what are you', 'introduce yourself', 'tell me about yourself']):
            return "I'm your personal todo assistant and chat companion! I help you manage your tasks while also being here for friendly conversation. I love helping people stay organized and productive!"

        # Weather/Time questions
        elif any(word in message_lower for word in ['weather', 'time', 'date', 'day']):
            return "I don't have access to current weather or time data, but I can definitely help you manage your todos and chat about other things! What's on your agenda today?"

        # Jokes/Fun
        elif any(word in message_lower for word in ['joke', 'funny', 'laugh']):
            return "Why did the todo list go to therapy? It had too many unresolved issues! 😄 What else can I help you with?"

        # Default friendly response
        else:
            responses = [
                "That's interesting! Tell me more about that.",
                "I love chatting! What's been happening with you?",
                "Sounds good! How else can I help you today?",
                "I'm all ears! What's next on your mind?",
                "Great to hear from you! What else is going on?",
                "I enjoy our conversations! What's new with you?"
            ]
            import random
            return random.choice(responses)

    def _process_with_ai(self, user_id_str: str, message: str) -> str:
        """
        Process message using OpenRouter API.
        Falls back to offline mode if API is unavailable.
        """
        # Check if API key is available
        if self.offline_mode:
            print("OpenRouter API key not available, using offline mode")
            return self._handle_offline_fallback(message)

        try:
            # Prepare messages for the API call
            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful assistant that manages todo items for users.
                    You can help users create, view, update, delete, and toggle completion status of todos.
                    Be friendly and conversational. You can also chat about general topics.
                    For todo operations:
                    - To create: "Create a todo to buy groceries"
                    - To view: "Show me my todos"
                    - To complete: "Mark todo abc-123 as complete"
                    - To delete: "Delete todo abc-123"
                    """
                },
                {
                    "role": "user",
                    "content": f"User ID: {user_id_str}\nMessage: {message}"
                }
            ]

            # Call the OpenRouter API
            response = self.client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=messages,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error calling OpenRouter API: {str(e)}")
            # Fallback to offline mode
            return self._handle_offline_fallback(message)



    def _handle_offline_fallback(self, message: str) -> str:
        """Handle requests when AI API is unavailable."""
        message_lower = message.lower().strip()

        # Check for basic todo commands and handle them directly
        if any(word in message_lower for word in ['create', 'add', 'new']) and 'todo' in message_lower:
            return "I'd love to create a todo for you, but I'm currently in offline mode. Please try again when the AI service is available."
        elif any(word in message_lower for word in ['show', 'list', 'view', 'get']) and any(word in message_lower for word in ['todo', 'task', 'todos', 'tasks']):
            return "I'd love to show you your todos, but I'm currently in offline mode. Please try again when the AI service is available."
        elif any(word in message_lower for word in ['complete', 'finish', 'done', 'mark']) and any(word in message_lower for word in ['todo', 'task']):
            return "I'd love to update your todos, but I'm currently in offline mode. Please try again when the AI service is available."
        elif any(word in message_lower for word in ['delete', 'remove']) and any(word in message_lower for word in ['todo', 'task']):
            return "I'd love to delete that todo, but I'm currently in offline mode. Please try again when the AI service is available."
        else:
            # Handle general conversation in offline mode
            return self._handle_general_conversation(message)

    def get_conversation_context(self, conversation_id: str, user_id: str) -> Dict[str, Any]:
        """
        Get conversation context for multi-turn conversations.

        Args:
            conversation_id: The conversation ID
            user_id: The user ID

        Returns:
            Dictionary containing conversation context
        """
        # This would integrate with the conversation service to retrieve recent messages
        # For now, returning an empty context - in a real implementation you'd retrieve
        # recent messages to provide context for the AI
        return {
            "recent_messages": [],
            "user_todos": []  # Could include user's current todos for context
        }