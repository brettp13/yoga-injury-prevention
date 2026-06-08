import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';

import { environment } from '../../../environments/environment';

@Injectable()
export class ContactService {
    private api_url = environment.API_URL;

    constructor(private http: HttpClient) {}

    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
      };

    createContactMessage(messageInfo: any[]) {
        return this.http.post(this.api_url + '/contact-us/', messageInfo, this.httpOptions);
    }
}
