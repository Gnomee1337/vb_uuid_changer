import os
import sys
import subprocess
import glob
import re


def generate_uuid(vdi_file):
    """Generate a new UUID for the specified VDI file."""
    try:
        result = subprocess.run(
            ["vboxmanage", "internalcommands", "sethduuid", vdi_file],
            check=True, capture_output=True, text=True
        )
        match = re.search(r'UUID changed to:\s*([a-fA-F0-9-]+)', result.stdout)
        return match.group(1) if match else None
    except subprocess.CalledProcessError as e:
        print("An error occurred while generating UUID:", e)
        return None


def replace_uuids_in_vbox(vbox_path, uuid_1, uuid_2):
    """Replace UUIDs in the .vbox file."""
    try:
        with open(vbox_path, 'r') as file:
            file_content = file.read()

        # Debugging: Print original content
        # print("Original .vbox file content:")
        # print(file_content)

        # Patterns to match UUIDs in the specified tags
        replacements = [
            (r'(<Machine uuid="\{)[^}]*?(\}".*?>)', rf'\1{uuid_1}\2'),  # Match <Machine>
            (r'(<HardDisk uuid="\{)[^}]*?(\}".*?\/>)', rf'\1{uuid_2}\2'),  # Match <HardDisk>
            (r'(<Image uuid="\{)[^}]*?(\}.*?\/>)', rf'\1{uuid_2}\2')  # Match <Image>
        ]

        # Replace UUIDs in the file content
        for pattern, new_uuid in replacements:
            # Print pattern and replacement for debugging
            print(f"Replacing pattern: {pattern} with UUID: {new_uuid}")
            file_content = re.sub(pattern, new_uuid, file_content)

        with open(vbox_path, 'w') as file:
            file.write(file_content)

        # Debugging: Print updated content
        # print("Updated .vbox file content:")
        # print(file_content)

    except FileNotFoundError:
        print(f"Error: The file '{vbox_path}' was not found.")
    except IOError as e:
        print(f"Error while reading or writing to the file: {e}")
    except re.error as e:
        print(f"Regex error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    # Get the path for the machine directory
    machine_path = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))

    # Find .vdi and .vbox files in the specified directory
    vdi_files = glob.glob(os.path.join(machine_path, "*.vdi"))
    vbox_files = glob.glob(os.path.join(machine_path, "*.vbox"))

    if not vdi_files or not vbox_files:
        print("No .vdi or .vbox files found.")
        return

    vdi_path = vdi_files[0]

    # Generate UUIDs for the VDI
    uuid_1 = generate_uuid(vdi_path)
    uuid_2 = generate_uuid(vdi_path)  # Assuming uuid_2 can be the same for this example

    if uuid_1 is None or uuid_2 is None:
        print("Failed to generate the UUIDs for the VDI file.")
        return

    # Print generated UUIDs for debugging
    print(f"Generated UUIDs:\nUUID 1: {uuid_1}\nUUID 2: {uuid_2}")

    # Replace UUIDs in the .vbox file
    replace_uuids_in_vbox(vbox_files[0], uuid_1, uuid_2)


if __name__ == '__main__':
    main()
