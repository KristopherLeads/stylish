import openai
from flask import current_app
import logging

class OpenAIClient:
    def __init__(self):
        self.client = None
        self.model = None
    
    def initialize(self, api_key, model='gpt-3.5-turbo'):
        """Initialize the OpenAI client with API key and model"""
        try:
            # Create OpenAI client with latest library
            self.client = openai.OpenAI(api_key=api_key)
            self.model = model
            logging.info(f"OpenAI client initialized with version {openai.__version__}")
            return True
        except Exception as e:
            logging.error(f"Failed to initialize OpenAI client: {str(e)}")
            logging.error(f"OpenAI version: {openai.__version__}")
            return False
    
    def process_markdown_with_style_guide(self, markdown_content, style_guide):
        """
        Process markdown content according to a style guide
        """
        if not self.client:
            raise ValueError("OpenAI client not initialized")
        
        system_prompt = f"""
        You are a markdown style guide processor. Your task is to analyze and improve markdown content according to the provided style guide.
        
        Style Guide:
        {style_guide}
        
        Instructions:
        1. Review the markdown content for compliance with the style guide
        2. Make necessary corrections and improvements
        3. Maintain the original meaning and structure
        4. Return only the corrected markdown content
        5. If no changes are needed, return the original content
        """
        
        user_prompt = f"""
        Please process this markdown content according to the style guide:
        
        {markdown_content}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            
            return {
                'success': True,
                'processed_content': response.choices[0].message.content,
                'tokens_used': response.usage.total_tokens
            }
        except Exception as e:
            logging.error(f"OpenAI API error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_style_compliance(self, markdown_content, style_guide):
        """
        Analyze markdown content for style guide compliance without making changes
        """
        if not self.client:
            raise ValueError("OpenAI client not initialized")
        
        system_prompt = f"""
        You are a markdown style guide analyzer. Review the provided markdown content against the style guide and provide a detailed analysis.
        
        Style Guide:
        {style_guide}

        IMPORTANT INSTRUCTIONS:
        - Only flag actual violations of the style guide, not stylistic preferences
        - Be conservative - when in doubt, don't flag an issue
        - Look at the actual text carefully before making claims about missing punctuation
        - Sentence case vs title case is often a matter of preference - only flag if explicitly against the style guide
        - Check that Oxford commas are actually missing before claiming they are
        - Focus on clear formatting and structural issues, not subjective style choices
        
        Provide your analysis in the following format:
        ## Compliance Score: X/10
        
        ## Issues Found:
        - List any style guide violations. When a violation occurs, you MUST cite the specific sentence in the output - for instance, if the problem is something like "Inconsistent use of straight quotes and curly quotes", your response should include the original text where the issue has arisen with the problem area in bold. Do not cite a problem without also citing the sentence where the problem exists.
        
        ## Suggestions:
        - Specific recommendations for improvement - ensure you are citing actual text that can be fixed as with "issues found".
        
        ## Strengths:
        - What the content does well according to the style guide
        """
        
        user_prompt = f"""
        Please analyze this markdown content for style guide compliance:
        
        {markdown_content}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            return {
                'success': True,
                'analysis': response.choices[0].message.content,
                'tokens_used': response.usage.total_tokens
            }
        except Exception as e:
            logging.error(f"OpenAI API error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
