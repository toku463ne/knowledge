"""
Python script to convert markdown files under data folder to Anki CSV format
Only markdown files with "anki" tag will be converted.
The markdown files will contain strings enclosed in double curly braces {{ }} which will be used as the front side of the Anki card.
The back side will be the rest of the content in the markdown file.
The script will also handle the title and tags of the markdown files.
"""

import os
import csv
from pathlib import Path
import frontmatter

# add the parent directory to the system path to import frontmatter
import sys
sys.path.append(str(Path(__file__).resolve().parent))

# args
import argparse
def parse_args():
    parser = argparse.ArgumentParser(description="Convert markdown files to Anki CSV format.")
    parser.add_argument('--input_dir', type=str, default='data', help='Directory containing markdown files.')
    parser.add_argument('--output_file', type=str, default='anki_cards.csv', help='Output CSV file path.')
    parser.add_argument('--tags', type=str, default='', help='Comma-separated tags to filter markdown files.')
    return parser.parse_args()


def convert_markdown_to_anki_csv(data_dir: str, output_file: str, tags: str = ''):
    """
    Convert markdown files in the specified directory to Anki CSV format.
    
    :param data_dir: Directory containing markdown files.
    :param output_file: Output CSV file path.
    """
    anki_cards = []

    # Iterate through all markdown files in the data directory
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                post = frontmatter.load(file_path)

                # Check if the post has the specified tags
                if tags:
                    tag_list = [tag.strip() for tag in tags.split(',')]
                    if not any(tag in post.get('tags', []) for tag in tag_list):
                        continue

                # Check if the post has the 'anki' tag
                if 'anki' in post.get('tags', []):
                    content = post.content.strip()
                    tags = ', '.join(post.get('tags', []))

                    # Extract front and back content
                    front_content = ''
                    back_content = content

                    # Replace all occurrences of {{string}} with {{***}} in the content for front_content
                    front_content = content
                    start_idx = 0
                    end_idx = 0
                    answer_list = []
                    while '{{' in front_content and '}}' in front_content:
                        start_idx = front_content.find('{{', start_idx + 2)
                        end_idx = front_content.find('}}', start_idx)
                        if start_idx != -1 and end_idx != -1:
                            answer_list.append(front_content[start_idx + 2:end_idx].strip())
                            front_content = (front_content[:start_idx + 2] + '***' + 
                                             front_content[end_idx:])
                        else:
                            break

                    front_content = front_content.replace('\n', '<br>')  # Replace newlines with <br> for HTML compatibility
                    # Keep the original content for back_content
                    back_content = ' '.join(answer_list).replace('\n', '<br>')

                    # Append the card to the list
                    anki_cards.append([front_content, back_content, tags])

    # Write to CSV file
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        #writer.writerow(['Title', 'Front', 'Back', 'Tags'])  # Header
        writer.writerows(anki_cards)


if __name__ == "__main__":
    args = parse_args()
    data_directory = args.input_dir
    output_csv_file = args.output_file
    tags = args.tags
    
    # Convert markdown files to Anki CSV format
    convert_markdown_to_anki_csv(data_directory, output_csv_file, tags)
    print(f"Anki cards have been written to {output_csv_file}")
    print("Conversion complete.")