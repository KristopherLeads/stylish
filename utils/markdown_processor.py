import markdown
import bleach
import os
import re
from typing import Dict, List

# This is a utility class/script that basically handles all the markdown-related stuff, both pre-and-post prompt/response

class MarkdownProcessor:
    def __init__(self, style_guides_dir):
        self.style_guides_dir = style_guides_dir
        self.allowed_tags = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'p', 'br', 'strong', 'em', 'u', 'strike',
            'ul', 'ol', 'li',
            'blockquote', 'code', 'pre',
            'a', 'img',
            'table', 'thead', 'tbody', 'tr', 'th', 'td'
        ]
        self.allowed_attributes = {
            'a': ['href', 'title'],
            'img': ['src', 'alt', 'title', 'width', 'height'],
            '*': ['id', 'class']
        }
    
    def sanitize_markdown(self, content: str) -> str:
        """Sanitize markdown content for security"""
        html = markdown.markdown(content)
        clean_html = bleach.clean(
            html, 
            tags=self.allowed_tags, 
            attributes=self.allowed_attributes,
            strip=True
        )
        return clean_html
    
    def load_style_guide(self, style_guide_name: str) -> str:
        """Load a style guide from the style_guides directory"""
        style_guide_path = os.path.join(self.style_guides_dir, f"{style_guide_name}.md")
        
        if not os.path.exists(style_guide_path):
            raise FileNotFoundError(f"Style guide '{style_guide_name}' not found")
        
        try:
            with open(style_guide_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading style guide: {str(e)}")
    
    def get_available_style_guides(self) -> List[str]:
        """Get list of available style guides"""
        if not os.path.exists(self.style_guides_dir):
            os.makedirs(self.style_guides_dir)
            return []
        
        style_guides = []
        for file in os.listdir(self.style_guides_dir):
            if file.endswith('.md'):
                style_guides.append(file[:-3])  # Remove .md extension
        
        return sorted(style_guides)
    
    def save_style_guide(self, name: str, content: str) -> bool:
        """Save a new style guide"""
        if not os.path.exists(self.style_guides_dir):
            os.makedirs(self.style_guides_dir)
        
        # Sanitize filename
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '', name)
        if not safe_name:
            raise ValueError("Invalid style guide name")
        
        style_guide_path = os.path.join(self.style_guides_dir, f"{safe_name}.md")
        
        try:
            with open(style_guide_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except Exception as e:
            raise Exception(f"Error saving style guide: {str(e)}")
    
    def validate_markdown(self, content: str) -> Dict:
        """Basic markdown validation"""
        issues = []
        
        # Check for common markdown issues
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for headers missing space after # while allowing for empty headers and code blocks
            # This regex checks for one or more #, followed immediately by a non-space, non-# character
            # This should largely correlate to headers if this is a proper markdown file, but if there's some weird code or something it might trigger a false positive
            # If you get that kind of error, let me know and I can update this logic
            if re.match(r'^#+[^#\s]', line.strip()):
                issues.append(f"Line {i}: Header missing space after #")
            
            # Check for unescaped special characters in URLs
            if '[' in line and '](' in line and ')' in line:
                # Find markdown links
                link_matches = re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', line)
                for match in link_matches:
                    url = match.group(2)
                    # Only flag if URL has spaces and doesn't look like a local file path
                    if ' ' in url and not url.startswith('#') and not url.startswith('./') and not url.startswith('../'):
                        issues.append(f"Line {i}: URL contains unescaped spaces")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'line_count': len(lines),
            'word_count': len(content.split())
        }
