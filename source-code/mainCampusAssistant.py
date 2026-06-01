#===================================================
#Imports
# os: provides access to operating system functionality such as file paths
#datetime: used for validating and comparing date/time input
#json: used for reading and writing persistent mock data files
#===================================================
import os
from datetime import datetime
import json

#===================================================
#Terminal formatting: used for readability in some terminal output
#===================================================
bold = "\033[1m"
reset = "\033[0m"

#===================================================
# BASE_DIR stores the folder where this Python file is located.
# All JSON paths are built from BASE_DIR so the program can always find the data files reliably.
#===================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EVENTS_PATH = os.path.join(BASE_DIR, "events.json")
BORROWED_PATH = os.path.join(BASE_DIR, "borrowed_items.json")
ROOMS_PATH = os.path.join(BASE_DIR, "study_rooms.json")

#===================================================
#Load JSON data with error handling for missing or malformed files; prevents crashes.
#Uses safe defaults to ensure smooth program operation.
#===================================================
try:
    with open(EVENTS_PATH) as f:
        events = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    events = {"events": []}

try:
    with open(BORROWED_PATH) as f:
        borrowed_items = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    borrowed_items = []

try:
    with open(ROOMS_PATH) as f:
        study_rooms = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    study_rooms = []

#===================================================
#Helper function:
#save_json(): writes updated program data to a JSON file using a safe, absolute path.
#This ensures persistent storage and prevents file path errors across different environments.
#===================================================
def save_json(filename, data):
    with open(os.path.join(BASE_DIR, filename), "w") as f:
        json.dump(data, f, indent=4)

#===================================================
#Backup/Restore Functions
#backup_all_data(): saves all datasets to separate backup JSON files
#restore_all_data(): loads backup JSON files back into memory (overwrites current data)
#===================================================
def backup_all_data():
    save_json("backup_events.json", events)
    save_json("backup_study_rooms.json", study_rooms)
    save_json("backup_borrowed_items.json", borrowed_items)
    print("All data backed up successfully.")

def restore_all_data():
    global events, study_rooms, borrowed_items
    try:
        with open(os.path.join(BASE_DIR, "backup_events.json")) as f:
            events = json.load(f)
        with open(os.path.join(BASE_DIR, "backup_study_rooms.json")) as f:
            study_rooms = json.load(f)
        with open(os.path.join(BASE_DIR, "backup_borrowed_items.json")) as f:
            borrowed_items = json.load(f)
        print("All data restored successfully.")
    except FileNotFoundError:
        print("Backup files not found. Restore failed.")



#===================================================
#Main menu loop (runs until user exits)
#Includes input validation to prevent crashes from invalid inputs.
#===================================================
while True:
    #===================================================
    #Main menu options
    #===================================================
    try:

        option = int(input(
            "Welcome to the Campus Assistant! Please choose an option:\n"
            "1. View upcoming events and timetables\n"
            "2. Search for available study spaces/rooms\n"
            "3. Track borrowed items\n"
            "4. Backup/Restore data\n"
            "0. Exit\n"
            ).strip())
        
    except ValueError:
        print("Invalid input. Please enter a number corresponding to the options.")
        continue
    
    #==================================================
    #Option 0: Exit program
    #==================================================
    if option == 0:
        print("Exiting the Campus Assistant. Have a great day!")
        break

    #==================================================
    #Option 1: Displays upcoming events
    #==================================================
    elif option == 1:
        print("Upcoming Events:")
        for event in events["events"]:
            print(
                f"{bold}EVENT{reset}: {event['event_name']} | "
                f"{bold}LOCATION{reset}: {event['location']} | "
                f"{bold}DATE{reset}: {event['date']} | "
                f"{bold}TIME{reset}: {event['time']}"
                )

    #==================================================
    #Option 2: Study room browsing and searching
    #Includes filtering by building, capacity, and time.
    #==================================================
    elif option == 2: 
        while True:
            try:
                study_room_option = int(input(
                    "Would you like to:\n"
                    "1. View all study rooms\n"
                    "2. View all available study rooms\n"
                    "3. View all booked study rooms\n"
                    "4. Search for available rooms (filters: building/capacity/time)\n"
                    "0. Back to main menu\n"
                    ).strip())
            except ValueError:
                print("Invalid input. Please enter a number corresponding to the options.")
                continue

            if study_room_option == 0:
                break

            elif study_room_option == 1:
                print("\nAll Study Rooms:\n")
                for room in study_rooms:
                    print(
                        f"{bold}ROOM ID{reset}: {room.get('room_id')} | "
                        f"{bold}BUILDING{reset}: {room.get('building')} | "
                        f"{bold}CAPACITY{reset}: {room.get('capacity')} | "
                        f"{bold}AVAILABILITY{reset}: {room.get('availability')} | "
                        f"{bold}FROM{reset}: {room.get('available_from')} | "
                        f"{bold}UNTIL{reset}: {room.get('available_until')}"
                        )
                    
            elif study_room_option == 2:
                print("\nAvailable Study Rooms:\n")
                found = False
                for room in study_rooms:
                    if room.get("availability") == "Available":
                        print(
                            f"{bold}ROOM ID{reset}: {room.get('room_id')} | "
                            f"{bold}BUILDING{reset}: {room.get('building')} | "
                            f"{bold}CAPACITY{reset}: {room.get('capacity')} | "
                            f"{bold}AVAILABILITY{reset}: {room.get('availability')} | "
                            f"{bold}FROM{reset}: {room.get('available_from')} | "
                            f"{bold}UNTIL{reset}: {room.get('available_until')}"
                            )
                        found = True
                if not found:
                    print("No available study rooms found.")

            elif study_room_option == 3:
                print("\nBooked Study Rooms:\n")
                found = False
                for room in study_rooms:
                    if room.get("availability") == "Booked":
                        print(
                            f"{bold}ROOM ID{reset}: {room.get('room_id')} | "
                            f"{bold}BUILDING{reset}: {room.get('building')} | "
                            f"{bold}CAPACITY{reset}: {room.get('capacity')} | "
                            f"{bold}AVAILABILITY{reset}: {room.get('availability')} | "
                            f"{bold}FROM{reset}: {room.get('available_from')} | "
                            f"{bold}UNTIL{reset}: {room.get('available_until')}"
                            )
                        found = True
                if not found:
                    print("No booked study rooms found.")
            #==================================================                    
            #Search available rooms using sequential filtering:
            #1) availability must be "Available"
            #2) building matches (if provided)
            #3) capacity meets minimum (if provided)
            #4) desired time falls within available_from .. available_until .. (if provided)
            #==================================================
            elif study_room_option == 4:

                building_filter = input("Which building would you like to study in? (press Enter to skip): ").strip()
                capacity_raw = input("What is the minimum capacity you require? (press Enter to skip): ").strip()
                time_input = input("Enter desired time (HH:MM) (press Enter to skip): ").strip()

                # Capacity validation
                min_capacity = None
                if capacity_raw:
                    try:
                        min_capacity = int(capacity_raw)
                    except ValueError:
                        print("Invalid capacity input. Please enter a number.")
                        continue

                # Time validation (single time, not a range)
                desired_time = None
                if time_input:
                    try:
                        desired_time = datetime.strptime(time_input, "%H:%M").time()
                    except ValueError:
                        print("Invalid time format. Please use HH:MM (e.g., 14:30).")
                        continue

                found = False

                for room in study_rooms:
                    # Only AVAILABLE rooms (matches the requirement)
                    if room.get("availability") != "Available":
                        continue

                    # Building filter (case-insensitive)
                    if building_filter and room.get("building", "").lower() != building_filter.lower():
                        continue

                    # Capacity filter (minimum)
                    if min_capacity is not None and int(room.get("capacity", 0)) < min_capacity:
                        continue

                    # Time filter: desired_time must be within available_from .. available_until
                    if desired_time is not None:
                        start = room.get("available_from")
                        end = room.get("available_until")

                        # If time fields missing, skip (can't prove time availability)
                        if not start or not end:
                            continue

                        try:
                            start_time = datetime.strptime(start, "%H:%M").time()
                            end_time = datetime.strptime(end, "%H:%M").time()
                        except ValueError:
                            continue

                        if not (start_time <= desired_time <= end_time):
                            continue

                    # If all filters pass
                    print(
                        f"{bold}ROOM ID{reset}: {room.get('room_id')} | "
                        f"{bold}BUILDING{reset}: {room.get('building')} | "
                        f"{bold}CAPACITY{reset}: {room.get('capacity')} | "
                        f"{bold}FROM{reset}: {room.get('available_from', 'N/A')} | "
                        f"{bold}UNTIL{reset}: {room.get('available_until', 'N/A')}"
                    )
                    found = True

                if not found:
                    print("No available rooms matched your search criteria.")
            else:
                print("Invalid option. Please choose a valid menu number.")

    #==================================================
    #Option 3: Track, update and search borrowed items
    #List of dictionaries saved to json
    #==================================================
    elif option == 3:
        try:
            borrowed_item_options = int(input(
                "Would you like to:\n"
                "1. Add a borrowed item\n"
                "2. Remove a borrowed item\n"
                "3. List borrowed items\n"
                "4. Search for borrowed items\n"
                "0. Back to main menu\n"
                ).strip())
        except ValueError:
            print("Invalid input. Please enter a number corresponding to the options.")
            continue

        if borrowed_item_options == 0:
            continue

        elif borrowed_item_options == 1:
            print("Please provide the following details:")
            new_item_id = input("Enter an Item ID: ").strip()
            new_item_name = input("Enter the name of this new item: ").strip()
            new_student_id = input("Enter the student ID of the borrower: ").strip()
            new_student_name = input("Enter the new borrower's name: ").strip()

            while True:
                try:
                    new_borrow_date = input("Enter the borrow date (YYYY-MM-DD): ").strip()
                    datetime.strptime(new_borrow_date, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
            while True:
                try:
                    new_due_date = input("Enter the due date (YYYY-MM-DD): ").strip()
                    datetime.strptime(new_due_date, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
            while True:
                new_status = input("Enter the status of this item (Borrowed/Returned): ").strip()
                if new_status in ["Borrowed", "Returned"]:
                    break
                else:
                    print("Invalid status. Please enter 'Borrowed' or 'Returned'.")

            new_item = {
                "item_id": new_item_id,
                "item_name": new_item_name,
                "student_id": new_student_id,
                "student_name": new_student_name,
                "borrow_date": new_borrow_date,
                "due_date": new_due_date,
                "status": new_status
            }

            if any(item["item_id"] == new_item_id for item in borrowed_items):
                print("An item with this Item ID already exists. Please use a unique Item ID.")
                continue
            borrowed_items.append(new_item)
            save_json("borrowed_items.json", borrowed_items)
            print("Borrowed item added successfully.")

        #==================================================
        # Remove:borrowed item:
        # Algotithm: linear search by item_id, remove if found, else notify not found.
        elif borrowed_item_options == 2:
            removal = input("Please enter the item ID of the borrowed item you wish to remove: ").strip()
            if removal == "":
                print("Invalid input. Please enter a valid Item ID.")
            else:
                removed = False
                for item in borrowed_items:
                    if item["item_id"] == removal:
                        borrowed_items.remove(item)
                        save_json("borrowed_items.json", borrowed_items)
                        print("Borrowed item removed successfully.")
                        removed = True
                        break
                if not removed:
                    print("No borrowed item found with that ID.")

                    
        elif borrowed_item_options == 3:
            print("List of Borrowed Items:")
            for item in borrowed_items:
                print(
                    f"- {bold}ITEM ID{reset}: {item['item_id']} | "
                    f"{bold}ITEM NAME{reset}: {item['item_name']} | "
                    f"{bold}BORROWER NAME{reset}: {item['student_name']} | "
                    f"{bold}BORROW DATE{reset}: {item['borrow_date']} | "
                    f"{bold}DUE DATE{reset}: {item['due_date']} | "
                    f"{bold}STATUS{reset}: {item['status']}\n"
                    )
        #==================================================
        # Search for borrowed items
        #Algorithm: linear search thorugh list to find matching item_id, item_name, student_id, student_name
        elif borrowed_item_options == 4:
            search = input("Enter Item ID, Student ID, or Student Name to search for: ").strip().lower()
            if not search:
                print("Search input cannot be blank.")
                continue

            found = False

            for item in borrowed_items:
                item_id = str(item.get("item_id", "")).lower()
                student_id = str(item.get("student_id", "")).lower()
                student_name = str(item.get("student_name", "")).lower()
                item_name = str(item.get("item_name", "")).lower()

                if (
                    search == item_id
                    or search == student_id
                    or search in student_name
                    or search in item_name
                ):
                    print(
                        f"- {bold}ITEM ID{reset}: {item['item_id']} | "
                        f"{bold}ITEM NAME{reset}: {item['item_name']} | "
                        f"{bold}BORROWER NAME{reset}: {item['student_name']} | "
                        f"{bold}STUDENT ID{reset}: {item['student_id']} | "
                        f"{bold}BORROW DATE{reset}: {item['borrow_date']} | "
                        f"{bold}DUE DATE{reset}: {item['due_date']} | "
                        f"{bold}STATUS{reset}: {item['status']}"
                    )
                    found = True
                    break

            if not found:
                print("No borrowed items match the filters provided.")

    elif option == 4:
        action = input("Enter B to backup or R to restore: ").strip().lower()
        if action == "b":
            backup_all_data()
        elif action == "r":
            restore_all_data()
        else:
            print("Invalid option.")
        

    else:
        print("Invalid option selected.")
        