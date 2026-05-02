# file_locker.py
import os
import subprocess
import getpass
import sys

class FileLocker:
    def __init__(self):
        self.check_gpg()
    
    def check_gpg(self):
        """Check if GPG is installed"""
        try:
            subprocess.run(['gpg', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: GPG is not installed. Install it with:")
            print("  Ubuntu/Debian: sudo apt install gnupg")
            print("  Mac: brew install gnupg")
            print("  Windows: install Gpg4win")
            sys.exit(1)
    
    def lock_file(self, filename, password):
        """Encrypt and lock a file"""
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found!")
            return False
        
        # Create encrypted file
        output_file = filename + '.gpg'
        
        # Use gpg with symmetric encryption
        cmd = [
            'gpg', '--symmetric', '--batch', '--yes',
            '--passphrase', password,
            '--output', output_file, filename
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            # Remove original file
            os.remove(filename)
            print(f"✓ File locked successfully: {output_file}")
            print(f"✓ Original file removed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error locking file: {e.stderr.decode() if e.stderr else 'Unknown error'}")
            return False
    
    def unlock_file(self, filename, password):
        """Decrypt and unlock a file"""
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found!")
            return False
        
        # Remove .gpg extension for output
        if filename.endswith('.gpg'):
            output_file = filename[:-4]
        else:
            output_file = filename + '.decrypted'
        
        cmd = [
            'gpg', '--decrypt', '--batch', '--yes',
            '--passphrase', password,
            '--output', output_file, filename
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            # Remove encrypted file
            os.remove(filename)
            print(f"✓ File unlocked successfully: {output_file}")
            print(f"✓ Encrypted file removed")
            return True
        except subprocess.CalledProcessError:
            print("Error: Wrong password or corrupted file!")
            return False

def main():
    print("=" * 50)
    print("FILE LOCKER TOOL (GPG Encryption)")
    print("=" * 50)
    
    locker = FileLocker()
    
    while True:
        print("\nOptions:")
        print("1. Lock a file")
        print("2. Unlock a file")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            filename = input("Enter file name to lock: ").strip()
            password = getpass.getpass("Enter password: ")
            confirm = getpass.getpass("Confirm password: ")
            
            if password != confirm:
                print("Error: Passwords don't match!")
                continue
            
            if len(password) < 4:
                print("Warning: Weak password! Use at least 4 characters.")
            
            locker.lock_file(filename, password)
        
        elif choice == '2':
            filename = input("Enter encrypted file name (.gpg): ").strip()
            password = getpass.getpass("Enter password: ")
            locker.unlock_file(filename, password)
        
        elif choice == '3':
            print("Goodbye!")
            break
        
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
