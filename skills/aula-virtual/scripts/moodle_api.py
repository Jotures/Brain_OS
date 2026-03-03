#!/usr/bin/env python3
"""
Moodle API Client for UAndina
=============================
Provides functions to interact with Universidad Andina del Cusco's 
Moodle Web Services API.

Features:
- Get enrolled courses
- Get assignments and due dates
- Get grades
- Get course contents

Usage:
    from moodle_api import MoodleAPI
    
    api = MoodleAPI()
    courses = api.get_courses()
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Try to load from .env file
try:
    from dotenv import load_dotenv
    skill_dir = Path(__file__).parent.parent
    env_path = skill_dir / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass


class MoodleAPI:
    """
    Client for UAndina Moodle Web Services API.
    
    Requires MOODLE_TOKEN to be set in environment or passed directly.
    """
    
    def __init__(self, token: str = None, base_url: str = None):
        """
        Initialize the Moodle API client.
        
        Args:
            token: Moodle web service token (or from MOODLE_TOKEN env)
            base_url: Moodle base URL (or from MOODLE_URL env)
        """
        self.token = token or os.getenv('MOODLE_TOKEN')
        self.base_url = base_url or os.getenv('MOODLE_URL')
        if not self.base_url:
            from course_map import MOODLE_URL
            self.base_url = MOODLE_URL
        
        if not self.token:
            raise ValueError(
                "No Moodle token provided. "
                "Run get_uandina_token.py first or set MOODLE_TOKEN"
            )
        
        # Web service endpoint
        self.ws_url = f"{self.base_url}/webservice/rest/server.php"
        
        # Cache for user info
        self._user_id = None
    
    def _call(self, function: str, **params) -> Any:
        """
        Make a call to the Moodle Web Service API.
        
        Args:
            function: The Moodle WS function name
            **params: Additional parameters for the function
            
        Returns:
            Parsed JSON response
        """
        request_params = {
            'wstoken': self.token,
            'wsfunction': function,
            'moodlewsrestformat': 'json',
            **params
        }
        
        try:
            response = requests.post(
                self.ws_url,
                data=request_params,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Check for Moodle errors
            if isinstance(result, dict) and 'exception' in result:
                raise MoodleAPIError(
                    result.get('message', 'Unknown error'),
                    result.get('errorcode', 'unknown')
                )
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise MoodleAPIError(f"Request failed: {e}", "request_error")
    
    def get_site_info(self) -> Dict:
        """
        Get site information and current user details.
        
        Returns:
            Dict with site name, user info, etc.
        """
        return self._call('core_webservice_get_site_info')
    
    def get_user_id(self) -> int:
        """
        Get the current user's ID.
        
        Returns:
            User ID as integer
        """
        if self._user_id is None:
            info = self.get_site_info()
            self._user_id = info.get('userid')
        return self._user_id
    
    def get_courses(self) -> List[Dict]:
        """
        Get all courses the user is enrolled in.
        
        Returns:
            List of course dictionaries
        """
        user_id = self.get_user_id()
        return self._call('core_enrol_get_users_courses', userid=user_id)
    
    def get_course_contents(self, course_id: int) -> List[Dict]:
        """
        Get the contents/sections of a specific course.
        
        Args:
            course_id: The Moodle course ID
            
        Returns:
            List of sections with modules
        """
        return self._call('core_course_get_contents', courseid=course_id)
    
    def get_assignments(self, course_ids: List[int] = None) -> Dict:
        """
        Get assignments from courses.
        
        Args:
            course_ids: Optional list of course IDs to filter
            
        Returns:
            Dict with 'courses' containing assignments
        """
        params = {}
        if course_ids:
            for i, cid in enumerate(course_ids):
                params[f'courseids[{i}]'] = cid
        
        return self._call('mod_assign_get_assignments', **params)
    
    def get_grades(self, course_id: int) -> Dict:
        """
        Get grades for a specific course.
        
        Args:
            course_id: The Moodle course ID
            
        Returns:
            Dict with grade items and grades
        """
        user_id = self.get_user_id()
        return self._call(
            'gradereport_user_get_grade_items',
            courseid=course_id,
            userid=user_id
        )
    
    def get_calendar_events(
        self,
        time_start: int = None,
        time_end: int = None
    ) -> Dict:
        """
        Get calendar events (deadlines, etc).
        
        Args:
            time_start: Unix timestamp for start (default: now)
            time_end: Unix timestamp for end (default: 30 days from now)
            
        Returns:
            Dict with 'events' list
        """
        import time
        
        if time_start is None:
            time_start = int(time.time())
        if time_end is None:
            time_end = time_start + (30 * 24 * 60 * 60)  # 30 days
        
        return self._call(
            'core_calendar_get_calendar_events',
            events={'timestart': time_start, 'timeend': time_end}
        )
    
    def get_upcoming_events(self, days: int = 30) -> List[Dict]:
        """
        Get upcoming calendar events (quizzes, exams, module openings).
        
        Uses core_calendar_get_calendar_upcoming_view for a comprehensive
        view of all upcoming academic events, not just assignments.
        
        Args:
            days: Number of days ahead to look
            
        Returns:
            List of event dicts with name, course, type, timestart, etc.
        """
        import time
        
        try:
            result = self._call('core_calendar_get_calendar_upcoming_view')
            
            events = []
            now = int(time.time())
            future = now + (days * 24 * 60 * 60)
            
            for event in result.get('events', []):
                timestart = event.get('timestart', 0)
                
                # Solo eventos futuros dentro del rango
                if now < timestart <= future:
                    event_type = event.get('eventtype', 'unknown')
                    module_name = event.get('modulename', '')
                    
                    # Clasificar tipo de evento para Brain OS
                    if module_name == 'quiz' or 'quiz' in event.get('name', '').lower():
                        brain_os_type = '⚡ Examen'
                    elif module_name == 'assign':
                        brain_os_type = '📝 Tarea'
                    elif event_type in ('course', 'group'):
                        brain_os_type = '📅 Evento'
                    else:
                        brain_os_type = '📅 Evento'
                    
                    events.append({
                        'id': event.get('id'),
                        'name': event.get('name', 'Sin nombre'),
                        'course_name': event.get('course', {}).get('fullname', ''),
                        'course_id': event.get('courseid'),
                        'type': brain_os_type,
                        'event_type': event_type,
                        'module_name': module_name,
                        'timestart': timestart,
                        'timestart_formatted': datetime.fromtimestamp(timestart).strftime('%Y-%m-%d %H:%M'),
                        'days_remaining': (timestart - now) // (24 * 60 * 60),
                        'description': event.get('description', ''),
                        'url': event.get('url', ''),
                    })
            
            # Ordenar por fecha
            events.sort(key=lambda x: x['timestart'])
            return events
            
        except MoodleAPIError as e:
            print(f"⚠️ Error getting calendar events: {e}")
            return []
    
    def get_activity_completion(self, course_id: int) -> List[Dict]:
        """
        Get completion status for all activities in a course.
        
        Args:
            course_id: The Moodle course ID
            
        Returns:
            List of activity dicts with completion status
        """
        user_id = self.get_user_id()
        
        try:
            result = self._call(
                'core_completion_get_activities_completion_status',
                courseid=course_id,
                userid=user_id
            )
            
            activities = []
            for status in result.get('statuses', []):
                activities.append({
                    'cmid': status.get('cmid'),
                    'module_name': status.get('modname', ''),
                    'state': status.get('state', 0),  # 0=incomplete, 1=complete, 2=complete_pass, 3=complete_fail
                    'completed': status.get('state', 0) in (1, 2),
                    'tracking': status.get('tracking', 0),  # 0=none, 1=manual, 2=automatic
                    'has_completion': status.get('tracking', 0) > 0,
                })
            
            return activities
            
        except MoodleAPIError:
            return []
    
    def get_course_progress_summary(self, course_id: int) -> Dict:
        """
        Get a progress summary for a course combining completion + contents.
        
        Returns:
            Dict with total_activities, completed, pending, percentage
        """
        activities = self.get_activity_completion(course_id)
        
        # Solo contar actividades con tracking habilitado
        tracked = [a for a in activities if a['has_completion']]
        completed = [a for a in tracked if a['completed']]
        
        total = len(tracked)
        done = len(completed)
        percentage = round((done / total) * 100, 1) if total > 0 else 0.0
        
        # Enriquecer con nombres usando course_contents
        try:
            contents = self.get_course_contents(course_id)
            # Crear mapa cmid -> nombre
            name_map = {}
            for section in contents:
                for module in section.get('modules', []):
                    name_map[module.get('id')] = {
                        'name': module.get('name', 'Sin nombre'),
                        'modname': module.get('modname', ''),
                        'section': section.get('name', ''),
                    }
            
            # Enriquecer actividades
            for act in tracked:
                info = name_map.get(act['cmid'], {})
                act['name'] = info.get('name', f'Activity {act["cmid"]}')
                act['activity_type'] = info.get('modname', '')
                act['section'] = info.get('section', '')
        except MoodleAPIError:
            for act in tracked:
                act['name'] = f'Activity {act["cmid"]}'
                act['activity_type'] = act.get('module_name', '')
                act['section'] = ''
        
        return {
            'total': total,
            'completed': done,
            'pending': total - done,
            'percentage': percentage,
            'activities': tracked,
        }
    
    def get_upcoming_deadlines(self, days: int = 14) -> List[Dict]:
        """
        Get upcoming assignment deadlines.
        
        Args:
            days: Number of days ahead to check
            
        Returns:
            List of assignments with due dates, sorted by date
        """
        import time
        
        now = int(time.time())
        future = now + (days * 24 * 60 * 60)
        
        deadlines = []
        
        try:
            assignments_data = self.get_assignments()
            
            for course in assignments_data.get('courses', []):
                course_name = course.get('fullname', 'Unknown Course')
                
                for assignment in course.get('assignments', []):
                    due_date = assignment.get('duedate', 0)
                    
                    # Only include if due date is in the future and within range
                    if now < due_date <= future:
                        deadlines.append({
                            'name': assignment.get('name'),
                            'course': course_name,
                            'course_id': course.get('id'),
                            'assignment_id': assignment.get('id'),
                            'due_date': due_date,
                            'due_date_formatted': datetime.fromtimestamp(due_date).strftime('%Y-%m-%d %H:%M'),
                            'days_remaining': (due_date - now) // (24 * 60 * 60)
                        })
            
            # Sort by due date
            deadlines.sort(key=lambda x: x['due_date'])
            
        except MoodleAPIError as e:
            print(f"⚠️ Error getting assignments: {e}")
        
        return deadlines


class MoodleAPIError(Exception):
    """Exception for Moodle API errors."""
    
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(f"[{code}] {message}" if code else message)


def main():
    """Test the Moodle API."""
    print("🎓 UAndina Moodle API Test")
    print("=" * 50)
    
    try:
        api = MoodleAPI()
        
        # Get site info
        print("\n📌 Site Info:")
        info = api.get_site_info()
        print(f"   Site: {info.get('sitename')}")
        print(f"   User: {info.get('fullname')}")
        print(f"   Username: {info.get('username')}")
        
        # Get courses
        print("\n📚 Enrolled Courses:")
        courses = api.get_courses()
        for course in courses[:10]:  # Limit to 10
            print(f"   [{course.get('id')}] {course.get('fullname')}")
        
        # Get upcoming deadlines
        print("\n⏰ Upcoming Deadlines (14 days):")
        deadlines = api.get_upcoming_deadlines(14)
        if deadlines:
            for d in deadlines[:5]:  # Limit to 5
                print(f"   📅 {d['due_date_formatted']} ({d['days_remaining']}d)")
                print(f"      {d['name']}")
                print(f"      → {d['course']}")
        else:
            print("   No upcoming deadlines!")
        
        print("\n✅ API connection successful!")
        
    except MoodleAPIError as e:
        print(f"\n❌ Moodle API Error: {e}")
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("   Run get_uandina_token.py first!")


if __name__ == "__main__":
    main()
