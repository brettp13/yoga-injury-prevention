import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpService } from '../shared/http.service';

import { environment } from '../../environments/environment';
import { UserService } from '../shared/user.service';

@Injectable()
export class PasswordValidationService {
    private api_url = environment.API_URL;
    token: string;
    httpHeaders = {};

    constructor(private http: HttpClient,
                private userService: UserService,
                private httpService: HttpService) {

        this.userService.token.subscribe(
            (token) => {
                this.token = token;
            });
    }

    validatePassword(password: any) {
        this.httpHeaders = this.httpService.createHeadersWithToken(this.token);
        console.log('called validatePassword');
        return this.http.post(this.api_url + '/auth/check-password/', password, this.httpHeaders);
    }
}