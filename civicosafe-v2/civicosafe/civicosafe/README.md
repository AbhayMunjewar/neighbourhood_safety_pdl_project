# Neighborhood Watch - HTML/CSS/JS Files

This folder contains standalone HTML files for the Neighborhood Watch and Safety Management application. Each file is a complete, self-contained page with inline CSS and JavaScript.

## Files Included

### ✅ Complete Files (Ready to Use)
1. **login.html** - Login and Signup page with tabs
2. **dashboard.html** - Main dashboard with stats and recent activity
3. **incidents.html** - Comprehensive incident reporting form
4. **alerts.html** - Community alerts with filtering tabs
5. **members.html** - Searchable neighborhood members directory
6. **emergency.html** - Emergency contacts with SOS button

### 📝 Template Files (Basic Structure Included)
7. **admin.html** - Admin control panel (template structure provided)
8. **about.html** - About and contact page (template structure provided)

**Note:** admin.html and about.html contain placeholder content. Follow the README instructions below to complete them using the same structure as the other pages.

## Features

- ✨ **Dark Mode**: All pages include a working dark mode toggle that persists across sessions
- 📱 **Responsive Design**: Mobile-friendly layouts that work on all devices
- 🎨 **Consistent Styling**: All pages use the same design system and color scheme
- 🔗 **Navigation**: Header navigation works across all pages
- 📄 **Footer**: Consistent footer on all pages (except login)
- 🚀 **No Dependencies**: Pure HTML, CSS, and JavaScript - no external libraries required

## How to Use

1. **Open any HTML file** in a web browser
2. **Navigate between pages** using the header navigation links
3. **Toggle dark mode** using the moon/sun icon in the header
4. **Fill out forms** and interact with the interface

## Page Structure

Each page follows this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title - Neighborhood Watch</title>
    <style>
        /* Inline CSS */
    </style>
</head>
<body>
    <!-- Header with navigation -->
    <header>...</header>
    
    <!-- Main content -->
    <main>...</main>
    
    <!-- Footer -->
    <footer>...</footer>
    
    <script>
        /* Inline JavaScript */
    </script>
</body>
</html>
```

## Color Scheme

### Light Mode
- Background: `#ffffff`
- Foreground: `#252525`
- Primary: `#030213`
- Muted: `#ececf0`
- Border: `rgba(0, 0, 0, 0.1)`

### Dark Mode
- Background: `#252525`
- Foreground: `#fafafa`
- Primary: `#fafafa`
- Muted: `#454545`
- Border: `#454545`

## Creating Additional Pages

To create the remaining pages (alerts, members, emergency, admin, about), use this template:

### Basic Template Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Page - Neighborhood Watch</title>
    <style>
        /* Copy the CSS from dashboard.html or incidents.html */
        /* Add any page-specific styles */
    </style>
</head>
<body>
    <!-- Header (copy from dashboard.html) -->
    <header>
        <div class="header-container">
            <a href="dashboard.html" class="logo">
                <!-- Logo SVG -->
                <span>Neighborhood Watch</span>
            </a>
            <nav>
                <a href="dashboard.html">Dashboard</a>
                <a href="incidents.html">Incidents</a>
                <a href="alerts.html" class="active">Alerts</a>
                <!-- ... other links -->
            </nav>
            <button class="theme-toggle" onclick="toggleTheme()">
                <!-- Theme toggle icons -->
            </button>
        </div>
    </header>

    <!-- Main content -->
    <main>
        <div class="container">
            <h1>Page Title</h1>
            <p class="subtitle">Page description</p>
            
            <!-- Your page content here -->
        </div>
    </main>

    <!-- Footer (copy from dashboard.html) -->
    <footer>
        <!-- Footer content -->
    </footer>

    <script>
        // Theme toggle function (copy from dashboard.html)
        function toggleTheme() {
            const html = document.documentElement;
            const lightIcon = document.querySelector('.theme-icon-light');
            const darkIcon = document.querySelector('.theme-icon-dark');
            
            if (html.classList.contains('dark')) {
                html.classList.remove('dark');
                localStorage.setItem('theme', 'light');
                lightIcon.style.display = 'block';
                darkIcon.style.display = 'none';
            } else {
                html.classList.add('dark');
                localStorage.setItem('theme', 'dark');
                lightIcon.style.display = 'none';
                darkIcon.style.display = 'block';
            }
        }

        // Check for saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.documentElement.classList.add('dark');
            document.querySelector('.theme-icon-light').style.display = 'none';
            document.querySelector('.theme-icon-dark').style.display = 'block';
        }
    </script>
</body>
</html>
```

## Page-Specific Content Ideas

### alerts.html
- Tabbed interface for filtering alerts (All, Emergency, Safety, Traffic, Community)
- Alert cards with priority badges (High, Medium, Low)
- Statistics sidebar
- "Create Alert" button

### members.html
- Search bar for filtering members
- Member cards with name, role, contact info
- Stats cards (Total Members, Admins, Block Captains, Verified)
- "Invite Member" button

### emergency.html
- Emergency services cards (911 Police, Fire, Medical)
- Local services contact list
- Utility companies section
- Block captains contact information
- SOS activation button (prominent, red)

### admin.html
- Tabbed interface (Overview, Users, Incidents, Alerts, Settings)
- Quick stats dashboard
- Pending approvals section
- Recent activity log
- System status indicators
- Settings toggles

### about.html
- Mission and Vision cards
- Core values section
- Team member profiles
- Statistics (members, years active, incidents resolved)
- Contact form
- Office hours information

## Customization Tips

1. **Colors**: Modify the CSS custom properties in `:root` and `.dark` to change the color scheme
2. **Typography**: Change font-family in the `body` selector
3. **Spacing**: Adjust padding and margins to your preference
4. **Icons**: Replace SVG paths with your own icons
5. **Content**: Update text, stats, and data as needed

## Browser Compatibility

These files work in all modern browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Notes

- The login page redirects to dashboard.html on form submit
- All form submissions show an alert (in production, connect to a backend)
- Dark mode preference is saved in localStorage
- Navigation highlights the current page

## License

© 2025 Neighborhood Watch. All rights reserved.
