<div align="center">
  <h1><a href="https://github.com/KristopherLeads/stylish"><img alt="Stylish" src="images/stylish.png" width=600/></a></h1>
</div>

**The World's First AI-Powered Markdown Editor Named Stylish**

It may not be the first AI-powered markdown editor, but this artisinal application coded in Python, Flask, JavaScript, and CSS/HTML definitely exists. This is a local web application that uses OpenAI to process and improve markdown articles according to user-defined custom style guides.

## Features

- **AI-Powered Processing**: Stylish uses OpenAI's GPT models to process markdown content
- **Custom Style Guides**: You can create and manage multiple style guides for different content types
- **Content Analysis**: Analyze content for style guide compliance without making changes
- **Validation**: Built-in markdown validation and issue detection finds common issues

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/KristopherLeads/stylish
cd stylish
# If using MacOS Github desktop, a better command is likely: cd Documents/Github/Stylish
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
cp env-example.md .env
nano .env
# Edit .env and add your OpenAI API key and Flask string
```

5. Run the application:
```bash
python3 stylish.py
```

6. Open your browser of choice and navigate to `http://127.0.0.1:5000`

### Shutting Down
To turn off the Stylish service, follow these steps:

```bash
Ctrl+C # This shuts down the web server
deactivate # This shuts of the emulated environment
```

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
stylish/
├── .env-example
├── README.md
├── stylish.py
├── config.py
├── requirements.txt
├── test_openai.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── style_guides/
│   └── default.md
├── templates/
│   ├── base.html
│   └── index.html
└── utils/
    ├── markdown_processor.py
    └── openai_client.py
```

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
- Ensure that in the process of setting up your `.env` file, you correctly copied it and changed the name from `.example-env` to `.env`

**OpenAI Issue with Keyword, e.g. Proxies**
- This is a [known issue](https://community.openai.com/t/error-with-openai-1-56-0-client-init-got-an-unexpected-keyword-argument-proxies/1040332/90) - 1.55.3 was tested to work fine and was the version I used for all testing.
- To install 1.55.3, use this command:

```bash
pip install openai==1.55.3
```

**Style Guide Not Found**
- Ensure the style guide file exists in the `style_guides/` directory
- Check that the filename matches exactly

**Processing Takes Too Long**
- Large content may take longer to process via OpenAI - if you keep failing processing, consider breaking large documents into smaller sections

**Memory Issues**
- Restart the application if you encounter memory issues
