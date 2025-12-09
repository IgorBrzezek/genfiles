# ==================================================================================
# genfiles.py

import argparse
import os
import random
import string
from typing import Optional, Dict, Any 

# --- Metadata ---
_AUTHOR = "Igor Brzezek"
_DATE = "09.12.2025"
_EMAIL = "igor.brzezek@gmail.com"
_GITHUB = "https://github.com/igorbrzezek/genfiles"
_VERSION = "1.0.2"
# -----------------

def generate_random_data(size_bytes: int, is_binary: bool) -> bytes:
    """Generates random data of the specified size, either text or binary."""
    if is_binary:
        # Random bytes
        return os.urandom(size_bytes)
    else:
        # Random text (ASCII characters)
        characters = string.ascii_letters + string.digits + ' \n\t'
        random_text = ''.join(random.choice(characters) for _ in range(size_bytes))
        return random_text.encode('utf-8')

def create_files_simple(root_dir: str, num_files: int, size_kb: int) -> Dict[str, Any]:
    """Creates a specified number of binary files of a fixed size in the root directory."""
    
    file_size_bytes = size_kb * 1024
    
    print(f"Creating files in directory: {root_dir}")
    os.makedirs(root_dir, exist_ok=True)

    stats = {
        'total_files': 0,
        'total_size_bytes': 0,
    }

    for i in range(1, num_files + 1):
        file_name = f"fixed_file_{i:03d}.bin"
        file_path = os.path.join(root_dir, file_name)
        
        # Always binary data
        data = generate_random_data(file_size_bytes, is_binary=True)
        
        try:
            with open(file_path, "wb") as f:
                f.write(data)
            
            size_mb = file_size_bytes / (1024 * 1024)
            print(f"  Created file: {file_name} (binary, {size_mb:.2f} MB)")
            
            # Update stats
            stats['total_files'] += 1
            stats['total_size_bytes'] += file_size_bytes
            
        except IOError as e:
            print(f"  Error writing file {file_name}: {e}")
            
    return stats


def create_structured_files(
    root_dir: str, N: int, M: int, K: int, file_type: str,
    min_size_bytes: int = 100
) -> Dict[str, Any]:
    """
    Creates the root directory, N subdirectories, and 1..M files in each.
    Returns statistics about the generated files. (Original logic)
    """
    
    # Convert K kilobytes to bytes
    max_size_bytes = K * 1024
    
    print(f"Creating structured directory: {root_dir}")
    os.makedirs(root_dir, exist_ok=True)
    
    # Check if minimum size is reasonable
    if min_size_bytes > max_size_bytes:
        print(f"Warning: Minimum size ({min_size_bytes}B) is larger than maximum ({max_size_bytes}B). Setting minimum to maximum.")
        min_size_bytes = max_size_bytes

    # Statistics tracking
    stats = {
        'total_files': 0,
        'binary_files': 0,
        'text_files': 0,
        'total_size_bytes': 0,
        'binary_size_bytes': 0,
        'text_size_bytes': 0,
    }
        
    for i in range(1, N + 1):
        # Create subdirectory name
        subdir_name = f"subdir_{i:03d}"
        subdir_path = os.path.join(root_dir, subdir_name)
        os.makedirs(subdir_path, exist_ok=True)
        print(f"  Created subdirectory: {subdir_name}")
        
        # Random number of files in the range 1 to M
        num_files = random.randint(1, M)
        
        for j in range(1, num_files + 1):
            # Determine file type
            if file_type == 'bin':
                is_binary = True
            elif file_type == 'txt':
                is_binary = False
            else: # 'mix'
                is_binary = random.choice([True, False])

            # Randomize file size
            file_size = random.randint(min_size_bytes, max_size_bytes)
            
            # Create file name
            extension = ".bin" if is_binary else ".txt"
            file_name = f"file_{j:03d}{extension}"
            file_path = os.path.join(subdir_path, file_name)
            
            # Generate data
            data = generate_random_data(file_size, is_binary)
            
            # Write file
            try:
                with open(file_path, "wb") as f:
                    f.write(data)
                
                type_str = "binary" if is_binary else "text"
                size_kb = file_size / 1024
                print(f"    Created file: {file_name} ({type_str}, {size_kb:.2f} KB)")

                # Update stats
                stats['total_files'] += 1
                stats['total_size_bytes'] += file_size
                if is_binary:
                    stats['binary_files'] += 1
                    stats['binary_size_bytes'] += file_size
                else:
                    stats['text_files'] += 1
                    stats['text_size_bytes'] += file_size
                    
            except IOError as e:
                print(f"    Error writing file {file_name}: {e}")

    return stats


def print_structured_statistics(stats: Dict[str, Any]) -> None:
    """Prints a summary of the generated structured file statistics."""
    total_files = stats['total_files']
    
    if total_files == 0:
        print("\nNo files were generated.")
        return

    # Calculate averages
    avg_total_size = stats['total_size_bytes'] / total_files / 1024 if total_files > 0 else 0
    
    binary_files = stats['binary_files']
    avg_binary_size = stats['binary_size_bytes'] / binary_files / 1024 if binary_files > 0 else 0
    
    text_files = stats['text_files']
    avg_text_size = stats['text_size_bytes'] / text_files / 1024 if text_files > 0 else 0

    # Total sizes in MB
    total_size_mb = stats['total_size_bytes'] / (1024 * 1024)
    binary_size_mb = stats['binary_size_bytes'] / (1024 * 1024)
    text_size_mb = stats['text_size_bytes'] / (1024 * 1024)
    
    print("\n--- Structured Generation Statistics ---")
    print(f"Total files generated: {total_files}")
    print(f"Total size: {total_size_mb:.2f} MB")
    print("-" * 30)
    
    print(f"Binary files: {binary_files}")
    print(f"  Total size (Binary): {binary_size_mb:.2f} MB")
    print(f"  Average size (Binary): {avg_binary_size:.2f} KB")
    print("-" * 30)

    print(f"Text files: {text_files}")
    print(f"  Total size (Text): {text_size_mb:.2f} MB")
    print(f"  Average size (Text): {avg_text_size:.2f} KB")
    print("-" * 30)
    
    
def print_simple_statistics(stats: Dict[str, Any]) -> None:
    """Prints a summary for the simple file creation mode."""
    total_files = stats['total_files']
    total_size_mb = stats['total_size_bytes'] / (1024 * 1024)
    avg_size_mb = total_size_mb / total_files if total_files > 0 else 0
    
    print("\n--- Simple File Creation Statistics ---")
    print(f"Total files created: {total_files}")
    print(f"File type: Binary (Fixed Size)")
    print(f"Total size: {total_size_mb:.2f} MB")
    print(f"Average file size: {avg_size_mb:.2f} MB")
    print("-" * 30)


def main(args: Optional[list] = None) -> None:
    """Main function to parse arguments and run file creation."""
    parser = argparse.ArgumentParser(
        description=f"Generates a directory and file structure for testing purposes.\nVersion: {_VERSION}\nAuthor: {_AUTHOR} ({_EMAIL})\nGitHub: {_GITHUB}",
        formatter_class=argparse.RawTextHelpFormatter # For better description formatting
    )
    
    # --- Directory Option (Required for both modes) ---
    parser.add_argument(
        '-d', '--directory',
        type=str,
        required=True,
        help="Name of the root directory to be created (required)."
    )
    
    # --- Simple File Creation Mode (Mutually Exclusive Group 1) ---
    # This mode overrides the structure creation options.
    simple_group = parser.add_argument_group('Simple Creation Mode (Overrides Structure)')
    simple_group.add_argument(
        '-fc', '--file-create',
        type=int,
        nargs=2,
        metavar=('N', 'M'),
        help="Simple file creation mode: Create N binary files, each of size M kilobytes (KB). N is file count, M is size in KB. (Overrides -n, -m, -k, --bin, --txt, --mix)"
    )

    # --- Structured Creation Mode Options (Mutually Exclusive Group 2) ---
    structure_group = parser.add_argument_group('Structured Creation Mode (Default)')
    structure_group.add_argument(
        '-n',
        type=int,
        help="Number N of subdirectories to create (e.g., 10). Required only in structured mode."
    )
    structure_group.add_argument(
        '-m', '--max-files',
        type=int,
        help="Maximum number M of files (from 1 to M) in each subdirectory (e.g., 5). Required only in structured mode.",
        dest='max_files' # 'max_files' as dest
    )
    structure_group.add_argument(
        '-k', '--max-size-kb',
        type=int,
        help="Maximum size K of files in kilobytes (KB) (e.g., 1024). Required only in structured mode.",
        dest='max_size_kb' # 'max_size_kb' as dest
    )
    
    # File Type Options
    type_group = structure_group.add_mutually_exclusive_group()
    type_group.add_argument(
        '--bin',
        action='store_const',
        const='bin',
        dest='file_type',
        help="Generate only binary files (Structured Mode)."
    )
    type_group.add_argument(
        '--txt',
        action='store_const',
        const='txt',
        dest='file_type',
        help="Generate only text files (Structured Mode)."
    )
    type_group.add_argument(
        '--mix',
        action='store_const',
        const='mix',
        dest='file_type',
        default='mix',
        help="Generate a mix of binary and text files (approx. 50/50 - default in Structured Mode)."
    )

    # Statistics Option
    parser.add_argument(
        '--stat',
        action='store_true',
        help="Show statistics on the generated files (count, total size, average size)."
    )
    
    # Parse arguments
    if args:
        parsed_args = parser.parse_args(args)
    else:
        parsed_args = parser.parse_args()

    # --- Determine Mode and Validation ---
    
    is_simple_mode = parsed_args.file_create is not None
    
    if is_simple_mode:
        N_files, M_size_kb = parsed_args.file_create
        
        if N_files <= 0 or M_size_kb <= 0:
            parser.error("For --file-create, both N (file count) and M (size in KB) must be integers greater than 0.")
            
        # Run Simple Mode
        try:
            stats = create_files_simple(
                root_dir=parsed_args.directory,
                num_files=N_files,
                size_kb=M_size_kb
            )
            print(f"\nFinished successfully. Created files in directory: {parsed_args.directory}")
            if parsed_args.stat:
                print_simple_statistics(stats)
        except Exception as e:
            print(f"\nAn error occurred during simple file creation: {e}")

    else:
        # Structured Mode Validation 
        if parsed_args.n is None or parsed_args.max_files is None or parsed_args.max_size_kb is None:
             parser.error("When --file-create is not used, -n, -m, and -k are required for structured generation.")
             
        if parsed_args.n <= 0:
            parser.error("-n must be an integer greater than 0.")
        if parsed_args.max_files <= 0:
            parser.error("-m/--max-files must be an integer greater than 0.")
        if parsed_args.max_size_kb <= 0:
            parser.error("-k/--max-size-kb must be an integer greater than 0.")
        
        # Run Structured Mode
        try:
            stats = create_structured_files(
                root_dir=parsed_args.directory,
                N=parsed_args.n,
                M=parsed_args.max_files,
                K=parsed_args.max_size_kb,
                file_type=parsed_args.file_type if parsed_args.file_type else 'mix'
            )
            print(f"\nFinished successfully. Structure created in directory: {parsed_args.directory}")
            if parsed_args.stat:
                print_structured_statistics(stats)
                
        except Exception as e:
            print(f"\nAn error occurred during structured file generation: {e}")

if __name__ == "__main__":
    main()
# ==================================================================================
