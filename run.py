from release_note import ReleaseNote

if __name__ == "__main__":
    release_note = ReleaseNote()
    print("Release note object created")
    release_note.set_version()
    print("Version set")
    release_note.set_issues()
    print("Issues set")
    html = release_note.set_content()
    #print(html)
    print("Content set")
    release_note.create_or_update()
    print("Terminated : "+release_note.url())

