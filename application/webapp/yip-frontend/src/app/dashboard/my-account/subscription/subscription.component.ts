import { Component, OnInit } from '@angular/core';

import { UserService } from '../../../shared/user.service';

@Component({
  selector: 'app-subscription',
  templateUrl: './subscription.component.html',
  styleUrls: ['./subscription.component.css']
})
export class SubscriptionComponent implements OnInit {
  token: string;
  authInfo: any;

  constructor(private userService: UserService) { }

  ngOnInit() {
    this.userService.token.subscribe(
      (token) => {
        this.token = token;
      });

    this.userService.userAuthInfo.subscribe(
      (authInfo) => {
        console.log('received:');
        console.log(authInfo);
        this.authInfo = authInfo;
      });

    this.userService.getAuthInfo(this.token);
    console.log(this.token);
  }

}
