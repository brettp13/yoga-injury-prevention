import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpService } from '../shared/http.service';
import { Router } from '@angular/router';

import { BehaviorSubject } from 'rxjs';

import { environment } from '../../environments/environment';
import { UserService } from './user.service';
import { UserProfileService } from './user.profile.service';

@Injectable()
export class SignupService {
    private api_url = environment.API_URL;
    signUpErrors: BehaviorSubject<any>;
    stripeToken: BehaviorSubject<string>;
    httpHeaders = {};

    constructor(private http: HttpClient,
                private httpService: HttpService,
                private userService: UserService,
                private userProfileService: UserProfileService,
                private router: Router) {
        this.signUpErrors = new BehaviorSubject([]);
        this.stripeToken = new BehaviorSubject('');
    }

    newStripeToken(token: string) {
        this.stripeToken.next(token);
    }

    createStripeSubscriber(email: string, token: string) {
        this.httpHeaders = this.httpService.createHeadersNoToken();
        var payload = {"email": email, "token": token}
        console.log(payload);

        this.http.post(this.api_url + '/stripe/create-subscriber/', payload, this.httpHeaders)
          .subscribe(
              (response) => {
                  console.log(response)
              },
              (error) => {
                  console.log(error)
              }
          )
    }

    createSignUp(userData: any[]) {
        this.httpHeaders = this.httpService.createHeadersNoToken();
        this.http.post(this.api_url + '/auth/create-user/', userData, this.httpHeaders)
          .subscribe(
              (response) => {
                  this.userService.newToken(response[0]['token']);
                  this.userService.signedIn();
                  this.userProfileService.createUserProfile(
                      response[0]['token'], 
                      [{
                          'first_name': userData[0]['first_name'], 
                          'last_name': userData[0]['last_name'], 
                          'yoga_style': userData[0]['yoga_style'],
                          'is_teacher': userData[0]['is_teacher'],
                          'email': userData[0]['email'],
                          'token': userData[0]['token'],
                          'traffic_source': userData[0]['traffic_source']
                      }]
                  );
                  //this.createStripeSubscriber(userData[0]['email'], userData[0]['token']);
                  this.router.navigate(['dashboard']);
              },
              (error) => {
                  this.signUpErrors.next(error.error.non_field_errors);
              }
          )
    }
}