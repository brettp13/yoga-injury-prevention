import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';

import { UserService } from '../../../shared/user.service';
import { UserProfileService } from '../../../shared/user.profile.service';
import { YogaPoseService } from '../../../shared/yogapose.service';

@Component({
  selector: 'app-account-details',
  templateUrl: './account-details.component.html',
  styleUrls: ['./account-details.component.css']
})
export class AccountDetailsComponent implements OnInit {
  accountDetailsForm: FormGroup;
  token: string;
  userAuthInfo: any;
  userProfile: any;
  showAlert: boolean = false;
  yogaStyles: any;
  defaultOption: any;

  constructor(private userService: UserService, 
              private userProfileService: UserProfileService,
              private yogaPoseService: YogaPoseService) { }

  ngOnInit() {
    this.accountDetailsForm = new FormGroup({
      'firstName': new FormControl(null),
      'lastName': new FormControl(null),
      'email': new FormControl(null, [Validators.email]),
      'yoga-style': new FormControl(null)
    });

    this.userService.token.subscribe(
      (token) => {
        this.token = token;
      });

    this.userService.userAuthInfo.subscribe(
      (authInfo) => {
        this.userAuthInfo = authInfo;
      });

    this.userProfileService.userProfile.subscribe(
      (profile) => {
        this.userProfile = profile;
      });

    this.yogaPoseService.yogaStyles.subscribe(
      (yogaStyles) => {
        this.yogaStyles = yogaStyles;
      });

    this.yogaPoseService.getYogaStyles();
    this.userService.getAuthInfo(this.token);
    this.userProfileService.getUserProfile(this.token);
    this.defaultOption = this.userProfile.yoga_style;
  }

  // shortcut functions for my-account form
  get firstName() { return this.accountDetailsForm.get('firstName') };
  get lastName() { return this.accountDetailsForm.get('lastName') };
  get email() { return this.accountDetailsForm.get('email') };
  get yogaStyle() { return this.accountDetailsForm.get('yoga-style') }

  // Update user account info
  onSubmit() {
    let newFirstName = this.firstName.value;
    let newLastName = this.lastName.value;
    let newEmail = this.email.value;
    let newYogaStyle = this.yogaStyle.value;
    
    if (!newEmail) {
      console.log('No update for email');
    } else {
      this.userService.updateAuthInfo(this.token, [{'email': newEmail}]);
    }
    
    if (!newFirstName) {
      console.log('No update for first name');
    } else {
      this.userProfileService.updateUserProfile(this.token, [{'first_name': newFirstName}]);
    }

    if (!newLastName) {
      console.log('No update for last name');
    } else {
      this.userProfileService.updateUserProfile(this.token, [{'last_name': newLastName}]);
    }

    if (!newYogaStyle) {
      console.log('No update for yoga style');
    } else {
      console.log({'yoga_style': newYogaStyle});
      this.defaultOption = newYogaStyle;
      this.userProfileService.updateUserProfile(this.token, [{'yoga_style': newYogaStyle}]);
    }

    this.accountDetailsForm.reset();
    this.showAlert = true;
    this.ngOnInit();
  }
}
