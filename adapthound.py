import sqlite3
import json
import sys
import re

def clean_a_text(texts):
    combined_text = '\n'.join(texts)
    # Split into lines
    lines = combined_text.split('\n')
    # Remove lines matching the pattern [MM/DD HH:MM:SS] [+] BOF output
    cleaned_lines = [line for line in lines if not re.match(r'\[\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2}\]\s*\[\+\]\s*BOF output', line)]
    # Join the remaining lines, preserving newlines for meaningful data
    return '\n'.join(line for line in cleaned_lines if line.strip())

def retrieve_and_parse_packets(db_path, task_id, output_file):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = """
        SELECT packet
        FROM consoles
        WHERE json_extract(packet, '$.a_task_id') = ?
        """
        
        cursor.execute(query, (task_id,))
        rows = cursor.fetchall()

        texts = []
        for row in rows:
            try:
                packet = json.loads(row[0])
                a_text = packet.get('a_text', '')
                if a_text:  # Only include non-empty a_text
                    texts.append(a_text)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON: {row[0]}")
                continue
        
        # Clean and combine the texts
        if texts:
            cleaned_text = clean_a_text(texts)
            if cleaned_text:
                # Write to output file
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(cleaned_text + '\n')
                print(f"Saved cleaned a_text to {output_file}")
                return cleaned_text
            else:
                print(f"No non-empty cleaned a_text found for task_id '{task_id}'.")
                return ""
        else:
            print(f"No non-empty a_text found for task_id '{task_id}'.")
            return ""
    
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return ""
    except IOError as e:
        print(f"Error writing to file: {e}")
        return ""
    
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <Path to db usually AdaptixC2/dist/data/adaptixserver.db> <Task ID> <output_file>")
        sys.exit(1)
    
    db_path = sys.argv[1]
    task_id = sys.argv[2]
    output_file = sys.argv[3]
    
    cleaned_text = retrieve_and_parse_packets(db_path, task_id, output_file)
    
    if cleaned_text:
        print(f"\nCleaned a_text for task_id '{task_id}':")
        print(cleaned_text)
        print("\n---\n")
    else:
        print(f"No non-empty cleaned a_text entries found for task_id '{task_id}'.")
