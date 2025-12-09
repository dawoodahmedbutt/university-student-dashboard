# Data Management Module Structure

## Overview

The Data Management dashboard now uses a modular structure where each table (Students, Courses, Modules) has its own dedicated file with complete CRUD operations.

## File Structure

```
frontend_v2/
├── src/
│   ├── data/
│   │   └── dashboard_api.py          # API client with CRUD endpoints
│   └── pages/
│       ├── data_management.py         # Main page with dropdown selector
│       └── tables/                    # Table-specific CRUD modules
│           ├── __init__.py
│           ├── student_table.py       # Student CRUD operations
│           ├── course_table.py        # Course CRUD operations
│           └── module_table.py        # Module CRUD operations
```

## Architecture

### Main Entry Point: `data_management.py`

- Provides a dropdown selector to choose between Students, Courses, or Modules
- Delegates rendering to the appropriate table module
- Clean and minimal code (only ~35 lines)

### Table Modules

Each table module (`student_table.py`, `course_table.py`, `module_table.py`) contains:

1. **Main render function**: `render_[table]_table(table_placeholder)`

   - Loads data from API
   - Renders search bar
   - Displays filtered table
   - Calls CRUD functions

2. **Delete function**: `render_delete_[table]()`

   - Search by ID
   - Show preview
   - Confirmation checkbox
   - Delete operation with table refresh

3. **Update function**: `render_update_[table]()`

   - Load record by ID
   - Pre-fill form fields
   - Edit and submit
   - Clear form after success

4. **Create function**: `render_create_[table]()`

   - Empty form for new records
   - Validation
   - Create operation with table refresh

5. **Refresh helper**: `refresh_[table]_table()`
   - Reloads data from API
   - Applies search filter
   - Updates table display

## API Endpoints

### Students

- `GET /students/getall` - List all students
- `POST /CRUD/student/create` - Create student
- `PUT /CRUD/student/update/{id}` - Update student
- `DELETE /CRUD/student/delete/{student_id}` - Delete student

### Courses

- `GET /CRUD/course/getall` - List all courses
- `POST /CRUD/course/create` - Create course
- `PUT /CRUD/course/update/{id}` - Update course
- `DELETE /CRUD/course/delete/{id}` - Delete course

### Modules

- `GET /CRUD/module/getall` - List all modules
- `POST /CRUD/module/create` - Create module
- `PUT /CRUD/module/update/{id}` - Update module
- `DELETE /CRUD/module/delete/{id}` - Delete module

## Features

### Common Features Across All Tables

- **Search Filtering**: Case-insensitive search across all relevant columns
- **ID-based Operations**: Find records by ID for update/delete
- **Validation**: Required fields marked with asterisk (\*)
- **Confirmation**: Delete operations require checkbox confirmation
- **Auto-refresh**: Tables refresh after successful CRUD operations
- **Cache Management**: Clears Streamlit cache after mutations
- **Error Handling**: User-friendly error messages

### Table-Specific Features

#### Students

- Fields: first_name, last_name, email, address, year_of_study, course_id
- Course dropdown for foreign key selection
- Year validation (1-4)
- Search by name, email, or ID

#### Courses

- Fields: name
- Simple single-field management
- Search by name or ID

#### Modules

- Fields: name, course_id
- Course dropdown for foreign key selection
- Search by name or ID

## How to Add a New Table

1. **Create API endpoints** in `dashboard_api.py`:

   ```python
   ENDPOINTS = {
       ...
       "list_[table]": "/CRUD/[table]/getall",
       "create_[table]": "/CRUD/[table]/create",
       "update_[table]": "/CRUD/[table]/update/{id}",
       "delete_[table]": "/CRUD/[table]/delete/{id}",
   }

   @st.cache_data(ttl=30)
   def list_[table]s() -> pd.DataFrame:
       ...

   def create_[table](data: Dict) -> Dict:
       ...

   def update_[table](id: int, updates: Dict) -> Dict:
       ...

   def delete_[table](id: int) -> bool:
       ...
   ```

2. **Create table module** in `pages/tables/[table]_table.py`:

   - Copy structure from existing table file
   - Adjust field names and validation
   - Update column display preferences

3. **Update data_management.py**:

   ```python
   from pages.tables import ..., [table]_table

   table_options = {
       ...
       "[Table Name]": "[table]"
   }

   if table_type == "[table]":
       [table]_table.render_[table]_table(table_placeholder)
   ```

## Benefits of This Structure

1. **Modularity**: Each table is self-contained and independent
2. **Maintainability**: Easy to modify one table without affecting others
3. **Scalability**: Simple to add new tables
4. **Code Reuse**: Common patterns across all tables
5. **Clarity**: Clean separation of concerns
6. **Testing**: Each module can be tested independently

## Session State Management

Each table uses namespaced session state keys to avoid conflicts:

- Students: `update_first`, `update_last`, `update_email`, etc.
- Courses: `update_course_name_field`
- Modules: `update_module_name_field`, `update_module_course_id`

## Future Enhancements

Potential improvements:

- Generic base class for common CRUD operations
- Dynamic field generation from backend schema
- Bulk operations (multi-delete, import/export)
- Advanced filtering and sorting
- Pagination for large datasets
- Audit logging for changes
