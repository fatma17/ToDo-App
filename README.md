# To-Do App (Odoo Custom Module)
## Overview
This is a **custom Odoo module** for managing To-Do tasks. The module demonstrates essential development concepts in Odoo, including model creation, inheritance, workflow management, security rules, and more.

## Technical Concepts  
The project implements the following Odoo development features:

- **Tree and Form Views:** Customized user-friendly views for managing tasks.

- **Search view:** Enhanced search with filters and groupings. Filter tasks by `status` and group by `status`, `Due Date`.

- **Workflows:** Manage task status transitions `New → In Progress → Completed → Closed`.
   
- **Chatter Integration:** Track task history and add comments.

- **Task Lines:** Support for subtasks (One2many relationship).  

- **Automated Actions:** for triggering specific behaviors, such as `Mark tasks if the due date is passed`.

- **Report Actions:** Generate PDF reports for tasks.

- **Sequence Management:** Automatically generate unique identifiers for tasks.

- **Wizard:** Provides a guided interface for actions, such as `assigning multiple tasks to a specific user`.

- **Record Rules and Security:** Implemented role-based access control.
     >- **Managers**: Full access to create, edit, and delete tasks.
     >- **Users**: Restricted to view only their assigned tasks.

