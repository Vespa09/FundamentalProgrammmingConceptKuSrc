🍽️ PyRestaurant

Restaurant Reservation & Ordering Management System

A desktop-based restaurant management application built with Python, CustomTkinter, and SQLite. PyRestaurant streamlines table reservations, food ordering, shopping cart management, and bill settlement through an intuitive graphical user interface.

""Python" (https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)" (https://www.python.org/)
""CustomTkinter" (https://img.shields.io/badge/GUI-CustomTkinter-2B579A?style=for-the-badge)" (https://github.com/TomSchimansky/CustomTkinter)
""SQLite" (https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)" (https://www.sqlite.org/)
""License" (https://img.shields.io/badge/License-Not%20Specified-lightgrey?style=for-the-badge)" (#-license)

Project Type: Desktop Application
Academic Course: Fundamental Programming Concept
Institution: Kasetsart University, Sriracha Campus

---

📑 Table of Contents

- "Overview" (#-overview)
- "Key Features" (#-key-features)
- "Technology Stack" (#-technology-stack)
- "System Workflow" (#-system-workflow)
- "Project Structure" (#-project-structure)
- "Database Schema" (#-database-schema)
- "Getting Started" (#-getting-started)
- "Application Usage" (#-application-usage)
- "Validation and Business Rules" (#-validation-and-business-rules)
- "Team Members" (#-team-members)
- "Limitations and Future Improvements" (#-limitations-and-future-improvements)
- "License" (#-license)

---

📌 Overview

PyRestaurant is a Python desktop application designed to manage essential restaurant operations in a single system. It connects customer authentication, table reservations, food and beverage ordering, and payment-status tracking through a SQLite database.

The project demonstrates fundamental programming concepts and practical application development, including graphical user interface design, database operations, input validation, and business logic separation.

Project Objectives

- Simplify the table reservation process.
- Allow customers to browse menus and manage food orders.
- Calculate order totals and organize outstanding bills.
- Maintain application data using a relational database.
- Demonstrate modular Python programming and database integration.

✨ Key Features

🔐 1. User Authentication

- User registration and login using username and password.
- Input validation for passwords, phone numbers, and email addresses.
- Duplicate checking for usernames, phone numbers, and email addresses.
- Password-field interaction restrictions for copy, cut, and right-click actions.

«Security note: Restricting clipboard actions is a user-interface measure, not a substitute for secure password storage or authentication controls.»

📅 2. Table Reservation Management

- Browse available tables by reservation date and time slot.
- Filter table availability before creating a reservation.
- Automatically calculate the reservation end time, one hour after the start time.
- Validate reservation times and reject past reservations.
- Check existing reservations to help prevent scheduling conflicts.

🍕 3. Menu and Order Management

- Load food and beverage menus from the SQLite database.
- Display menu items with prices and descriptions.
- Increase or decrease item quantities.
- Select a table associated with the customer's reservation.
- Review selected items in a shopping cart.
- Calculate order totals dynamically.

💳 4. Billing and Payment Tracking

- Retrieve unpaid orders from the database.
- Group order items for billing summaries.
- Calculate item subtotals and the total amount due.
- Select a payment method: cash, bank transfer, or credit card.
- Update payment status after confirmation.
- Reset the billing interface after completing the payment workflow.

«Payment scope: The documented payment methods represent application-level selections. Real payment processing, payment gateway integration, and transaction verification are not established by the current project description.»

---

🛠️ Technology Stack

Technology| Purpose
Python 3.10+| Application logic and event handling
CustomTkinter| Desktop graphical user interface
SQLite3| Relational data storage
"tkcalendar"| Date selection for reservation workflows
Git & GitHub| Source code management and collaboration
Mermaid| System workflow documentation

Application Architecture

The application separates its responsibilities into GUI, business logic, authentication logic, and database access modules.

┌───────────────────────────────────┐
│       Presentation Layer           │
│          CustomTkinter             │
│              gui.py                │
└────────────────┬──────────────────┘
                 │
       ┌─────────┴─────────┐
       ▼                   ▼
┌──────────────┐   ┌────────────────┐
│ Authentication│   │ Order & Cart   │
│   logic.py    │   │   order.py     │
└───────┬──────┘   └────────┬───────┘
        │                   │
        └─────────┬─────────┘
                  ▼
       ┌─────────────────────┐
       │   Data Access Layer │
       │       data.py       │
       └──────────┬──────────┘
                  ▼
       ┌─────────────────────┐
       │   SQLite Database   │
       │     database.db     │
       └─────────────────────┘

This diagram represents the intended module responsibilities; exact call relationships should be verified against the implementation.

---

🔄 System Workflow

The following flowchart illustrates the main customer journey, from authentication to reservations, ordering, and billing.

flowchart TD
    A([Start Application]) --> B{Authenticated?}

    B -- No --> C[Register or Log In]
    C --> B

    B -- Yes --> D[Main Menu]

    D --> E[Table Reservation]
    E --> F[Select Date and Time]
    F --> G{Table Available?}
    G -- No --> E
    G -- Yes --> H[Confirm Reservation]
    H --> D

    D --> I[Order Food]
    I --> J[Select Reserved Table]
    J --> K[Browse Menu and Set Quantities]
    K --> L[Review Shopping Cart]
    L --> M{Confirm Order?}
    M -- No --> K
    M -- Yes --> N[(Save Unpaid Orders)]
    N --> D

    D --> O[Check Bill]
    O --> P[Retrieve Unpaid Orders]
    P --> Q[Review Bill and Total]
    Q --> R[Select Payment Method]
    R --> S[Confirm Payment]
    S --> T[(Update Payment Status)]
    T --> D

    D --> U[Log Out]
    U --> V([End Session])

Core Business Flow

1. Authenticate — register a new account or log in.
2. Reserve — select an available table and reservation time.
3. Order — choose a reserved table, browse the menu, and add items to the cart.
4. Review — verify quantities and the total order amount.
5. Settle — review outstanding orders, select a payment method, and confirm the payment workflow.

---

📂 Project Structure

FundamentalProgrammmingConceptKuSrc/
│
├── database/
│   └── database.db       # SQLite database
│
├── main/
│   ├── gui.py            # GUI layout and event handling
│   ├── data.py           # Database access and CRUD operations
│   ├── order.py          # Order and shopping cart logic
│   └── logic.py          # User authentication logic
│
└── README.md             # Project documentation

Module Responsibilities

File| Responsibility
"gui.py"| Creates application screens and handles user interactions
"data.py"| Manages database operations
"order.py"| Handles order processing and cart operations
"logic.py"| Implements authentication-related logic
"database.db"| Stores application records in SQLite

---

🗄️ Database Schema

The application uses SQLite to store user accounts, restaurant tables, reservations, menu items, and orders.

Table| Description| Representative Fields
"User"| User account information| "username", "password", "firstname", "lastname", "phone", "email", "role"
"dining_tables"| Restaurant table information| "table_no", "capacity", "cost"
"reservations"| Table reservation records| "id", "table_no", "customer", "booking_date", "time_slot", "status"
"menu_food"| Food menu items| "id", "food", "price", "description"
"menu_drink"| Beverage menu items| "id", "drink", "price", "description"
"orders"| Customer order records| "no_order", "menu", "quantity", "totalprice", "status", "table_no", "customer", "day", "time", "status_pay"

Data Relationships

Conceptually, the data follows these relationships:

- A customer can have multiple reservations.
- A reservation refers to a restaurant table.
- A customer can place multiple orders.
- Orders contain menu information, quantities, prices, and payment status.

The exact primary keys, foreign keys, indexes, and cardinalities should be confirmed against the database definition.

Payment Status

Status| Meaning
"ยังไม่จ่าย"| Payment is outstanding
"จ่ายแล้ว"| Payment is marked as completed

---

🚀 Getting Started

Follow the steps below to set up and run PyRestaurant locally.

Prerequisites

- Python 3.10 or later
- Git
- A supported desktop environment with Tkinter available

SQLite3 is included with most standard Python installations. No separate database server is required.

1. Clone the Repository

git clone https://github.com/vespa/FundamentalProgrammmingConceptKuSrc.git
cd FundamentalProgrammmingConceptKuSrc

2. Create a Virtual Environment

Windows

python -m venv .venv
.venv\Scripts\activate

macOS / Linux

python3 -m venv .venv
source .venv/bin/activate

3. Install Dependencies

python -m pip install --upgrade pip
python -m pip install customtkinter tkcalendar

4. Verify the Database

Confirm that the SQLite database exists at:

database/database.db

If the project requires initial database setup, follow the initialization instructions provided by the source code. Do not replace an existing database containing important records.

5. Launch the Application

Run the following command from the project root:

python main/gui.py

The application should open its desktop interface if the dependencies, database, and runtime environment are configured correctly.

---

🖥️ Application Usage

Typical User Journey

Step| Action| Expected Result
1| Register or log in| Access the main menu
2| Open table booking| Browse available reservation slots
3| Confirm a reservation| Save the reservation record
4| Open food ordering| Browse the menu and choose quantities
5| Confirm the cart| Submit the selected order
6| Open check bill| Review outstanding orders and the total
7| Select a payment method| Choose the intended payment channel
8| Confirm payment| Update the recorded payment status

The expected results describe the documented application workflow, not independently verified runtime test results.

---

✅ Validation and Business Rules

The documented application includes the following validation rules.

Area| Rule
Registration| Password must contain at least six characters
Registration| Validate phone number and email formats
Registration| Prevent duplicate usernames, phone numbers, and email addresses
Reservations| Reject past reservation times
Reservations| Validate reservation start and end times
Reservations| Check for conflicting reservations
Ordering| Support quantity adjustments and total calculation
Billing| Retrieve orders that have not been marked as paid
Payment| Update payment status following confirmation

Important Implementation Considerations

For a more reliable production system, consider strengthening these rules with:

- Password hashing using a suitable password-hashing algorithm.
- Parameterized SQL queries for database operations.
- Database transactions for reservation creation and payment-status updates.
- Database constraints to protect data integrity.
- Server-side or database-level conflict checks when multiple users may book simultaneously.
- Automated tests for validation, reservations, order totals, and payment-state transitions.

---

👥 Team Members

This project was developed as part of the Fundamental Programming Concept course at Kasetsart University, Sriracha Campus.

Name| Student ID
นาย ธนากร ขนทอง| "6930200760"
นาย แทนโชค สังข์วัย| "6930200689"
นางสาว กฤษยารัตน์ กลิ่นพิพัฒน์| "6930200018"

---

🔭 Limitations and Future Improvements

Potential next steps for the project include:

- [ ] Secure password storage and improved authentication controls.
- [ ] Automated unit and integration tests.
- [ ] A normalized database schema with explicit foreign keys.
- [ ] A reservation conflict-prevention mechanism backed by database transactions.
- [ ] Order history and reservation management screens.
- [ ] Receipt generation and printable invoices.
- [ ] Actual payment gateway integration and transaction verification.
- [ ] Application logging and structured error handling.
- [ ] Dependency management through a "requirements.txt" file.
- [ ] Packaging for convenient installation on desktop systems.

These items are proposed improvements and should not be interpreted as features that are already implemented.

---

📄 License

No license has been specified in the provided project information.

If you intend to distribute the project publicly, consider selecting an appropriate open-source license and adding a "LICENSE" file. Until then, do not assume that others have permission to reuse, modify, or redistribute the source code.

---

<p align="center">
  <strong>PyRestaurant</strong><br>
  Restaurant Operations, Simplified.
</p><p align="center">
  Built with Python · CustomTkinter · SQLite
</p>