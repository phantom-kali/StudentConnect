# StudentConnect

StudentConnect is a comprehensive web application designed to enhance campus life by providing students with a platform to connect, share, and collaborate. The site offers a wide range of features, from social interactions like confessions, groups, and stories, to practical functionalities such as dining options, job listings, and marketplace services.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Accounts**: User authentication, profile management, and following system.
- **Confessions**: Anonymously post confessions and interact with others.
- **Dining**: View and review dining options on campus.
- **Events**: Stay updated on campus events and manage RSVPs.
- **Feed**: Social feed featuring posts from followed users and trending content.
- **Groups**: Join or create groups for different interests and activities.
- **Jobs**: Browse and apply for campus job listings.
- **Marketplace**: Buy and sell items within the campus community.
- **Messaging**: Direct messaging between users.
- **Notifications**: Real-time notifications for activities and updates.
- **Search**: Powerful search functionality across the site.
- **Stories**: Share short, time-limited stories with followers.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/phantom-kali/StudentConnect.git
   cd StudentConnect
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```bash
   python manage.py migrate
   ```

## Configuration

1. **Environment Variables:**
   Create a `.env` file in the root directory to configure your environment variables. Include the following:

   ```bash
   DEBUG=True
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///db.sqlite3
   ```

2. **Static Files:**
   Collect static files with the command:
   ```bash
   python manage.py collectstatic
   ```

## Running the Project

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the site:**
   Open your web browser and navigate to `http://localhost:8000`.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.