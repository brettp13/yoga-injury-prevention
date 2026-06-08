import { Component, OnInit } from '@angular/core';

import { UserService } from '../../shared/user.service';
import { UserProfileService } from '../../shared/user.profile.service';

@Component({
  selector: 'app-dashboard-home',
  templateUrl: './dashboard-home.component.html',
  styleUrls: ['./dashboard-home.component.css']
})
export class DashboardHomeComponent implements OnInit {
  token: string;
  userProfile: any;

  constructor(private userService: UserService, 
              private userProfileService: UserProfileService) { }

  ngOnInit() {
    this.userService.token.subscribe(token => {
      this.token = token;
    });
    
    this.userProfileService.userProfile.subscribe(
      (userProfile) => {
        this.userProfile = userProfile;
      });

    this.userProfileService.getUserProfile(this.token);
  }

}
