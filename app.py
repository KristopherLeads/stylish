from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import logging
from config import config
from utils.openai_client import OpenAIClient
from utils.markdown_processor import MarkdownProcessor

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_CONFIG') or 'default'
app.config.from_object(config[config_name])
config[config_name].init_app(app)

# Initialize components
openai_client = OpenAIClient()
markdown_processor = MarkdownProcessor(app.config['STYLE_GUIDES_DIR'])

# Initialize OpenAI client
if app.config['OPENAI_API_KEY']:
    openai_client.initialize(
        app.config['OPENAI_API_KEY'], 
        app.config['OPENAI_MODEL']
    )
else:
    logging.warning("OpenAI API key not found. Please set OPENAI_API_KEY in your environment.")

@app.route('/')
def index():
    """Main page"""
    style_guides = markdown_processor.get_available_style_guides()
    return render_template('index.html', style_guides=style_guides)

@app.route('/api/process', methods=['POST'])
def process_markdown():
    """Process markdown content with style guide"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        markdown_content = data.get('markdown_content', '').strip()
        style_guide_name = data.get('style_guide_name', '').strip()
        action = data.get('action', 'process')  # 'process' or 'analyze'
        
        if not markdown_content:
            return jsonify({'success': False, 'error': 'No markdown content provided'}), 400
        
        if not style_guide_name:
            return jsonify({'success': False, 'error': 'No style guide selected'}), 400
        
        # Load style guide
        try:
            style_guide = markdown_processor.load_style_guide(style_guide_name)
        except FileNotFoundError:
            return jsonify({'success': False, 'error': f'Style guide "{style_guide_name}" not found'}), 404
        except Exception as e:
            return jsonify({'success': False, 'error': f'Error loading style guide: {str(e)}'}), 500
        
        # Validate markdown
        validation = markdown_processor.validate_markdown(markdown_content)
        
        # Process with OpenAI
        if action == 'analyze':
            result = openai_client.analyze_style_compliance(markdown_content, style_guide)
        else:
            result = openai_client.process_markdown_with_style_guide(markdown_content, style_guide)
        
        if result['success']:
            response_data = {
                'success': True,
                'validation': validation,
                'tokens_used': result['tokens_used']
            }
            
            if action == 'analyze':
                response_data['analysis'] = result['analysis']
            else:
                response_data['processed_content'] = result['processed_content']
            
            return jsonify(response_data)
        else:
            return jsonify({'success': False, 'error': result['error']}), 500
        
    except Exception as e:
        logging.error(f"Error processing markdown: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.route('/api/style-guides', methods=['GET'])
def get_style_guides():
    """Get list of available style guides"""
    try:
        style_guides = markdown_processor.get_available_style_guides()
        return jsonify({'success': True, 'style_guides': style_guides})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/style-guides/<name>', methods=['GET'])
def get_style_guide(name):
    """Get specific style guide content"""
    try:
        content = markdown_processor.load_style_guide(name)
        return jsonify({'success': True, 'content': content})
    except FileNotFoundError:
        return jsonify({'success': False, 'error': 'Style guide not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/style-guides', methods=['POST'])
def create_style_guide():
    """Create a new style guide"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        content = data.get('content', '').strip()
        
        if not name or not content:
            return jsonify({'success': False, 'error': 'Name and content are required'}), 400
        
        markdown_processor.save_style_guide(name, content)
        return jsonify({'success': True, 'message': 'Style guide created successfully'})
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error creating style guide: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'openai_configured': openai_client.client is not None,
        'style_guides_count': len(markdown_processor.get_available_style_guides())
    })

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'success': False, 'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create style guides directory if it doesn't exist
    os.makedirs(app.config['STYLE_GUIDES_DIR'], exist_ok=True)
    
    # Run the application
    app.run(
        debug=app.config['DEBUG'],
        host='127.0.0.1',
        port=5000
    )
