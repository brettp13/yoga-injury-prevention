import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpService } from '../shared/http.service';

import { environment } from '../../environments/environment';

@Injectable()
export class EmailValidationService {
    private api_url = environment.API_URL;
    httpHeaders = {};
    
    constructor(private http: HttpClient, private httpService: HttpService) {}

    validateEmail(email: any) {
        this.httpHeaders = this.httpService.createHeadersNoToken();
        return this.http.post(this.api_url + '/auth/does-email-exist/', email, this.httpHeaders);
    }
}