import os
import time
import logging
from datetime import datetime
from pathlib import Path
import shutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Log to console
    ]
)


class InboxHandler(FileSystemEventHandler):
    """
    Custom event handler to process new files in the Inbox directory.
    """

    def on_created(self, event):
        """
        Triggered when a new file is created in the watched directory.

        Args:
            event: The file system event object
        """
        # Skip directory creation events
        if event.is_directory:
            return

        # Process the new file
        self.process_new_file(event.src_path)

    def process_new_file(self, file_path):
        """
        Process a new file by copying it to Needs_Action/ and creating metadata.

        Args:
            file_path (str): Path to the new file in Inbox/
        """
        try:
            # Convert to Path object for easier manipulation
            src_path = Path(file_path)

            # Define destination directory
            dest_dir = Path("Needs_Action")
            dest_dir.mkdir(exist_ok=True)  # Create if it doesn't exist

            # Prepare destination file path with FILE_ prefix
            dest_file_path = dest_dir / f"FILE_{src_path.name}"

            # Copy the file to Needs_Action/ with FILE_ prefix
            shutil.copy2(src_path, dest_file_path)
            logging.info(f"Copied {src_path.name} to {dest_file_path}")

            # Create metadata for the companion .md file
            file_size = src_path.stat().st_size
            current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            # Prepare the metadata content
            metadata_content = f"""---
type: file_drop
original_name: {src_path.name}
size_bytes: {file_size}
created: {current_time}
status: pending
---

New file dropped for processing.
Please analyze and create a plan."""

            # Create the companion .md file
            metadata_file_path = dest_dir / f"FILE_{src_path.stem}.md"
            with open(metadata_file_path, 'w', encoding='utf-8') as meta_file:
                meta_file.write(metadata_content)

            logging.info(f"Created metadata file: {metadata_file_path}")

        except FileNotFoundError as e:
            logging.error(f"File not found during processing: {e}")
        except PermissionError as e:
            logging.error(f"Permission denied during processing: {e}")
        except OSError as e:
            logging.error(f"OS error during processing: {e}")
        except Exception as e:
            logging.error(f"Unexpected error during file processing: {e}")


def main():
    """
    Main function to set up and start the file system watcher.
    """
    # Define the directory to watch
    inbox_dir = Path("Inbox")

    # Create the Inbox directory if it doesn't exist
    inbox_dir.mkdir(exist_ok=True)
    logging.info(f"Watching directory: {inbox_dir.absolute()}")

    # Create the event handler and observer
    event_handler = InboxHandler()
    observer = Observer()
    observer.schedule(event_handler, str(inbox_dir), recursive=False)

    # Start the observer
    observer.start()
    logging.info("File system watcher started. Press Ctrl+C to stop.")

    try:
        # Run indefinitely
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Handle graceful shutdown on Ctrl+C
        logging.info("Stopping file system watcher...")
        observer.stop()
    except Exception as e:
        # Handle any other exceptions
        logging.error(f"Unexpected error in main loop: {e}")
    finally:
        # Wait for the observer to finish
        observer.join()
        logging.info("File system watcher stopped.")


if __name__ == "__main__":
    main()