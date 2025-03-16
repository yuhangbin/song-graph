"""
Main module for the Song-Graph project.
"""

def greet(name: str) -> str:
    """
    Return a personalized greeting message.
    
    Args:
        name (str): The name to greet
        
    Returns:
        str: The greeting message
    """
    return f"Hello, {name}! Welcome to Song-Graph."

def main():
    """Main entry point of the program."""
    print(greet("User"))

if __name__ == "__main__":
    main() 