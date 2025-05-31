# Stylish
**The World's First AI-Powered Markdown Editor Named Stylish**

It may not be the first AI-powered markdown editor, but this artisinal application coded in Python, Flask, JavaScript, and CSS/HTML definitely exists. This is a local web application that uses OpenAI to process and improve markdown articles according to user-defined custom style guides.

## Features

- **AI-Powered Processing**: Uses OpenAI's GPT models to process markdown content
- **Custom Style Guides**: Create and manage multiple style guides for different content types
- **Content Analysis**: Analyze content for style guide compliance without making changes
- **Real-time Processing**: Process content instantly through a clean web interface
- **Validation**: Built-in markdown validation and issue detection
- **Export Results**: Copy processed content to clipboard
- **Responsive Design**: Works on desktop and mobile devices

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/KristopherLeads/stylish
cd stylish
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate - but this was developed on a Mac so caveat emptor
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

5. Run the application:
```bash
python3 app.py
```

6. Open your browser and navigate to `http://127.0.0.1:5000`

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-3.5-turbo)
- `SECRET_KEY`: Flask secret key for session security
- `FLASK_CONFIG`: Set to 'production' for deployment (default: development)

### Style Guides

Style guides are stored in the `style_guides/` directory as markdown files. You can:

1. Create new style guides through the web interface
2. Manually add `.md` files to the `style_guides/` directory
3. Import existing style guides from other projects

## Usage

### Creating a Style Guide

1. Click "New Style Guide" in the web interface
2. Provide a name (used as filename)
3. Write your style guide in markdown format
4. Save the style guide

Example style guide structure:
```markdown
# Technical Writing Style Guide

## Voice and Tone
- Use active voice
- Write clearly and concisely
- Maintain a professional tone

## Formatting
- Use ## for main sections
- Use bullet points for lists
- Include code examples in backticks
```

### Processing Content

1. Paste your markdown content in the input area
2. Select a style guide from the dropdown
3. Choose either:
   - **Process Content**: Get AI-improved version
   - **Analyze Only**: Get compliance analysis without changes

### API Endpoints

The application provides REST API endpoints:

- `GET /health` - Health check
- `GET /api/style-guides` - List available style guides
- `GET /api/style-guides/<name>` - Get specific style guide
- `POST /api/style-guides` - Create new style guide
- `POST /api/process` - Process markdown content

## Development

### Project Structure

```
markdown-style-processor/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── utils/
│   ├── openai_client.py  # OpenAI integration
│   └── markdown_processor.py  # Markdown utilities
├── templates/            # HTML templates
├── static/              # CSS, JS, and other static files
├── style_guides/        # Style guide storage
└── tests/              # Unit tests (coming soon)
```

### Running in Development

```bash
export FLASK_CONFIG=development
python app.py
```

The application will run with debug mode enabled and auto-reload on file changes.

### Testing

```bash
# Run health check
curl http://127.0.0.1:5000/health

# Test API endpoints
curl -X POST http://127.0.0.1:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{"markdown_content": "# Test", "style_guide_name": "default", "action": "analyze"}'
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

**OpenAI API Key Not Working**
- Verify your API key is correct and has sufficient credits
- Check that the key is properly set in your `.env` file

**OpenAI Issue with Keyword, e.g. Proxies**
- This is a [known issue](https://community.openai.com/t/error-with-openai-1-56-0-client-init-got-an-unexpected-keyword-argument-proxies/1040332/90) - 1.55.3 was tested to work fine and was the version I used for all testing.
- To install 1.55.3, simply:

```bash
pip install openai==1.55.3
```

**Style Guide Not Found**
- Ensure the style guide file exists in the `style_guides/` directory
- Check that the filename matches exactly (case-sensitive)

**Processing Takes Too Long**
- Large content may take longer to process
- Consider breaking large documents into smaller sections

**Memory Issues**
- Restart the application if you encounter memory issues
- Consider using a more powerful OpenAI model for better performance

### Support

For support and questions:
- Open an issue on GitHub
- Check existing issues for similar problems
- Review the documentation above
