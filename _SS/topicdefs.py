from mcap.reader import make_reader
import json
import os

def inspect_mcap_topics(mcap_file_path, output_file=None):
    """
    Extract and display topic definitions from an MCAP file.
    Optionally save to a text file.
    
    Args:
        mcap_file_path: Path to the .mcap file
        output_file: Path to output .txt file (optional, defaults to same name as mcap)
    """
    # Default output file name
    if output_file is None:
        base_name = os.path.splitext(mcap_file_path)[0]
        output_file = f"{base_name}_topics.txt"
    
    # Open output file for writing
    with open(output_file, 'w') as out:
        def write_line(text=""):
            """Helper to write to both console and file"""
            print(text)
            out.write(text + "\n")
        
        with open(mcap_file_path, "rb") as f:
            reader = make_reader(f)
            
            # Get summary information
            summary = reader.get_summary()
            
            write_line("=" * 80)
            write_line(f"MCAP File: {mcap_file_path}")
            write_line(f"Total Topics: {len(summary.channels)}")
            write_line("=" * 80)
            write_line()
            
            # Create a mapping of schema_id to schema
            schemas = {schema.id: schema for schema in summary.schemas.values()}
            
            # Iterate through each channel (topic)
            for channel_id, channel in summary.channels.items():
                write_line(f"Topic: {channel.topic}")
                write_line(f"  Message Type: {channel.message_encoding}")
                write_line(f"  Schema: {channel.schema_id}")
                
                # Get the schema for this channel
                if channel.schema_id in schemas:
                    schema = schemas[channel.schema_id]
                    write_line(f"  Schema Name: {schema.name}")
                    write_line(f"  Schema Encoding: {schema.encoding}")
                    write_line()
                    write_line("  Message Definition:")
                    write_line("  " + "-" * 76)
                    
                    # Display the schema data (usually the message definition)
                    schema_text = schema.data.decode('utf-8')
                    for line in schema_text.split('\n'):
                        write_line(f"  {line}")
                    
                write_line()
                write_line("=" * 80)
                write_line()
        
        print(f"\nOutput saved to: {output_file}")

# Usage
if __name__ == "__main__":
    # Replace with your MCAP file path
    mcap_file = "bag_file/robot_1_quad_log_spirit_20251008_1525_0.mcap"
    
    # Option 1: Use default output file name (adds _topics.txt to the input filename)
    inspect_mcap_topics(mcap_file, "robot_topics_defs.txt")
    
    # Option 2: Specify custom output file name
    # inspect_mcap_topics(mcap_file, "robot_topics_definitions.txt")