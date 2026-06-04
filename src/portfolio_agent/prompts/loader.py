"""Utility for loading and rendering Jinja2 prompts."""

import jinja2
from pathlib import Path
from functools import lru_cache

@lru_cache
def get_prompt_env() -> jinja2.Environment:
    """
    Creates and configures a Jinja2 environment for loading prompts.
    Caches the environment for performance.
    """
    # Define the path to the prompts directory
    prompt_dir = Path(__file__).parent.resolve()
    
    # Create a Jinja2 environment with a file system loader
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(prompt_dir),
        trim_blocks=True,
        lstrip_blocks=True
    )

def load_prompt(template_name: str, **kwargs) -> str:
    """
    Loads a prompt from a Jinja2 template and renders it with provided variables.
    
    Args:
        template_name (str): The name of the prompt template file (e.g., "coordinator.jinja").
        **kwargs: Variables to pass to the template for rendering.
        
    Returns:
        str: The rendered prompt as a string.
        
    Raises:
        jinja2.TemplateNotFound: If the template file does not exist.
    """
    env = get_prompt_env()
    try:
        template = env.get_template(template_name)
        return template.render(**kwargs)
    except jinja2.TemplateNotFound:
        raise FileNotFoundError(f"Prompt template not found: {template_name}")
    except Exception as e:
        raise IOError(f"Error rendering prompt template '{template_name}': {e}")

# Example usage (for testing):
if __name__ == "__main__":
    # Create a dummy prompt for testing
    dummy_prompt_path = Path(__file__).parent / "test.jinja"
    dummy_prompt_path.write_text("Hello, {{ name }}! This is a test.")
    
    try:
        rendered_prompt = load_prompt("test.jinja", name="World")
        print("Rendered prompt:")
        print(rendered_prompt)
        assert rendered_prompt == "Hello, World! This is a test."
        print("\n✅ Prompt loader test passed!")
    finally:
        # Clean up the dummy file
        if dummy_prompt_path.exists():
            dummy_prompt_path.unlink()
