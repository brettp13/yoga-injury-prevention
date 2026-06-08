import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpService } from '../shared/http.service';

import { BehaviorSubject } from 'rxjs';
import { Router } from '@angular/router';

import { environment } from '../../environments/environment';
 
@Injectable()
export class UserService {
    token_value= '';
    token: BehaviorSubject<string>;
    userSignedIn: BehaviorSubject<boolean>;
    private api_url = environment.API_URL;
    loginErrors: BehaviorSubject<any>;
    userAuthInfo: BehaviorSubject<any>;
    httpHeadersNoToken = {};
    httpHeadersWithToken = {};

    constructor (private http: HttpClient,
                 private router: Router,
                 private httpService: HttpService) {
        this.userSignedIn = new BehaviorSubject(false);
        this.token = new BehaviorSubject(this.token_value);
        this.loginErrors = new BehaviorSubject([]);
        this.userAuthInfo = new BehaviorSubject([]);
    };

    newToken(token_value: string) {
        this.token_value = token_value;
        this.token = new BehaviorSubject(token_value);
        localStorage.setItem('token', token_value);
    }

    signedIn() {
        this.userSignedIn.next(true);
    }

    signedOut() {
        this.userSignedIn.next(false);
        localStorage.removeItem('token');
    }

    login(email: string, password: string,) {
        this.httpHeadersNoToken = this.httpService.createHeadersNoToken();
        this.http.post(
            this.api_url + '/auth/login/', 
            {'email': email, 'password': password}, 
            this.httpHeadersNoToken
        ).subscribe(
            (response) => {
                this.newToken(response['token']);
                this.signedIn();
                this.router.navigate(['dashboard']);
            },
            (error) => {
                this.loginErrors.next(error.error.non_field_errors);
            }
        )

    }

    checkIfLoggedIn() {
        const token = localStorage.getItem('token');
        if (token) {
            this.signedIn();
            this.newToken(token);
            this.router.navigate(['dashboard']);
        }
    }

    getAuthInfo(token: string) {
        console.log('called getAuthInfo');
        this.httpHeadersWithToken = this.httpService.createHeadersWithToken(token);
        return this.http.get(
            this.api_url + '/auth/user-detail', 
            this.httpHeadersWithToken
        ).subscribe(
            (authInfo) => {
                this.userAuthInfo.next(authInfo);
            },
            (error) => {
                console.log(error);
            }
        )
    }

    updateAuthInfo(token: string, newAuthInfo: any[]) {
        this.httpHeadersWithToken = this.httpService.createHeadersWithToken(token);
        return this.http.put(
            this.api_url + '/auth/user-detail/', 
            newAuthInfo[0], 
            this.httpHeadersWithToken
        ).subscribe(
            (newAuthInfo) => {
                this.userAuthInfo.next(newAuthInfo);
            },
            (error) => {
                console.log(error);
            }
        )
    }
}
