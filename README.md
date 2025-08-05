# MAJOR GAMES REPORTING TEMPLATES

## OVERVIEW
A web-based template generator for sports reporting during major games competitions. This tool allows users to quickly generate standardized reporting templates by selecting sport, gender, event name, and event type from dropdown menus, then filling in dynamic variables to produce professional sports reports.

## FEATURES
- Dynamic dropdown menus that filter based on Excel data
- Auto-population of next event information from competition schedules
- Real-time template preview as you type
- Support for 196+ different sports templates
- Automatic variable field generation based on template requirements
- Copy-to-clipboard functionality for generated templates
- Responsive web interface that works on any device

## HOW IT WORKS
1. Select your sport from the dropdown menu
2. Choose gender category
3. Pick the specific event name
4. Select the event type (Heat, Final, Group Stage, etc.)
5. The system automatically generates input fields for required variables
6. Fill in the template variables (some fields auto-populate from schedule data)
7. Preview your template in real-time
8. Generate and copy the final template

<!-- ## TECHNICAL DETAILS
- Built with HTML, CSS, and JavaScript
- Uses GitHub Actions for automatic Excel-to-JSON conversion
- Hosted on GitHub Pages for free deployment
- Excel data automatically syncs when templates are updated

## FILE STRUCTURE
index.html - Main application interface
styles.css - Styling and layout
script.js - Application logic and functionality
sports_templates.xlsx - Source Excel file with all templates
data/templates.json - Auto-generated JSON data (do not edit manually)
scripts/excel_to_json.py - Conversion script for GitHub Actions
.github/workflows/update-templates.yml - Automated deployment workflow

## SETUP INSTRUCTIONS
1. Clone this repository to your local machine
2. Open index.html in any modern web browser
3. The application will automatically load template data
4. Start generating templates immediately

## UPDATING TEMPLATES
To add or modify templates:
1. Edit the sports_templates.xlsx file
2. Commit and push changes to GitHub
3. GitHub Actions will automatically convert Excel to JSON
4. Website updates automatically with new templates
5. No manual intervention required

## TEMPLATE FORMAT
Each template contains:
- Sport name
- Gender category  
- Event name
- Event type
- Template text with variable placeholders in curly brackets {VARIABLE_NAME}
- List of required fields for that template

## SUPPORTED SPORTS
Swimming, Football, Basketball, Badminton, Tennis, Sepak Takraw, Gymnastics, Athletics, and many more. The system supports any sport defined in the Excel template file.

## AUTO-POPULATION FEATURES
The system can automatically fill in:
- Next opponent information
- Match dates and times
- Venue details
- Competition stages
- Time zones
- Based on competition schedule data

## BROWSER COMPATIBILITY
Works on all modern browsers including:
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## CONTRIBUTING
1. Fork the repository
2. Make your changes to the Excel file or code
3. Test your changes locally
4. Submit a pull request with description of changes
5. Changes will be reviewed and merged if approved

## TROUBLESHOOTING
If templates don't load:
- Check browser console for errors
- Ensure you have internet connection for loading JSON data
- Try refreshing the page
- Check that templates.json file exists in data folder

If auto-population doesn't work:
- Verify schedule data is properly formatted
- Check that sport names match between templates and schedule
- Ensure dates are in correct format (YYYY-MM-DD)

## CONTACT
For questions or issues, please create an issue on the GitHub repository or contact the project maintainer.

## VERSION HISTORY
v1.0 - Initial release with basic template generation
v1.1 - Added auto-population features
v1.2 - Improved user interface and real-time preview
v1.3 - Added GitHub Actions for automatic updates

## LICENSE
This project is open source. Please check the LICENSE file for specific terms and conditions. -->
