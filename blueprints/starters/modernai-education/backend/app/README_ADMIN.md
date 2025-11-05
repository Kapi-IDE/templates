# Modern AI Pro Admin Interface

This document provides information on using the admin interface for the Modern AI Pro platform.

## Access

The admin interface is available at `/admin` after starting the backend server. For example, if your server is running at `http://localhost:8000`, the admin interface will be at `http://localhost:8000/admin`.

## Authentication

The admin interface is now integrated with your User model and requires a user with the `admin` role. You must create an admin user before you can access the admin interface.

### Creating an Admin User

To create an admin user, run the script in the scripts directory:

```bash
cd backend
python scripts/create_admin_user.py --username admin --email admin@example.com --password your_secure_password
```

This will create a new user with admin role or update an existing user to have admin privileges.

### Authentication Security

**Important:** For production, you should set the following environment variables:
- `SECRET_KEY`: A secure secret key for session management and JWT token generation

The admin authentication is tied to your application's user model, ensuring that only users with the `admin` role can access the interface.

## Available Models

The admin interface provides access to all core models in the Modern AI Pro platform:

### User Management
- Users
- Payment History
- Referrals
- ELO History

### Learning Management
- Lesson Categories
- Lessons
- Lesson Content
- User Lessons
- User Lesson Issues
- Learning Pods
- Learning Pod Members

### Assessment
- Quiz Questions
- Quiz Sessions
- User Answers
- Surveys

### Programming
- Programming Challenges
- Programming Sessions

### Onboarding
- Onboarding States
- User Onboarding States

## Features

For each model, you can:
- View all records in a tabular format
- Create new records
- Edit existing records
- Delete records
- Filter and search records

## Usage Tips

1. Use the admin interface to seed initial content like lesson categories, lessons, and quiz questions.
2. Monitor user progress and engagement through the User Lessons and Quiz Sessions tables.
3. Manage Learning Pods and their members for group-based learning activities.
4. Track ELO ratings to see competitive progress among users.

## Security Notes

- The admin interface should only be accessible by authorized personnel.
- Consider placing the admin interface behind a separate authentication proxy for production environments.
- Regularly review access logs for unauthorized access attempts.
- Make sure to set secure environment variables as mentioned in the Authentication section.