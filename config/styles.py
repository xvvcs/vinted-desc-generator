DESCRIPTION_STYLES = {
    'professional': {
        'tone': 'formal and business-like',
        'structure': 'organized with clear sections',
        'format': 'bullet points and clear paragraphs',
        'details': 'comprehensive but concise'
    },
    'casual': {
        'tone': 'friendly and conversational',
        'structure': 'flowing narrative',
        'format': 'paragraphs with occasional bullet points',
        'details': 'key information with personal touch'
    },
    'detailed': {
        'tone': 'technical and precise',
        'structure': 'highly organized with sections',
        'format': 'numbered lists and subsections',
        'details': 'extensive information with measurements'
    },
    'minimal': {
        'tone': 'straightforward and concise',
        'structure': 'simple and direct',
        'format': 'short paragraphs',
        'details': 'essential information only'
    }
}

def get_style_prompt(style_name):
    style = DESCRIPTION_STYLES.get(style_name, DESCRIPTION_STYLES['professional'])
    return f"""Please write the description in a {style['tone']} tone.
    Use a {style['structure']} structure.
    Format the text using {style['format']}.
    Include {style['details']} details.""" 