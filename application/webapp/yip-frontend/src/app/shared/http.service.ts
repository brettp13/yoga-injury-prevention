import { Injectable } from '@angular/core';
import { HttpHeaders } from '@angular/common/http';

@Injectable()
export class HttpService {
    httpHeaders = {};
    
    createHeadersWithToken(token: string) {
        this.httpHeaders = {
            headers: new HttpHeaders({
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token
            })
        }
        return this.httpHeaders;
    }

    createHeadersNoToken() {
        this.httpHeaders = {
            headers: new HttpHeaders({
                'Content-Type': 'application/json'
            })
        }
        return this.httpHeaders;
    }
}