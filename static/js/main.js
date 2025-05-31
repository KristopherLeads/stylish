// Global variables
let currentResults = '';

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    // Check API health on load
    checkHealth();
});

// Health check
async function checkHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        
        if (!data.openai_configured) {
            showToast('Warning: OpenAI API key not configured. Please set your OPENAI_API_KEY environment variable.', 'warning');
        }
    } catch (error) {
        console.error('Health check failed:', error);
    }
}

// Process markdown
async function processMarkdown() {
    const content = document.getElementById('markdownInput').value.trim();
    const styleGuide = document.getElementById('styleGuideSelect').value;
    
    if (!content) {
        showToast('Please enter markdown content to process.', 'error');
        return;
    }
    
    if (!styleGuide) {
        showToast('Please select a style guide.', 'error');
        return;
    }
    
    setLoading('processBtn', 'processSpinner', true);
    
    try {
        const response = await fetch('/api/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                markdown_content: content,
                style_guide_name: styleGuide,
                action: 'process'
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.processed_content, 'processed');
            displayMetadata(data);
            showToast('Content processed successfully!', 'success');
        } else {
            showToast(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Processing failed:', error);
        showToast('Processing failed. Please try again.', 'error');
    } finally {
        setLoading('processBtn', 'processSpinner', false);
    }
}

// Analyze markdown
async function analyzeMarkdown() {
    const content = document.getElementById('markdownInput').value.trim();
    const styleGuide = document.getElementById('styleGuideSelect').value;
    
    if (!content) {
        showToast('Please enter markdown content to analyze.', 'error');
        return;
    }
    
    if (!styleGuide) {
        showToast('Please select a style guide.', 'error');
        return;
    }
    
    setLoading('analyzeBtn', 'analyzeSpinner', true);
    
    try {
        const response = await fetch('/api/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                markdown_content: content,
                style_guide_name: styleGuide,
                action: 'analyze'
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.analysis, 'analysis');
            displayMetadata(data);
            showToast('Analysis completed successfully!', 'success');
        } else {
            showToast(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Analysis failed:', error);
        showToast('Analysis failed. Please try again.', 'error');
    } finally {
        setLoading('analyzeBtn', 'analyzeSpinner', false);
    }
}

// Display results in the results panel
function displayResults(content, type) {
    const resultsDiv = document.getElementById('results');
    const copyBtn = document.getElementById('copyBtn');
    
    currentResults = content;
    
    if (type === 'analysis') {
        // Convert markdown analysis to HTML for better display
        resultsDiv.innerHTML = `<div class="analysis-content">${marked ? marked.parse(content) : content.replace(/\n/g, '<br>')}</div>`;
    } else {
        // Display processed markdown in a code block
        resultsDiv.innerHTML = `<pre><code class="language-markdown">${escapeHtml(content)}</code></pre>`;
        // Re-run Prism highlighting
        if (typeof Prism !== 'undefined') {
            Prism.highlightAll();
        }
    }
    
    copyBtn.classList.remove('d-none');
}

// Display metadata
function displayMetadata(data) {
    const metadataDiv = document.getElementById('metadata');
    let metadataHtml = '<div class="row text-center">';
    
    if (data.tokens_used) {
        metadataHtml += `<div class="col-md-4"><small class="text-muted">Tokens Used: <strong>${data.tokens_used}</strong></small></div>`;
    }
    
    if (data.validation) {
        metadataHtml += `<div class="col-md-4"><small class="text-muted">Lines: <strong>${data.validation.line_count}</strong></small></div>`;
        metadataHtml += `<div class="col-md-4"><small class="text-muted">Words: <strong>${data.validation.word_count}</strong></small></div>`;
    }
    
    metadataHtml += '</div>';
    
    if (data.validation && data.validation.issues && data.validation.issues.length > 0) {
        metadataHtml += '<div class="alert alert-warning mt-2"><strong>Validation Issues:</strong><ul class="mb-0 mt-2">';
        data.validation.issues.forEach(issue => {
            metadataHtml += `<li>${issue}</li>`;
        });
        metadataHtml += '</ul></div>';
    }
    
    metadataDiv.innerHTML = metadataHtml;
}

// Copy results to clipboard
async function copyResults() {
    if (currentResults) {
        try {
            await navigator.clipboard.writeText(currentResults);
            showToast('Results copied to clipboard!', 'success');
        } catch (error) {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = currentResults;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showToast('Results copied to clipboard!', 'success');
        }
    }
}

// Clear input
function clearInput() {
    document.getElementById('markdownInput').value = '';
    document.getElementById('results').innerHTML = '<p class="text-muted text-center mt-5">Results will appear here after processing...</p>';
    document.getElementById('metadata').innerHTML = '';
    document.getElementById('copyBtn').classList.add('d-none');
    currentResults = '';
}

// Load sample content
function loadSample() {
    const sampleMarkdown = `# Technical Documentation Guide

## Introduction

This document provides guidelines for writing technical documentation.

## Writing Style

- Use clear, concise language
- Write in active voice when possible
- Use bullet points for lists
- Include code examples where appropriate

## Code Examples

Here's a simple Python function:

\`\`\`python
def hello_world():
    print("Hello, World!")
\`\`\`

## Best Practices

1. Always include a table of contents for long documents
2. Use consistent formatting throughout
3. Provide examples for complex concepts
4. Keep sentences short and readable

> **Note**: Remember to review your documentation regularly to keep it up-to-date.

## Conclusion

Following these guidelines will help create better technical documentation.
`;
    
    document.getElementById('markdownInput').value = sampleMarkdown;
    showToast('Sample content loaded!', 'info');
}

// Create new style guide
function createStyleGuide() {
    const modal = new bootstrap.Modal(document.getElementById('styleGuideModal'));
    modal.show();
    
    // Load sample style guide content
    document.getElementById('styleGuideContent').value = `# Style Guide Template

## Overview
This style guide defines the writing standards and formatting rules for content.

## Writing Guidelines

### Voice and Tone
- Use active voice
- Write in a professional but approachable tone
- Be concise and direct

### Grammar and Style
- Use sentence case for headings
- Spell out numbers under 10
- Use the Oxford comma

## Formatting Rules

### Headers
- Use ## for main sections
- Use ### for subsections
- Don't skip header levels

### Lists
- Use bullet points for unordered lists
- Use numbers for sequential steps
- Keep list items parallel in structure

### Code
- Use backticks for inline code
- Use code blocks for multi-line examples
- Always specify language for syntax highlighting

## Examples

Good: "Click the **Save** button to save your changes."
Bad: "Click on the Save button in order to save your changes."
`;
}

// Save style guide
async function saveStyleGuide() {
    const name = document.getElementById('styleGuideName').value.trim();
    const content = document.getElementById('styleGuideContent').value.trim();
    
    if (!name || !content) {
        showToast('Please provide both name and content for the style guide.', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/style-guides', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                content: content
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Style guide saved successfully!', 'success');
            
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('styleGuideModal'));
            modal.hide();
            
            // Clear form
            document.getElementById('styleGuideForm').reset();
            
            // Refresh style guide dropdown
            await refreshStyleGuides();
            
            // Select the newly created style guide
            document.getElementById('styleGuideSelect').value = name;
        } else {
            showToast(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Failed to save style guide:', error);
        showToast('Failed to save style guide. Please try again.', 'error');
    }
}

// Refresh style guides dropdown
async function refreshStyleGuides() {
    try {
        const response = await fetch('/api/style-guides');
        const data = await response.json();
        
        if (data.success) {
            const select = document.getElementById('styleGuideSelect');
            const currentValue = select.value;
            
            // Clear existing options except the first one
            select.innerHTML = '<option value="">Select a style guide...</option>';
            
            // Add style guides
            data.style_guides.forEach(guide => {
                const option = document.createElement('option');
                option.value = guide;
                option.textContent = guide;
                select.appendChild(option);
            });
            
            // Restore selection if it still exists
            if (currentValue && data.style_guides.includes(currentValue)) {
                select.value = currentValue;
            }
        }
    } catch (error) {
        console.error('Failed to refresh style guides:', error);
    }
}

// Utility functions
function setLoading(buttonId, spinnerId, isLoading) {
    const button = document.getElementById(buttonId);
    const spinner = document.getElementById(spinnerId);
    
    if (isLoading) {
        button.disabled = true;
        spinner.classList.remove('d-none');
    } else {
        button.disabled = false;
        spinner.classList.add('d-none');
    }
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastBody = document.getElementById('toastBody');
    
    // Set message
    toastBody.textContent = message;
    
    // Set type-specific styling
    toast.className = 'toast';
    if (type === 'error') {
        toast.classList.add('bg-danger', 'text-white');
    } else if (type === 'success') {
        toast.classList.add('bg-success', 'text-white');
    } else if (type === 'warning') {
        toast.classList.add('bg-warning');
    } else {
        toast.classList.add('bg-info', 'text-white');
    }
    
    // Show toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
