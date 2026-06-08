import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpService } from '../shared/http.service';

import { environment } from '../../environments/environment';
import { BehaviorSubject } from 'rxjs';

@Injectable()
export class UserProfileService {
    private api_url = environment.API_URL;
    userProfile: BehaviorSubject<any>;
    httpHeaders = {};

    constructor(private http:HttpClient, private httpService: HttpService) { 
        this.userProfile = new BehaviorSubject([]);
    };

    createUserProfile(token: string, info: any[]) {
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        this.http.post(this.api_url + '/profile/create-profile/', info[0], this.httpHeaders)
          .subscribe(
              (response) => {
                  console.log(response);
                  this.userProfile.next(response);
              },
              (error) => {
                  console.log(error);
              }
          )
    }

    getUserProfile(token: string) {
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        this.http.post(this.api_url + '/profile/profile-detail/', '', this.httpHeaders)
          .subscribe(
              (userProfile) => {
                  this.userProfile.next(userProfile);
              },
              (error) => {
                  console.log(error);
              }
          )
    }

    updateUserProfile(token:string, newProfileInfo: any[]) {
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        this.http.put(this.api_url + '/profile/profile-detail/', newProfileInfo[0], this.httpHeaders)
          .subscribe(
              (newProfileInfo) => {
                  this.userProfile.next(newProfileInfo);
              },
              (error) => {
                  console.log(error);
              }
          )
    }
    
}