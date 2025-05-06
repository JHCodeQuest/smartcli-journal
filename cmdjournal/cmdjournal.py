#!/usr/bin/env python3
from datetime import datetime
import os
from .database import add_entry, view_entries, add_tag, get_entries_by_tag
import sqlite3
from textblob import TextBlob

connection = sqlite3.connect("journal.db")

def create_journal():
    # ask user to name journal
    name = input("Name your journal: ")
    #find the current directory to create journal in
    cwd = os.getcwd() #os import to get current path
    path = os.path.join(cwd, name) #concatenate to create a new path
    #Create journal
    try:
        os.mkdir(path)
    except OSError:
        print(f"Creation of the directory {path} failed")
    else:
        print("Successfully created the directory")
        
def open_journal():
    # Already in the current working directory
    # Get a list of journals within the current directory
    journal_list = os.listdir()
    #Loop through the list of journals and print them one by one
    print("current journals: " + str(len(journal_list)))
    for journal in journal_list:
        print(journal)
    #Ask the user to choose a journal out of the list
    name = input("Name of journal: ")
    cwd = os.getcwd()
    #Create the path to move into
    path = cwd + "/" + name
    #move the path once created
    os.chdir(path)
    #Get list of entries
    directory_list = os.listdir()
    #loop through list and print them one by one
    print("Current Entries: " + str(len(directory_list)))
    for entry in directory_list:
        print(entry)
        
def fetch_content():
    # grab text from user
    content = input("Write away :)")
    return content

def add_content():
    #Ask user for title for their entry
    title = input("What is the title of your entry?")
    #fetch content for the entry
    content = fetch_content()
    #generate a filename, fix document spacing and make it a .txt file
    filename = title.replace(" ","") + ".txt"
    author = input("What is your author name for entry? ")
    words = content.split()
    with open(filename, "a") as entry:
        #add authors name
        entry.write(author + "\n")
        #add title
        entry.write(title + "\n")
        # add date
        entry.write(str(datetime.now()) + "\n")
        #loop through content and add \n
        for i in range(0, len(words), 10):
            entry.write(" ".join(words[i:i+10]) + "\n")

    # Perform NLP emotion analysis using TextBlob
    analysis = TextBlob(content)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity

    if polarity > 0.3:
        emotion_label = "Strongly Positive"
    elif 0 < polarity <= 0.3:
        emotion_label = "Positive"
    elif polarity == 0:
        emotion_label = "Neutral"
    elif -0.3 < polarity < 0:
        emotion_label = "Negative"
    else:
        emotion_label = "Strongly Negative"

    subjectivity_label = "Objective" if subjectivity < 0.5 else "Subjective"

    # Ask if it's a dream entry
    is_dream = input("Is this a dream entry? (y/n): ").lower() == 'y'
    dream_meaning = ""
    if is_dream:
        # Very basic example of dream interpretation based on keywords
        if "water" in content.lower():
            dream_meaning = "Represents emotions and the unconscious."
        elif "flying" in content.lower():
            dream_meaning = "Symbolizes freedom or a desire to escape."
        else:
            dream_meaning = "Dream meaning not clear."

    # Save to database with emotion and dream meaning
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO entries (content, date, emotion, subjectivity, dream_meaning) VALUES (?, ?, ?, ?, ?)",
        (content, str(datetime.now()), emotion_label, subjectivity_label, dream_meaning)
    )
    connection.commit()

def add_page(title=None):
    #title of page
    if title is None:
        title = input("Name your entry: ")
    filename = title.replace(" ","") + ".txt"
    #add page
    # TODO: Define how add_entry should work here
    add_entry()

def remove_page():
    # Ask the user to specify part of the entry to identify it
    content_snippet = input("Enter part of the entry you want to delete: ")
    # Remove the entry based on the content match
    cursor = connection.cursor()
    cursor.execute("DELETE FROM entries WHERE content LIKE ?", ('%' + content_snippet + '%',))
    connection.commit()
    print("Matching entry removed from the database.")

def update_entry():
    # Ask the user to identify the entry to update
    old_snippet = input("Enter part of the entry you want to update: ")
    # Get new content from the user
    new_content = input("Enter the new content: ")
    new_date = datetime.now().isoformat()
    # Update the matching entry in the database
    cursor = connection.cursor()
    cursor.execute("UPDATE entries SET content = ?, date = ? WHERE content LIKE ?", (new_content, new_date, '%' + old_snippet + '%'))
    connection.commit()
    
    print("Entry updated.")
    
def search_entries_by_keyword():
    keyword = input("Enter a keyword to search for: ")
    cursor = connection.cursor()
    cursor.execute("SELECT content, date, emotion FROM entries WHERE content LIKE ?", ('%' + keyword + '%',))
    results = cursor.fetchall()
    if results:
        for content, date, emotion in results:
            print("Date:", date)
            print("Emotion:", emotion)
            print("Content Snippet:", content[:100] + "..." if len(content) > 100 else content)
            print("-----")
    else:
        print("No entries found containing that keyword.")

def filter_entries_by_date():
    #prompt for date or date range
    #convert to ISO format
    #query database for entries where date between start and end
    #display entries
    pass

def add_tag_to_entry():
    snippet = input("Enter part of the entry to tag: ")
    tag = input("Enter the tag: ")
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, content FROM entries WHERE content LIKE ?", ('%' + snippet + '%',))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"ID: {row[0]}, Content: {row[1][:50]}...")
        entry_id = int(input("Enter the ID of the entry to tag: "))
        add_tag(entry_id, tag)
        print("Tag added.")
    else:
        print("No matching entry found.")

def view_entries_by_tag():
    tag = input("Enter the tag to filter by: ")
    entries = get_entries_by_tag(tag)
    if entries:
        for entry in entries:
            print(f"ID: {entry[0]}")
            print(f"Content: {entry[1]}")
            print(f"Created At: {entry[2]}")
            print("-----")
    else:
        print("No entries found for this tag.")

def encrypt_entry():
    #Use key from user or config
    #encrypt the entry content before writing to file or database
    pass

def decrypt_entry():
    #use key
    #decrypt and displat entry
    pass

def analyze_entries():
    cursor = connection.execute("SELECT content, emotion, subjectivity, dream_meaning FROM entries")
    for content, emotion, subjectivity, dream_meaning in cursor.fetchall():
        print("Entry Snippet:", content[:50])
        print("Emotion Tone:", emotion)
        print("Subjectivity:", subjectivity)
        if dream_meaning:
            print("Dream Interpretation:", dream_meaning)
        print("-----")

def controls():
    while True:
        # enable user to use journal
        print("What would you like to do?: ")
        #allow user to select functions
        print("1: Create a journal")
        print("2: Open a journal and view entries by tag")
        print("3: Create an entry")
        print("4: Add to an entry")
        print("5: Remove an entry")
        print("6: Update an entry (database)")
        print("7: Add a tag to an entry")
        print("8: View entries by tag")
        print("9: Analyze entries for emotion and dreams")
        print("10: Search entries by keyword")
        #option for search
        option = input("Your choice: ")
        print("-----\n-----")

        # execute the function the user selected

        if option == "1":
            create_journal()
        elif option == "2":
            open_journal()
            view_entries_by_tag()
        elif option == "3":
            add_page()
        elif option == "4":
            add_entry()
        elif option == "5":
            remove_page()
        elif option == "6":
            update_entry()
        elif option == "7":
            add_tag_to_entry()
        elif option == "8":
            view_entries_by_tag()
        elif option == "9":
            analyze_entries()
        elif option == "10":
            search_entries_by_keyword()
        elif option == "0":
            choice = input("Do you need anything else? (y/n): ").strip().lower()
            if choice in ("y", "yes"):
                controls()
            else:
                print("Goodbye!")
                close_connection()
        else:
           print("Please enter a valid option")
        
   
    
def create_table():
    with connection:
        connection.execute("CREATE TABLE entries (content TEXT, date TEXT, emotion TEXT, subjectivity TEXT, dream_meaning TEXT);")
  
def close_connection():
    connection.close()