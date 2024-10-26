import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  categories = [
    { name: 'General', description: 'General topics and announcements' },
    { name: 'Courses', description: 'Discussions about courses and programs' },
    { name: 'Events', description: 'Campus events and meetups' }
  ];

  threads = [
    { id: 1, title: 'What are the best electives?', snippet: 'Looking for suggestions on fun electives...' },
    { id: 2, title: 'CS vs SE: Which program is better?', snippet: 'I’m trying to decide between these two...' }
  ];

  constructor() {}

  ngOnInit() {}

  viewThread(threadId: number) {
    // Navigate to the discussion thread page
    console.log(`Navigating to thread with ID: ${threadId}`);
  }
}
