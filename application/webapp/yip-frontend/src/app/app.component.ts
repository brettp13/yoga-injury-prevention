import { Component, OnInit } from '@angular/core';

import { UserService } from '../app/shared/user.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  trafficSource: string = '';

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.userService.checkIfLoggedIn();

    // Set the traffic source in the session
    this.trafficSource = window['trafficSource'];
    localStorage.setItem('trafficSource', this.trafficSource);
  }
}
