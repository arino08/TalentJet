# TalentJet - Recruitment Management System

![TalentJet Logo](talentjet/static/images/logo.png)

## Project Overview

TalentJet is a comprehensive recruitment management system built with Django that streamlines the hiring process by connecting job seekers with employers. The platform offers intuitive interfaces for job posting, application tracking, and candidate evaluation, making recruitment efficient and effective for all parties involved.

## Technology Stack

- **Backend**: Django 4.2
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: PostgreSQL
- **Authentication**: Django Authentication System
- **File Storage**: Django FileField for resume storage
- **Responsive Design**: Bootstrap responsive grid system
- **Developer Tools**: Git, VS Code

## Key Features

### For Job Seekers
- User-friendly account creation and profile management
- Resume upload and management
- Job search with filtering options
- One-click job application process
- Application status tracking
- Interview scheduling and notifications

### For Employers
- Company profile management
- Job posting with detailed descriptions
- Applicant tracking system
- Candidate profile viewing with resume download
- Application approval/rejection workflow
- Interview scheduling and management

## Installation and Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git
- PostgreSQL

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/arino08/talentjet.git
   cd talentjet
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Create a `.env` file in the project root
   - Add the following variables:
     ```
     DEBUG=True
     SECRET_KEY=your_secret_key_here
     DATABASE_URL=postgresql://user:password@localhost/dbname
     ```

5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000/`
   - Admin interface is available at `http://127.0.0.1:8000/admin/`

## Project Structure

```
RecruitementManagement/
├── talentjet/                 # Main Django app
│   ├── migrations/            # Database migrations
│   ├── static/                # Static files (CSS, JS, images)
│   ├── templates/             # HTML templates
│   │   ├── applications/      # Application-related templates
│   │   ├── authentication/    # User auth templates
│   │   ├── jobs/              # Job listing templates
│   │   └── profiles/          # User profile templates
│   ├── admin.py               # Admin configuration
│   ├── forms.py               # Form definitions
│   ├── models.py              # Database models
│   ├── urls.py                # URL routing
│   └── views.py               # View functions
├── RecruitementManagement/    # Project settings
│   ├── settings.py            # Django settings
│   ├── urls.py                # Project URL routing
│   └── wsgi.py                # WSGI configuration
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Database Schema

### User Model
- Extended Django User model with roles (seeker, employer)
- Additional profile information (contact details, experience)

### Job Model
- Title, description, requirements
- Location, salary range
- Employment type (full-time, part-time, contract)
- Posted date, deadline

### Application Model
- ForeignKey to Job and User
- Application status (pending, accepted, rejected)
- Application date
- Additional notes

## Usage Guide

### For Job Seekers
1. Create an account and complete your profile
2. Upload your resume
3. Browse available jobs
4. Apply for positions with one click
5. Track application status in your dashboard

### For Employers
1. Create a company account
2. Set up your company profile
3. Post job openings with detailed descriptions
4. Review applications through the management interface
5. Accept or reject candidates
6. Schedule interviews with promising candidates

## API Documentation

TalentJet provides a RESTful API for integration with other systems:

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/jobs/` | GET | List all jobs | Not required |
| `/api/jobs/<id>/` | GET | Retrieve job details | Not required |
| `/api/applications/` | GET | List user applications | Required |
| `/api/applications/` | POST | Submit application | Required |

## Screenshots

![Dashboard](docs/screenshots/dashboard.png)
![Job Listings](docs/screenshots/job-listings.png)
![Application Management](docs/screenshots/application-management.png)
![User Profile](docs/screenshots/user-profile.png)

## Technical Highlights

### UI/UX Features
- Responsive design adapts to any device
- Intuitive navigation with breadcrumbs
- Form validation with clear error messages
- Modal dialogs for quick actions
- Animated transitions for enhanced user experience

### Performance Optimizations
- Database query optimization with select_related and prefetch_related
- Static file caching and compression
- Lazy loading of images
- Pagination for large datasets
- Background processing for email notifications

### Security Measures
- CSRF protection on all forms
- User input validation and sanitization
- Password policy enforcement
- Role-based access control
- Secure file upload handling

## Future Improvements

- **Recommendation Engine**: AI-based job recommendations for seekers
- **Advanced Search**: Improved search with filters and saved searches
- **Messaging System**: In-app messaging between employers and candidates
- **Analytics Dashboard**: Insights for employers about application trends
- **Mobile App**: Native mobile applications for iOS and Android
- **Integration**: API connections to popular job boards

## Contributing

We welcome contributions to TalentJet! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Project Link: [https://github.com/arino08/talentjet](https://github.com/arino08/talentjet)

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- All the contributors who have invested their time in this project
