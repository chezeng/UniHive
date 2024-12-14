import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-welcome',
  templateUrl: './welcome.component.html',
  styleUrls: ['./welcome.component.css']
})
export class WelcomeComponent {
  constructor(private router: Router) {}

  onPreview() {
    this.router.navigate(['/forum']); // Replace with your actual forum route
  }

  onRegister() {
    this.router.navigate(['/register']); // Replace with your registration route
  }
}
