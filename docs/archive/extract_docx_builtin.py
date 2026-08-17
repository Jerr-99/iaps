#!/usr/bin/env python3
import zipfile
import xml.etree.ElementTree as ET
import os
from pathlib import Path

os.chdir("/home/jerry99/iaps")

# Define document paths
docs = [
    "ProjectInfor/Sources/Project Overview.docx",
    "ProjectInfor/Sources/Project Proposal - Jerry Lelumai.docx",
    "ProjectInfor/Sources/System Design Specifications.docx",
    "ProjectInfor/Sources/Backgroud-Audit Process.docx",
    "ProjectInfor/Sources/To my project implementation.docx"
]

def extract_text_from_docx(docx_path):
    """Extract text from a .docx file using zipfile and XML parsing."""
    texts = []
    try:
        with zipfile.ZipFile(docx_path, 'r') as zip_ref:
            # Read the main document XML
            with zip_ref.open('word/document.xml') as xml_file:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Define namespace
                ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                
                # Extract all text elements
                for paragraph in root.findall('.//w:p', ns):
                    para_text = []
                    for text_elem in paragraph.findall('.//w:t', ns):
                        if text_elem.text:
                            para_text.append(text_elem.text)
                    if para_text:
                        texts.append(''.join(para_text))
    except Exception as e:
        print(f"Error extracting text: {e}")
        return []
    
    return texts

# Extract content from each document
for doc_path in docs:
    try:
        print(f"\n{'='*80}")
        print(f"FILE: {doc_path}")
        print(f"{'='*80}\n")
        
        texts = extract_text_from_docx(doc_path)
        for text in texts:
            if text.strip():
                print(text)
                
    except Exception as e:
        print(f"Error reading {doc_path}: {e}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*80}")
print("EXTRACTION COMPLETE")
print(f"{'='*80}\n")
