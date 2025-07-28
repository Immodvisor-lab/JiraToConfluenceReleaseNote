from release_note import ReleaseNote

def generate_release_note():
    release_note = ReleaseNote()
    print("Release note object created")
    #version = "2.33.0"
    #release_note.set_version(version)
    release_note.set_version()
    print("Version set")
    release_note.set_issues()
    print("Issues set")
    html = release_note.set_content()
    #print(html)
    print("Content set")
    release_note.create_or_update()
    print("See the release note : "+release_note.url)
    return True

if __name__ == "__main__":
    while True:
        try:
            generate_release_note()
            
            # Options menu
            print("\nWhat would you like to do?")
            print("1 - Generate again")
            print("2 - Quit")
            
            while True:
                choice = input("Enter your choice (1 or 2): ").strip()
                if choice == "1":
                    print("\n" + "="*50)
                    break
                elif choice == "2":
                    print("Goodbye!")
                    exit()
                else:
                    print("Invalid choice. Please enter 1 or 2.")
        except KeyboardInterrupt:
            print("\nProgram interrupted. Goodbye!")
            exit()
        except Exception as e:
            print(f"An error occurred: {e}")
            print("\nWhat would you like to do?")
            print("1 - Try again")
            print("2 - Quit")
            
            while True:
                choice = input("Enter your choice (1 or 2): ").strip()
                if choice == "1":
                    print("\n" + "="*50)
                    break
                elif choice == "2":
                    print("Goodbye!")
                    exit()
                else:
                    print("Invalid choice. Please enter 1 or 2.")

